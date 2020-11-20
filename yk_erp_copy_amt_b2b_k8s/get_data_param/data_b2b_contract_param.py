from tool.configparser_paternal import ConfigParserPaternal


class DataContractParm(ConfigParserPaternal):

    # 初始化所有ini配置文件字段
    def __init__(self):
        ConfigParserPaternal.__init__(self)
        # 读取配置文件参数
        self.cfg.read('..\\data_param_ini\\data_b2b_cust_contract_ini.ini', encoding='utf-8')

    # 返回销售合同保存信息
    def return_contract_param(self):
        return self.cfg.get('CONTRACT_DATA', 'param')

    # 返回销售合同做单单号
    def return_contract_reserved(self):
        return self.cfg.get('CONTRACT_DATA', 'contract_reserved_no')
    
    # 返回销售合同客户编码
    def return_unit_num_id(self):
        return self.cfg.get('CONTRACT_DATA', 'login_name_unit_num_id')