# vim:tabstop=8:shiftwidth=4:smarttab:expandtab:softtabstop=4:autoindent:

from base_options import Option, OptionsBase

class ProgramOptions(OptionsBase):
    def __init__(self):
        OptionsBase.__init__(self)
        options = []
        self.Main_Geometry = Option(
            'Main Geometry', 'string', None, '+48+48')
        options.append(self.Main_Geometry)

        self._options = options

if __name__ == '__main__':
    opt = ProgramOptions()
    print(opt)
