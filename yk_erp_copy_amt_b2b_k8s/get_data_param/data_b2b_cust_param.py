from tool.configparser_paternal import ConfigParserPaternal


class DataCustParm(ConfigParserPaternal):

    # 初始化所有ini配置文件字段
    def __init__(self):
        ConfigParserPaternal.__init__(self)
        # 读取配置文件参数
        self.cfg.read('..\\data_param_ini\\data_b2b_cust_unit_ini.ini', encoding='utf-8')

    # 返回客户保存信息
    def return_cust_unit_reserved_no(self):
        return self.cfg.get('CUST_DATA', 'cust_unit_reserved_no')

    # 返回客户保存信息
    def return_cust_unit_params(self):
        return self.cfg.get('CUST_DATA', 'params')

