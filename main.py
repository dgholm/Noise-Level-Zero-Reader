# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

import tkinter
from tkinter import ttk

class Main:
    def __init__(self, parent):
        self.parent = parent
        self.root = tkinter.Tk()
        self.root.title('BIXjoe')
        self.init_widgets()

    def init_widgets(self):
        self.connect = ttk.Button(self.root, command=self.connect, text='Connect', width=12)
        self.disconnect = ttk.Button(self.root, command=self.disconnect, text='Disconnect', width=12)
        self.connect.grid(column=0, row=0, sticky='w')
        self.entry = ttk.Entry(self.root, width=90)
        self.entry.grid(column=0, row=0, sticky='e')
        self.txt = tkinter.Text(self.root, width=80, height=50)
        self.txt.grid(column=0, row=1, sticky='nwes')
        sb = ttk.Scrollbar(command=self.txt.yview, orient='vertical')
        sb.grid(column=1, row=1, sticky='ns')
        self.txt['yscrollcommand'] = sb.set

    def connect(self):
        self.insert('Connecting...')
        self.disconnect.grid(column=0, row=0, sticky='w')
        self.connect.grid_forget()

    def disconnect(self):
        self.insert('Disconnecting...')
        self.connect.grid(column=0, row=0, sticky='w')
        self.disconnect.grid_forget()

    def insert(self, text):
        self.txt.insert(tkinter.INSERT, text)

if __name__ == '__main__':
    main = Main(None)
    main.root.mainloop()
