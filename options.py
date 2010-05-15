# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

import tkinter
from tkinter import ttk
from tkinter import StringVar
from user_options import UserOptions

class Options:
    def __init__(self, parent, user_options):
        self.user = user_options
        self.top = tkinter.Toplevel(parent)
        self.top.transient(parent)
        self.top.title('BIXpy User Options')
        self.top.parent = parent
        self.top.result = None
        self.Automatic_Who = StringVar()
        self.Automatic_Who.set(self.user.Automatic_Who.Value)
        self.Black_Hole_List_Entries = self.user.Black_Hole_List.Value
        self.Black_Hole_List = StringVar()
        self.Browser_Path = StringVar()
        self.Browser_Path.set(self.user.Browser_Path.Value)
        self.Echo_Input = StringVar()
        self.Echo_Input.set(self.user.Echo_Input.Value)
        self.Echo_Output = StringVar()
        self.Echo_Output.set(self.user.Echo_Output.Value)
        self.Host_Name = StringVar()
        self.Host_Name.set(self.user.Host_Name.Value)
        self.Login_Name = StringVar()
        self.Login_Name.set(self.user.Login_Name.Value)
        self.Login_Password = StringVar()
        self.Login_Password.set(self.user.Login_Password.Value)
        self.Keep_Alive = StringVar()
        self.Keep_Alive.set(self.user.Keep_Alive.Value)
        self.Mailer_Path = StringVar()
        self.Mailer_Path.set(self.user.Mailer_Path.Value)
        self.New_Black_Hole_Entry = StringVar()
        self.Read_Mode = StringVar()
        self.Read_Mode.set(self.user.Read_Mode.Value)
        self.System_Type = StringVar()
        self.System_Type.set(self.user.System_Type.Value)
        self.Trace_Events = StringVar()
        self.Trace_Events.set(self.user.Trace_Events.Value)
        self.Word_Wrap_at_72 = StringVar()
        self.Word_Wrap_at_72.set(self.user.Word_Wrap_at_72.Value)
        self.left_width = 0
        self.min_left_width = 23
        self.right_width = 31
        self.init_widgets()
        self.top.grab_set()
        self.top.initial_focus = self.top
        self.top.protocol("WM_DELETE_WINDOW", self.cancel)
        self.top.geometry("+%d+%d" % (parent.winfo_rootx()+24, parent.winfo_rooty()+48))
        self.top.bind("<Return>", self.ok)
        self.top.bind("<Escape>", self.cancel)
        self.top.initial_focus = self.widget18c
        self.top.initial_focus.focus_set()
        self.top.wait_window(self.top)

    def init_widgets(self):
        self.label1 = ttk.Label(self.top, text='System Type ', width=0)
        self.label1.grid(column=0, row=0, sticky='e')
        self.widget1 = ttk.Combobox(self.top, textvariable=self.System_Type, width=self.right_width, values=self.user.System_Type.Choices)
        self.widget1.grid(column=1, row=0, sticky='w')

        self.label2 = ttk.Label(self.top, text='Host Name ', width=self.left_width)
        self.label2.grid(column=0, row=1, sticky='e')
        self.widget2 = ttk.Entry(self.top, textvariable = self.Host_Name, width=self.right_width + 3)
        self.widget2.grid(column=1, row=1, sticky='w')

        self.label3 = ttk.Label(self.top, text='Login Name ', width=self.left_width)
        self.label3.grid(column=0, row=2, sticky='e')
        self.widget3 = ttk.Entry(self.top, textvariable = self.Login_Name, width=self.right_width + 3)
        self.widget3.grid(column=1, row=2, sticky='w')

        self.label4 = ttk.Label(self.top, text='Login Password ', width=self.left_width)
        self.label4.grid(column=0, row=3, sticky='e')
        self.widget4 = ttk.Entry(self.top, textvariable = self.Login_Password, width=self.right_width + 3)
        self.widget4.grid(column=1, row=3, sticky='w')

        self.label5 = ttk.Label(self.top, text='Read Mode ', width=self.left_width)
        self.label5.grid(column=0, row=4, sticky='e')
        self.widget5 = ttk.Combobox(self.top, textvariable=self.Read_Mode, width=self.right_width, values=self.user.Read_Mode.Choices)
        self.widget5.grid(column=1, row=4, sticky='w')

        self.label6 = ttk.Label(self.top, text='', width=self.left_width)
        self.label6.grid(column=0, row=5, sticky='e')
        self.widget6 = ttk.Checkbutton(self.top, text='Keep Alive', variable=self.Keep_Alive, width=self.right_width)
        self.widget6.grid(column=1, row=5, sticky='w')

        self.label7 = ttk.Label(self.top, text='', width=self.left_width)
        self.label7.grid(column=0, row=6, sticky='e')
        self.widget7 = ttk.Checkbutton(self.top, text='Automatic Who', variable=self.Automatic_Who, width=self.right_width)
        self.widget7.grid(column=1, row=6, sticky='w')

        self.label8 = ttk.Label(self.top, text='', width=self.left_width)
        self.label8.grid(column=0, row=7, sticky='e')
        self.widget8 = ttk.Checkbutton(self.top, text='Echo Input', variable=self.Echo_Input, width=self.right_width)
        self.widget8.grid(column=1, row=7, sticky='w')

        self.label9 = ttk.Label(self.top, text='', width=self.left_width)
        self.label9.grid(column=0, row=8, sticky='e')
        self.widget9 = ttk.Checkbutton(self.top, text='Echo Output', variable=self.Echo_Output, width=self.right_width)
        self.widget9.grid(column=1, row=8, sticky='w')

        self.label10 = ttk.Label(self.top, text='', width=self.left_width)
        self.label10.grid(column=0, row=9, sticky='e')
        self.widget10 = ttk.Checkbutton(self.top, text='Trace Events', variable=self.Trace_Events, width=self.right_width)
        self.widget10.grid(column=1, row=9, sticky='w')

        self.label11 = ttk.Label(self.top, text='', width=self.left_width)
        self.label11.grid(column=0, row=10, sticky='e')
        self.widget11 = ttk.Checkbutton(self.top, text='Word Wrap at 72', variable=self.Word_Wrap_at_72, width=self.right_width)
        self.widget11.grid(column=1, row=10, sticky='w')

        self.label12 = ttk.Label(self.top, text='Browser Path ', width=self.left_width)
        self.label12.grid(column=0, row=11, sticky='e')
        self.widget2 = ttk.Entry(self.top, textvariable = self.Browser_Path, width=self.right_width + 3)
        self.widget2.grid(column=1, row=11, sticky='w')

        self.label13 = ttk.Label(self.top, text='Mailer Path ', width=self.left_width)
        self.label13.grid(column=0, row=12, sticky='e')
        self.widget2 = ttk.Entry(self.top, textvariable = self.Mailer_Path, width=self.right_width + 3)
        self.widget2.grid(column=1, row=12, sticky='w')

        self.label14 = ttk.Label(self.top, text='Black Hole List ', width=self.left_width)
        self.label14.grid(column=0, row=13, sticky='e')
        self.widget14 = ttk.Combobox(self.top, textvariable=self.Black_Hole_List, width=self.right_width, values=self.user.Black_Hole_List.Value)
        self.widget14.grid(column=1, row=13, sticky='w')

        self.label15 = ttk.Label(self.top, text='New Black Hole Entry ', width=self.left_width)
        self.label15.grid(column=0, row=14, sticky='e')
        self.widget15 = ttk.Entry(self.top, textvariable = self.New_Black_Hole_Entry, width=self.right_width + 3)
        self.widget15.grid(column=1, row=14, sticky='w')

        self.widget16a = ttk.Button(self.top, text='Add', width=10)
        self.widget16a.grid(column=1, row=15, sticky='w')
        self.widget16b = ttk.Button(self.top, text='Delete', width=10)
        self.widget16b.grid(column=1, row=15, sticky='e')

        self.label17 = ttk.Label(self.top, text=' ', width=self.min_left_width)
        self.label17.grid(column=0, row=16, sticky='w')

        self.widget18a = ttk.Button(self.top, text='OK', command=self.ok, width=10)
        self.widget18a.grid(column=0, row=17, sticky='w')
        self.widget18b = ttk.Button(self.top, text='Save', command=self.save, width=10)
        self.widget18b.grid(column=1, row=17, sticky='w')
        self.widget18c = ttk.Button(self.top, text='Cancel', command=self.cancel, width=10)
        self.widget18c.grid(column=1, row=17, sticky='e')

    def copy_instance_values(self):
        # copy the instance values back to the UserOptions object.
        self.user.Automatic_Who.Value = self.Automatic_Who.get()
        self.user.Black_Hole_List.Value = self.Black_Hole_List_Entries
        self.user.Browser_Path.Value = self.Browser_Path.get()
        self.user.Echo_Input.Value = self.Echo_Input.get()
        self.user.Echo_Output.Value = self.Echo_Output.get()
        self.user.Host_Name.Value = self.Host_Name.get()
        self.user.Login_Name.Value = self.Login_Name.get()
        self.user.Login_Password.Value = self.Login_Password.get()
        self.user.Keep_Alive.Value = self.Keep_Alive.get()
        self.user.Mailer_Path.Value = self.Mailer_Path.get()
        self.user.Read_Mode.Value = self.Read_Mode.get()
        self.user.System_Type.Value = self.System_Type.get()
        self.user.Trace_Events.Value = self.Trace_Events.get()
        self.user.Word_Wrap_at_72.Value = self.Word_Wrap_at_72.get()

    def ok(self, event = None):
        self.copy_instance_values()
        self.cancel()

    def save(self, event = None):
        self.copy_instance_values()
        self.user.write('UserOptions')
        self.cancel()

    def cancel(self, event = None):
        self.top.parent.focus_set()
        self.top.destroy()

if __name__ == '__main__':
    user = UserOptions()
    root = tkinter.Tk()
    root.update()
    opt = Options(root, user)
