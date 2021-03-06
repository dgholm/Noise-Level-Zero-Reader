# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

import codecs
import re
import tkinter
from tkinter import ttk
from tkinter import StringVar
from options import Options
from program_options import ProgramOptions
from user_options import UserOptions
from telnetlib import Telnet
from telnetlib import BINARY, DO, DONT, IAC, WILL, WONT
import webbrowser

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
        self.txt.bind('<Button-1>', self.single_click)
        self.txt.bind('<Double-1>', self.double_click)
        self.txt.bind_all('<<Selection>>', self.launch_web)
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
            self.telnet.set_option_negotiation_callback(self.telnet_negotiation)
            self.append('\nConnected.\n')
            self.disc.grid(column=1, row=0, sticky='w')
            self.conn.grid_forget()
            self.connected = True
            self.root.update()
            self.process_telnet()

    def single_click(self, event):
        self.d_click = False

    def double_click(self, event):
        self.d_click = True

    def launch_web(self, event):
        if self.d_click:
            try:
                text = event.widget.get('sel.first', 'sel.last')
            except:
                text = None
            print(text)
            if text:
                webbrowser.open(text)

    def send_text(self, event = None):
        if self.telnet and self.connected:
            line = self.Text.get().replace('\r\n', '\n').replace('\n\r', '\n').replace('\r', '\n')
            org_len = len(line) + self.cur_len
            first_time = True
            while first_time or len(line) > 0:
                first_time = False
                if len(line) + self.cur_len > 72:
                    idx = 72 - self.cur_len
                    while idx > 0 and ((not line[idx] in self.wrap_chars) or \
                            ((idx + 1 < len(line)) and (line[idx + 1] == '.'))):
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
                        response = b'nlz\n'
                        show = response
                    elif bytes.endswith(b'Name? '):
                        if self.user.Login_Name.Value:
                            response = self.user.Login_Name.Value.encode('utf-8') + b';;-BLINK\n'
                        else:
                            self.root.initial_focus.focus_set()
                            self.blink = True
                    elif bytes.endswith(b'Password: '):
                        if self.user.Login_Password.Value:
                            response = self.user.Login_Password.Value.encode('utf-8') + b'\n'
                            show = b'*\r\n'
                        else:
                            self.pw = True
                            self.root.initial_focus.focus_set()
                    elif bytes.find(b'\r\n::: Ready!') >= 0:
                        self.logged_in = True
                        if self.user.Read_Mode.Value:
                            response = 'read ' + self.user.Read_Mode.Value + '\n'
                        else:
                            response = ''
                        if self.user.Show_New.Value == '1':
                            if len(response) > 0:
                                response = 'show new; ' + response
                            else:
                                response = 'show new\n'
                        response = response.encode('utf-8')
                        self.root.initial_focus.focus_set()
                elif bytes.endswith(b'\x07Are you there? \r\n'):
                    if self.user.Keep_Alive.Value:
                        response = b'Yes\n'
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

    def telnet_negotiation(self, socket, command, option):
        if not self.negotiating:
            print('Sending the WILL BINARY (%s, %s, %s) command' %(IAC, WILL, BINARY))
            self.negotiating = True
            socket.send(IAC)
            socket.send(WILL)
            socket.send(BINARY)
            print('Sending the DO BINARY (%s, %s, %s) command' %(IAC, DO, BINARY))
            socket.send(IAC)
            socket.send(DO)
            socket.sendall(BINARY)
        response = WONT
        resp_text = 'WONT'
        if command==DO:
            print('Received a DO command (%s, %s, %s)' %(IAC, command, option))
            if option == BINARY:
                response = WILL
                resp_text = 'WILL'
            socket.send(IAC)
            socket.send(response)
            socket.sendall(option)
            print('Sent a %s response (%s, %s, %s)' %(resp_text, IAC, response, option))
        else:
            print('Ignoring a received command (%s, %s, %s)' %(IAC, command, option))
        return

if __name__ == '__main__':
    main = Main()
