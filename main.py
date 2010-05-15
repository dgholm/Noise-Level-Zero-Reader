# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

import tkinter
from tkinter import ttk
from tkinter import StringVar
from options import Options
from program_options import ProgramOptions
from user_options import UserOptions
from telnetlib import Telnet
import re

class Main:
    def __init__(self):
        self.debug = False
        self.connected = False
        self.logged_in = False
        self.blink = False
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
        self.root.mainloop()

    def init_widgets(self):
        self.options = ttk.Button(self.root, command=self.options, text="Options", width=12)
        self.options.grid(column=0, row=0, sticky='w')
        self.conn = ttk.Button(self.root, command=self.connect, text='Connect', width=12)
        self.disc = ttk.Button(self.root, command=self.disconnect, text='Disconnect', width=12)
        self.conn.grid(column=1, row=0, sticky='w')
        self.entry = ttk.Entry(self.root, textvariable = self.Text, width=90)
        self.entry.grid(column=2, row=0, sticky='e')
        self.txt = tkinter.Text(self.root, width=80, height=50)
        self.txt.config(state = tkinter.DISABLED)
        self.txt.grid(column=0, row=1, columnspan=3, sticky='nwes')
        sb = ttk.Scrollbar(command=self.txt.yview, orient='vertical')
        sb.grid(column=3, row=1, sticky='ns')
        self.txt['yscrollcommand'] = sb.set

    def cancel(self, event = None):
        self.disconnect()
        geom = self.root.geometry()
        m = re.match("(\d+)x(\d+)([-+]\d+)([-+]\d+)", geom)
        if m:
            vals = m.groups()
            geom = "%s%s" % (vals[2], vals[3])
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
            self.append('\nConnected.\n')
            self.disc.grid(column=1, row=0, sticky='w')
            self.conn.grid_forget()
            self.connected = True
            self.root.update()
            self.process_telnet()

    def send_text(self, event = None):
        if self.telnet and self.connected:
            text = self.Text.get()
            if self.blink:
                text += ';;-BLINK\r\n'
                self.blink = False
            if self.debug:
                print(text)
            try:
                self.telnet.write(text.encode('ascii') + b'\r\n')
            except EOFError:
                self.show_disconnected()
                return
            self.Text.set('')
            if self.pw:
                self.append(b'*\r\n')
                self.pw = False

    def process_telnet(self):
        response = ''
        show = ''
        while self.telnet:
            text = None
            try:
                text = self.telnet.read_very_eager()
            except EOFError:
                self.show_disconnected()
                return
            if text:
                if self.debug:
                    print(text)
                self.append(text)
                if not self.logged_in and text.endswith(b'\r\nLogin: '):
                    response = b'nlz\r\n'
                    show = response
                elif not self.logged_in and text.endswith(b'Name? '):
                    if self.user.Login_Name.Value:
                        response = self.user.Login_Name.Value.encode('ascii') + b';;-BLINK\r\n'
                    else:
                        self.root.initial_focus.focus_set()
                        self.blink = True
                elif not self.logged_in and text.endswith(b'Password: '):
                    if self.user.Login_Password.Value:
                        response = self.user.Login_Password.Value.encode('ascii') + b'\r\n'
                        show = b'*\r\n'
                    else:
                        self.pw = True
                        self.root.initial_focus.focus_set()
                elif not self.logged_in and text.endswith(b'\r\n::: Ready!\r\n:'):
                    if self.debug:
                        print('Logged in!')
                    self.logged_in = True
                    self.root.initial_focus.focus_set()
                if response:
                    try:
                        self.telnet.write(response)
                    except EOFError:
                        self.show_disconnected()
                        return
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

if __name__ == '__main__':
    main = Main()
