# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

from xml.etree import ElementTree as ET

_string_test = 'string'
class Option:
    def __init__(self, name = None, type = None, choices = None, default_value = None):
        self.Name = name
        self.Node = name.replace(' ', '_')
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

class OptionsBase:
    def __init__(self):
        self.debug = False
        self.root_tag = 'BIXpy'
        self._options = []

    def read(self, option_section):
        tree = ET.ElementTree()
        tree.parse('%s%s.xml' %(self.root_tag, option_section))
        root = tree.getroot()
        if self.debug:
            print(root)
        if not root.tag == self.root_tag:
            # TODO: Display a pop-up error
            return
        element = tree.find('/' + option_section)
        if self.debug:
            print(element)
        if not element:
            # TODO: Display a pop-up error
            return
        for option in self._options:
            element = tree.find('/%s/%s' %(option_section, option.Node))
            if self.debug:
                print(element)
                print(element.tag)
                print(element.text)
            if not element == None:
                if self.debug:
                    print(element.text)
                if element.text:
                    option.Value = element.text

    def write(self, option_section):
        parser = ET.TreeBuilder()
        attr = dict()
        attr['Version'] = '1.0'
        parser.start(self.root_tag, attr)
        parser.data('\r\n\t')
        parser.start(option_section, dict())
        parser.data('\r\n')
        for option in self._options:
            if self.debug:
                print(option.Name, option.Node, option.Value)
                print()
            parser.data('\t\t')
            name = option.Node
            parser.start(name, dict())
            parser.data(str(option.Value))
            parser.end(name)
            parser.data('\r\n')
        parser.data('\t')
        parser.end(option_section)
        parser.data('\r\n')
        parser.end(self.root_tag)
        tree = ET.ElementTree(parser.close())
        tree.write('%s%s.xml' %(self.root_tag, option_section))

    def __str__(self):
        first = True
        text = '['
        for option in self._options:
            if first:
                first = False
            else:
                text += ', '
            text += str(option)
        text += ']'
        return text

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
