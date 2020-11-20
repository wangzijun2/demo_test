from tool.configparser_paternal import ConfigParserPaternal


class DataSupplyAuditParam(ConfigParserPaternal):

    # 初始化所有ini配置文件字段
    def __init__(self):
        ConfigParserPaternal.__init__(self)
        # 读取配置文件参数
        self.cfg.read('..\\data_param_ini\\data_supply_audit_ini.ini', encoding='utf-8')

    def return_po_num_id(self):
        # 采购订单单号
        return self.cfg.get('GET_PO_NIM_ID', 'po_num_id')

    def get_auto_sup_po_dtl(self):
        # 供应商确认参数
        return self.cfg.get('AUTO_SUP_PO_DTL', 'params')