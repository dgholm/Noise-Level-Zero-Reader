# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

import xml.etree.ElementTree as ET

class Option:
    def __init__(self, default_value = ''):
        self.Value = default_value

    def get(self):
        return self.Value

    def set(self, new_value):
        self.Value = new_value

class UserOptions:
    def __init__(self):
        self.AutomaticWho = Option()
        self.BlackHoleListEntries = Option()
        self.BrowserPath = Option()
        self.EchoInput = Option('0')
        self.EchoOutput = Option('0')
        self.HostName = Option()
        self.LoginName = Option()
        self.LoginPassword = Option()
        self.KeepAlive = Option('0')
        self.MailerPath = Option()
        self.ReadMode = Option()
        self.SystemType = Option()
        self.TraceEvents = Option('0')
        self.WordWrapAt72 = Option('1')

if __name__ == '__main__':
    opt = UserOptions()
