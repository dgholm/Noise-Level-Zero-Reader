# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

import tkinter
from tkinter import ttk
from tkinter import StringVar

class Options:
    def __init__(self, parent):
        self.parent = parent
        self.root = tkinter.Tk()
        self.root.title('BIXjoe Options')
        self.AutomaticWho = StringVar()
        self.BlackHoleListEntries = []
        self.BlackHoleList = StringVar()
        self.BrowserPath = StringVar()
        self.EchoInput = StringVar()
        self.EchoOutput = StringVar()
        self.HostName = StringVar()
        self.LoginName = StringVar()
        self.LoginPassword = StringVar()
        self.KeepAlive = StringVar()
        self.MailerPath = StringVar()
        self.NewBlackHoleEntry = StringVar()
        self.ReadMode = StringVar()
        self.SystemType = StringVar()
        self.TraceEvents = StringVar()
        self.WordWrapAt72 = StringVar()
        self.left_width = 0
        self.min_left_width = 23
        self.right_width = 31
        self.init_widgets()

    def init_widgets(self):
        self.label1 = ttk.Label(self.root, text='System Type ', width=0)
        self.label1.grid(column=0, row=0, sticky='e')
        self.widget1 = ttk.Combobox(self.root, textvariable=self.SystemType, width=self.right_width, values=['NLZ', 'Test'])
        self.widget1.grid(column=1, row=0, sticky='w')

        self.label2 = ttk.Label(self.root, text='Host Name ', width=self.left_width)
        self.label2.grid(column=0, row=1, sticky='e')
        self.widget2 = ttk.Entry(self.root, textvariable = self.HostName, width=self.right_width + 3)
        self.widget2.grid(column=1, row=1, sticky='w')

        self.label3 = ttk.Label(self.root, text='Login Name ', width=self.left_width)
        self.label3.grid(column=0, row=2, sticky='e')
        self.widget3 = ttk.Entry(self.root, textvariable = self.LoginName, width=self.right_width + 3)
        self.widget3.grid(column=1, row=2, sticky='w')

        self.label4 = ttk.Label(self.root, text='Login Password ', width=self.left_width)
        self.label4.grid(column=0, row=3, sticky='e')
        self.widget4 = ttk.Entry(self.root, textvariable = self.LoginPassword, width=self.right_width + 3)
        self.widget4.grid(column=1, row=3, sticky='w')

        self.label5 = ttk.Label(self.root, text='Read Mode ', width=self.left_width)
        self.label5.grid(column=0, row=4, sticky='e')
        self.widget5 = ttk.Combobox(self.root, textvariable=self.ReadMode, width=self.right_width, values=['reference', 'forward', 'backward'])
        self.widget5.grid(column=1, row=4, sticky='w')

        self.label6 = ttk.Label(self.root, text='', width=self.left_width)
        self.label6.grid(column=0, row=5, sticky='e')
        self.widget6 = ttk.Checkbutton(self.root, text='Keep Alive', variable=self.KeepAlive, width=self.right_width)
        self.widget6.grid(column=1, row=5, sticky='w')

        self.label7 = ttk.Label(self.root, text='', width=self.left_width)
        self.label7.grid(column=0, row=6, sticky='e')
        self.widget7 = ttk.Checkbutton(self.root, text='Automatic Who', variable=self.AutomaticWho, width=self.right_width)
        self.widget7.grid(column=1, row=6, sticky='w')

        self.label8 = ttk.Label(self.root, text='', width=self.left_width)
        self.label8.grid(column=0, row=7, sticky='e')
        self.widget8 = ttk.Checkbutton(self.root, text='Echo Input', variable=self.EchoInput, width=self.right_width)
        self.widget8.grid(column=1, row=7, sticky='w')

        self.label9 = ttk.Label(self.root, text='', width=self.left_width)
        self.label9.grid(column=0, row=8, sticky='e')
        self.widget9 = ttk.Checkbutton(self.root, text='Echo Output', variable=self.EchoOutput, width=self.right_width)
        self.widget9.grid(column=1, row=8, sticky='w')

        self.label10 = ttk.Label(self.root, text='', width=self.left_width)
        self.label10.grid(column=0, row=9, sticky='e')
        self.widget10 = ttk.Checkbutton(self.root, text='Trace Events', variable=self.TraceEvents, width=self.right_width)
        self.widget10.grid(column=1, row=9, sticky='w')

        self.label11 = ttk.Label(self.root, text='', width=self.left_width)
        self.label11.grid(column=0, row=10, sticky='e')
        self.widget11 = ttk.Checkbutton(self.root, text='Word Wrap at 72', variable=self.WordWrapAt72, width=self.right_width)
        self.widget11.grid(column=1, row=10, sticky='w')

        self.label12 = ttk.Label(self.root, text='Browser Path ', width=self.left_width)
        self.label12.grid(column=0, row=11, sticky='e')
        self.widget2 = ttk.Entry(self.root, textvariable = self.BrowserPath, width=self.right_width + 3)
        self.widget2.grid(column=1, row=11, sticky='w')

        self.label13 = ttk.Label(self.root, text='Mailer Path ', width=self.left_width)
        self.label13.grid(column=0, row=12, sticky='e')
        self.widget2 = ttk.Entry(self.root, textvariable = self.MailerPath, width=self.right_width + 3)
        self.widget2.grid(column=1, row=12, sticky='w')

        self.label14 = ttk.Label(self.root, text='Black Hole List ', width=self.left_width)
        self.label14.grid(column=0, row=13, sticky='e')
        self.widget14 = ttk.Combobox(self.root, textvariable=self.BlackHoleList, width=self.right_width, values=self.BlackHoleListEntries)
        self.widget14.grid(column=1, row=13, sticky='w')

        self.label15 = ttk.Label(self.root, text='New Black Hole Entry ', width=self.left_width)
        self.label15.grid(column=0, row=14, sticky='e')
        self.widget15 = ttk.Entry(self.root, textvariable = self.NewBlackHoleEntry, width=self.right_width + 3)
        self.widget15.grid(column=1, row=14, sticky='w')

        self.widget16a = ttk.Button(self.root, text='Add', width=10)
        self.widget16a.grid(column=1, row=15, sticky='w')
        self.widget16b = ttk.Button(self.root, text='Delete', width=10)
        self.widget16b.grid(column=1, row=15, sticky='e')

        self.label17 = ttk.Label(self.root, text=' ', width=self.min_left_width)
        self.label17.grid(column=0, row=16, sticky='w')

        self.widget18a = ttk.Button(self.root, text='OK', width=10)
        self.widget18a.grid(column=0, row=17, sticky='w')
        self.widget18b = ttk.Button(self.root, text='Save', width=10)
        self.widget18b.grid(column=1, row=17, sticky='w')
        self.widget18c = ttk.Button(self.root, text='Cancel', width=10)
        self.widget18c.grid(column=1, row=17, sticky='e')

if __name__ == '__main__':
    opt = Options(None)
    opt.root.mainloop()
