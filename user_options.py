# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

from base_options import Option, OptionsBase

class UserOptions(OptionsBase):
    def __init__(self):
        OptionsBase.__init__(self)
        options = []
        self.Automatic_Who = Option(
            'Automatic Who', 'boolean', None, '0')
        options.append(self.Automatic_Who)
        self.Black_Hole_List = Option(
            'Black Hole List', 'list', None, [])
        options.append(self.Black_Hole_List)
        self.Browser_Path = Option(
            'Browser Path', 'string', None, '')
        options.append(self.Browser_Path)
        self.Echo_Input = Option(
            'Echo Input', 'boolean', None, '0')
        options.append(self.Echo_Input)
        self.Echo_Output = Option(
            'Echo Output', 'boolean', None, '0')
        options.append(self.Echo_Output)
        self.Host_Name = Option(
            'Host Name', 'string', None, '')
        options.append(self.Host_Name)
        self.Login_Name = Option(
            'Login Name', 'string', None, '')
        options.append(self.Login_Name)
        self.Login_Password = Option(
            'Login Password', 'password', None, '')
        options.append(self.Login_Password)
        self.Keep_Alive = Option(
            'Keep Alive', 'boolean', None, '0')
        options.append(self.Keep_Alive)
        self.Mailer_Path = Option(
            'Mailer Path', 'string', None, '')
        options.append(self.Mailer_Path)
        self.Read_Mode = Option(
            'Read Mode', 'choice', ['backward', 'forward', 'reference'], '')
        options.append(self.Read_Mode)
        self.System_Type = Option(
            'System Type', 'choice', ['NLZ', 'other', 'test'], '')
        options.append(self.System_Type)
        self.Trace_Events = Option(
            'Trace Events', 'boolean', None, '0')
        options.append(self.Trace_Events)
        self.Word_Wrap_at_72 = Option(
            'Word Wrap At 72', 'boolean', None, '1')
        options.append(self.Word_Wrap_at_72)

        self._options = options

if __name__ == '__main__':
    opt = UserOptions()
    print(opt)
