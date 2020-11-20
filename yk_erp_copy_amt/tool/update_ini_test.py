import configparser


class Update:

    @staticmethod
    def update_ini(section, option, value, file):
        cfg = configparser.ConfigParser()
        cfg.read(file, encoding='utf-8')
        cfg.set(section, option, value)
        cfg.write(open(file, 'w', encoding='utf-8'))