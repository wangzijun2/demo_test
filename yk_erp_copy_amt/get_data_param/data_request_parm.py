from tool.configparser_paternal import ConfigParserPaternal


class DataRequest(ConfigParserPaternal):
    # 定义data参数接收值
    data = {}

    def __init__(self):
        # 调用父类构造函数
        ConfigParserPaternal.__init__(self)
        # 读取request请求方法配置文件
        self.cfg.read('..\\data_param_ini\\data_request_ini.ini', encoding='utf-8')
        self.data['url'] = self.cfg.get('DATA', 'url')
        self.data['method'] = self.cfg.get('DATA', 'method')
        self.data['params'] = self.cfg.get('DATA', 'params')
        self.data['app_key'] = self.cfg.getint('DATA', 'app_key')
        self.data['convert_flag'] = self.cfg.get('DATA', 'convert_flag')

    def get_data(self):
        return self.data
