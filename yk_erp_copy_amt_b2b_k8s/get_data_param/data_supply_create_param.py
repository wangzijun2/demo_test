from tool.configparser_paternal import ConfigParserPaternal


class SupplyCreateParam(ConfigParserPaternal):
    # 初始化所有ini配置文件字段
    def __init__(self):
        ConfigParserPaternal.__init__(self)
        # 读取配置文件参数
        self.cfg.read('..\\data_param_ini\\data_create_supply_ini.ini', encoding='utf-8')

    def return_supply_contract_save_param(self):
        return self.cfg.get('CREATE_SUPPLY', 'supply_contract_save_param')