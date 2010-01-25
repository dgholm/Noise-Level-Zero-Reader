# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

import xml.etree.ElementTree as ET

_string_test = 'string'
class Option:
    def __init__(self, name = None, type = None, choices = None, default_value = None):
        self.Name = name
        self.Node = name.replace(' ', '')
        self.Type = type
        self.Choices = choices
        self.Value = default_value

    def __str__(self):
        if type(_string_test) == type(self.Value):
            value_str = '\'%s\'' % (self.Value)
        else:
            value_str = str(self.Value)
        return '[Name=\'%s\', Node=\'%s\', Type=\'%s\', Choices=%s, Value=%s]' %(
            self.Name, self.Node, self.Type, self.Choices, value_str)

class UserOptions:
    def __init__(self):
        options = []
        self.AutomaticWho = Option(
            'Automatic Who', 'boolean', None, '0')
        options.append(self.AutomaticWho)
        self.BlackHoleList = Option(
            'Black Hole List', 'list', None, [])
        options.append(self.BlackHoleList)
        self.BrowserPath = Option(
            'Browser Path', 'string', None, '')
        options.append(self.BrowserPath)
        self.EchoInput = Option(
            'Echo Input', 'boolean', None, '0')
        options.append(self.EchoInput)
        self.EchoOutput = Option(
            'Echo Output', 'boolean', None, '0')
        options.append(self.EchoOutput)
        self.HostName = Option(
            'Host Name', 'string', None, '')
        options.append(self.HostName)
        self.LoginName = Option(
            'Login Name', 'string', None, '')
        options.append(self.LoginName)
        self.LoginPassword = Option(
            'Login Password', 'password', None, '')
        options.append(self.LoginPassword)
        self.KeepAlive = Option(
            'Keep Alive', 'boolean', None, '0')
        options.append(self.KeepAlive)
        self.MailerPath = Option(
            'Mailer Path', 'string', None, '')
        options.append(self.MailerPath)
        self.ReadMode = Option(
            'Read Mode', 'choice', ['backward', 'forward', 'reference'], '')
        options.append(self.ReadMode)
        self.SystemType = Option(
            'System Type', 'choice', ['NLZ', 'other', 'test'], '')
        options.append(self.SystemType)
        self.TraceEvents = Option(
            'Trace Events', 'boolean', None, '0')
        options.append(self.TraceEvents)
        self.WordWrapAt72 = Option(
            'Word Wrap At 72', 'boolean', None, '1')
        options.append(self.WordWrapAt72)

        self.Options = {}
        for option in options:
            self.Options[option.Name] = option

        del options

    def __str__(self):
        first = True
        text = '['
        for name in self.Options:
            if first:
                first = False
            else:
                text += ', '
            text += str(self.Options[name])
        text += ']'
        return text

if __name__ == '__main__':
    opt = UserOptions()
    print(opt)
