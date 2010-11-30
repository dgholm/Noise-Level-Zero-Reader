# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

import codecs
import tkinter
from tkinter import ttk
from tkinter import StringVar
from options import Options
from program_options import ProgramOptions
from user_options import UserOptions
from telnetlib import Telnet
from telnetlib import BINARY, DO, DONT, IAC, WILL, WONT
import re

class Main:
    def __init__(self):
        self.connected = False
        self.logged_in = False
        self.negotiating = False
        self.utf8 = codecs.lookup('utf-8')
        self.blink = False
        self.cur_len = 0
        self.pw = False
        self.root = tkinter.Tk()
        self.root.title('BIXpy')
        self.Text = StringVar()
        self.init_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.prog = ProgramOptions()
        self.prog.read('ProgramOptions')
        geom = self.prog.Main_Geometry.Value
        if geom:
            self.root.geometry(geom)
        self.root.bind("<Return>", self.send_text)
        self.root.initial_focus = self.entry
        self.root.initial_focus.focus_set()
        self.user = UserOptions()
        self.user.read('UserOptions')
        self.telnet = None
        self.wrap_chars = ' ,;:/\\]})=-+\n'
        self.root.mainloop()

    def init_widgets(self):
        self.options = ttk.Button(self.root, command=self.options, text="Options", width=12)
        self.options.grid(column=0, row=0, sticky='w')
        self.conn = ttk.Button(self.root, command=self.connect, text='Connect', width=12)
        self.disc = ttk.Button(self.root, command=self.disconnect, text='Disconnect', width=12)
        self.conn.grid(column=1, row=0, sticky='w')
        self.entry = ttk.Entry(self.root, textvariable = self.Text, width=90)
        self.entry.grid(column=2, row=0, sticky='ew')
        self.txt = tkinter.Text(self.root, width=80, height=50)
        self.txt.config(state = tkinter.DISABLED)
        self.txt.grid(column=0, row=1, columnspan=3, sticky='nwes')
        sb = ttk.Scrollbar(command=self.txt.yview, orient='vertical')
        sb.grid(column=3, row=1, sticky='ns')
        self.txt['yscrollcommand'] = sb.set
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def cancel(self, event = None):
        self.disconnect()
        if self.root.state() == 'normal':
            geom = self.root.geometry()
            self.prog.Main_Geometry.Value = geom
        self.prog.write('ProgramOptions')
        self.root.destroy()

    def connect(self):
        if not self.connected:
            self.append('\nConnecting...')
            self.root.update()
            if self.telnet:
                self.telnet.close()
            host = self.user.Host_Name.Value
            if not host:
                host = 'nlzero.com'
            self.telnet = Telnet(host, 23, 60)
            self.telnet.set_option_negotiation_callback(self.telnet_negotiate)
            self.append('\nConnected.\n')
            self.disc.grid(column=1, row=0, sticky='w')
            self.conn.grid_forget()
            self.connected = True
            self.root.update()
            self.process_telnet()

    def send_text(self, event = None):
        if self.telnet and self.connected:
            line = self.Text.get().replace('\r\n', '\n').replace('\n\r', '\n').replace('\r', '\n')
            org_len = len(line) + self.cur_len
            first_time = True
            while first_time or len(line) > 0:
                first_time = False
                if len(line) + self.cur_len > 72:
                    idx = 72 - self.cur_len
                    while idx > 0 and not line[idx] in self.wrap_chars:
                        idx -= 1
                    if idx == 0:
                        if self.cur_len > 0:
                            if line[0] in self.wrap_chars:
                                idx += 1
                        else:
                            idx = 72 - self.cur_len
                    else:
                        idx += 1
                    nl_idx = line.find('\n')
                    if nl_idx >= 0 and nl_idx < idx:
                        idx = nl_idx
                        found_nl = True
                    else:
                        found_nl = False
                    text = line[0:idx] + '\n'
                    if found_nl:
                        idx += 1
                    line = line[idx:]
                    self.cur_len = 0
                else:
                    text = line
                    nl_idx = text.find('\n')
                    if nl_idx < 0:
                        line = ''
                    else:
                        text = line[0:nl_idx]
                        line = line[nl_idx + 1:]
                    if org_len > 72 or nl_idx >= 0:
                        self.cur_len = len(text)
                    else:
                        self.cur_len = 0
                        text += '\n'
                if self.blink:
                    text += ';;-BLINK\n'
                    self.blink = False
                try:
                    bytes = self.utf8.encode(text)[0]
                    if self.user.Echo_Output.Value == '1':
                        print('-->', bytes)
                    self.telnet.write(bytes)
                except EOFError:
                    self.show_disconnected()
                    return
                self.Text.set('')
                if self.pw:
                    text = b'*\n'
                    self.append(text)
                    self.pw = False
                if self.user.Echo_Output.Value == '1':
                    print('-->', text)

    def process_telnet(self):
        response = ''
        show = ''
        while self.telnet:
            text = None
            try:
                bytes = self.telnet.read_very_eager()
            except EOFError:
                self.show_disconnected()
                return
            if bytes:
                if self.user.Echo_Input.Value == '1':
                    print('<--', bytes)
                text = self.utf8.decode(bytes, 'replace')[0]
                self.append(text)
                if not self.logged_in:
                    if bytes.endswith(b'\r\nLogin: '):
                        response = b'nlz\r\n'
                        show = response
                    elif bytes.endswith(b'Name? '):
                        if self.user.Login_Name.Value:
                            response = self.user.Login_Name.Value.encode('utf-8') + b';;-BLINK\r\n'
                        else:
                            self.root.initial_focus.focus_set()
                            self.blink = True
                    elif bytes.endswith(b'Password: '):
                        if self.user.Login_Password.Value:
                            response = self.user.Login_Password.Value.encode('utf-8') + b'\r\n'
                            show = b'*\r\n'
                        else:
                            self.pw = True
                            self.root.initial_focus.focus_set()
                    elif bytes.find(b'\r\n::: Ready!') >= 0:
                        self.logged_in = True
                        if self.user.Read_Mode.Value:
                            response = 'read ' + self.user.Read_Mode.Value + '\r\n'
                        else:
                            response = ''
                        if self.user.Show_New.Value == '1':
                            if len(response) > 0:
                                response = 'show new; ' + response
                            else:
                                response = 'show new\r\n'
                        response = response.encode('utf-8')
                        self.root.initial_focus.focus_set()
                elif bytes.endswith(b'\x07Are you there? \r\n'):
                    if self.user.Keep_Alive.Value:
                        response = b'Yes\r\n'
                if response:
                    try:
                        self.telnet.write(response)
                    except EOFError:
                        self.show_disconnected()
                        return
                    if self.user.Echo_Output.Value == '1':
                        if show:
                            print('-->', show)
                        else:
                            print('-->', response)
                    response = ''
                if show:
                    self.append(show)
                    show = ''
            self.root.update()

    def disconnect(self):
        if self.connected:
            self.append('\nDisconnecting...')
            self.root.update()
            if self.telnet:
                self.telnet.close()
                self.telnet = None
            self.show_disconnected()

    def show_disconnected(self):
        self.append('\nDisconnected.\n')
        self.conn.grid(column=1, row=0, sticky='w')
        self.disc.grid_forget()
        self.connected = False
        self.logged_in = False

    def append(self, text):
        self.txt.config(state = tkinter.NORMAL)
        self.txt.insert(tkinter.END, text)
        self.txt.config(state = tkinter.DISABLED)
        self.txt.see(tkinter.END)

    def options(self):
        opt = Options(self.root, self.user)

    def telnet_negotiate(self, sock, command, option):
        #
        # I found the source for this method on the web and made some
        # changes to it for my use in BIXpy:
        #
        # http://www.velocityreviews.com/forums/
        # t342450-usage-example-for-ansi-py-from-the-pexpect-package.html
        #
        # Here's a function I came up with to handle sub-negotiation.
        # During session negotiation, the server can ask a series of
        # "will you or won't you" questions of the client. One of
        # those questions happens to be:
        # "Will you tell me what terminal type you are?"
        # This question is the only one out of the possible list of
        # such questions that I respond with "Yes, I will." Then later
        # the function reports that the terminal type is a DEC VT-100.
        # If you don't do the sub-negotiation and the server demands
        # to know the terminal type, the Telnet function will report
        # that the terminal type is simply "network". No server will
        # recognize this, and some will refuse to even start a session
        # with you using some default terminal type.
        # A couple of good links--
        # http://www.cs.cf.ac.uk/Dave/Internet/node136.html
        # http://www.scit.wlv.ac.uk/rfc/rfc8xx/RFC854.html
        #
        negotiation_list=[
            ['BINARY',WILL,'WONT'],
            ['ECHO',WONT,'WONT'],
            ['RCP',WONT,'WONT'],
            ['SGA',WONT,'WONT'],
            ['NAMS',WONT,'WONT'],
            ['STATUS',WONT,'WONT'],
            ['TM',WONT,'WONT'],
            ['RCTE',WONT,'WONT'],
            ['NAOL',WONT,'WONT'],
            ['NAOP',WONT,'WONT'],
            ['NAOCRD',WONT,'WONT'],
            ['NAOHTS',WONT,'WONT'],
            ['NAOHTD',WONT,'WONT'],
            ['NAOFFD',WONT,'WONT'],
            ['NAOVTS',WONT,'WONT'],
            ['NAOVTD',WONT,'WONT'],
            ['NAOLFD',WONT,'WONT'],
            ['XASCII',WONT,'WONT'],
            ['LOGOUT',WONT,'WONT'],
            ['BM',WONT,'WONT'],
            ['DET',WONT,'WONT'],
            ['SUPDUP',WONT,'WONT'],
            ['SUPDUPOUTPUT',WONT,'WONT'],
            ['SNDLOC',WONT,'WONT'],
            ['TTYPE',WONT,'WONT'],
            ['EOR',WONT,'WONT'],
            ['TUID',WONT,'WONT'],
            ['OUTMRK',WONT,'WONT'],
            ['TTYLOC',WONT,'WONT'],
            ['VT3270REGIME',WONT,'WONT'],
            ['X3PAD',WONT,'WONT'],
            ['NAWS',WONT,'WONT'],
            ['TSPEED',WONT,'WONT'],
            ['LFLOW',WONT,'WONT'],
            ['LINEMODE',WONT,'WONT'],
            ['XDISPLOC',WONT,'WONT'],
            ['OLD_ENVIRON',WONT,'WONT'],
            ['AUTHENTICATION',WONT,'WONT'],
            ['ENCRYPT',WONT,'WONT'],
            ['NEW_ENVIRON',WONT,'WONT']
        ]
        if ord(option)<40:
            received_option=negotiation_list[ord(option)][0]
            response=negotiation_list[ord(option)][1]
            print_response=negotiation_list[ord(option)][2]
        else:
            received_option='unrecognised'
            response=WONT
            print_response='WONT'
        if command==DO:
            print("Received request to DO %s, sending %s" % \
            (received_option,print_response))
            #print(IAC, response, option)
            sock.sendall(IAC)
            sock.sendall(response)
            sock.sendall(option)
        elif command==DONT:
            print('Received the DONT %s command' %(received_option))
        elif command==WILL:
            print('Received the WILL %s command' %(received_option))
        elif command==WONT:
            print('Received the WONT %s command' %(received_option))
        elif command==theNULL:
            print('Received the NULL command')
        elif command==SB:
            print('Received the SB command')
            print(ord(option))
            print(self.conn.read_sb_data())
        elif command==SE:
            print('Received the SE command')
        else:
            print('Received something, don''t know what.')
            print(ord(option))
        if not self.negotiating:
            print('Sending the WILL BINARY and DO BINARY commands')
            self.negotiating = True
            sock.sendall(IAC)
            sock.sendall(DO)
            sock.sendall(BINARY)
            sock.sendall(IAC)
            sock.sendall(WILL)
            sock.sendall(BINARY)
        return

if __name__ == '__main__':
    main = Main()
