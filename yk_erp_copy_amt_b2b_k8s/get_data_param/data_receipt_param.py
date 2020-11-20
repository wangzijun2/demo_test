from tool.configparser_paternal import ConfigParserPaternal


class DataReceipt(ConfigParserPaternal):

    def __init__(self):
        ConfigParserPaternal.__init__(self)
        # 读取配置文件参数
        self.supply_param = {}
        self.cfg.read('..\\data_param_ini\\data_receipt_num_id_ini.ini', encoding='utf-8')

    def return_receipt_num_id(self):
        # 验收单单号
        return self.cfg.get('RECEIPT_DATE_PARAMS', 'receipt_num_id')

    def get_receipt_num_hdr_params(self):
        # 验收单表头收货参数
        return self.cfg.get('RECEIPT_DATE_PARAMS', 'receipt_num_hdr_params')

    def get_update_dtl_qty_param(self):
        # 验收单表体更新数量参数
        return self.cfg.get('RECEIPT_DATE_PARAMS', 'update_dtl_qty_param')