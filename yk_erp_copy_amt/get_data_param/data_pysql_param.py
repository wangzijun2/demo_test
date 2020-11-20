from tool.configparser_paternal import ConfigParserPaternal


class DataPysql(ConfigParserPaternal):
    # 定义data参数接收值
    data = {}

    def __init__(self):
        # 调用父类构造函数
        ConfigParserPaternal.__init__(self)
        # 读取request请求方法配置文件
        self.cfg.read('..\\data_param_ini\\data_pysql_ini.ini', encoding='utf-8')
        self.data["host"] = self.cfg.get('MYSQL_DATA', 'host')
        self.data["user"] = self.cfg.get('MYSQL_DATA', 'user')
        self.data["passwd"] = self.cfg.get('MYSQL_DATA', 'passwd')
        self.data["db"] = self.cfg.get('MYSQL_DATA', 'db')
        self.data["port"] = self.cfg.getint('MYSQL_DATA', 'port')

    def get_pysqldata(self):
        return self.data
