import configparser


class Update:
    file = '..\\data_ini.ini'

    def update_ini(self, section, option, value):
        cfg = configparser.ConfigParser()
        cfg.read(self.file)
        cfg.set(section, option, value)
        cfg.write(open(self.file, 'w'))