# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

import tkinter
from tkinter import ttk
from options import Options
from user_options import UserOptions

class Main:
    def __init__(self, parent):
        self.parent = parent
        self.root = tkinter.Tk()
        self.root.title('BIXjoe')
        self.init_widgets()
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.root.geometry("+%d+%d" % (48, 48))
        self.root.initial_focus = self.entry
        self.root.initial_focus.focus_set()
        self.root.mainloop()

    def init_widgets(self):
        self.user = UserOptions()
        self.options = ttk.Button(self.root, command=self.options, text="Options", width=12)
        self.options.grid(column=0, row=0, sticky='w')
        self.connect = ttk.Button(self.root, command=self.connect, text='Connect', width=12)
        self.disconnect = ttk.Button(self.root, command=self.disconnect, text='Disconnect', width=12)
        self.connect.grid(column=1, row=0, sticky='w')
        self.entry = ttk.Entry(self.root, width=90)
        self.entry.grid(column=2, row=0, sticky='e')
        self.txt = tkinter.Text(self.root, width=80, height=50)
        self.txt.grid(column=0, row=1, columnspan=3, sticky='nwes')
        sb = ttk.Scrollbar(command=self.txt.yview, orient='vertical')
        sb.grid(column=3, row=1, sticky='ns')
        self.txt['yscrollcommand'] = sb.set

    def cancel(self, event = None):
        # check to see if still connected...
        self.root.destroy()

    def connect(self):
        self.insert('Connecting...')
        self.disconnect.grid(column=1, row=0, sticky='w')
        self.connect.grid_forget()

    def disconnect(self):
        self.insert('Disconnecting...')
        self.connect.grid(column=1, row=0, sticky='w')
        self.disconnect.grid_forget()

    def insert(self, text):
        self.txt.insert(tkinter.INSERT, text)

    def options(self):
        opt = Options(self.root, self.user)

if __name__ == '__main__':
    main = Main(None)
