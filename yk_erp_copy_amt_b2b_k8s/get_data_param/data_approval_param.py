from tool.configparser_paternal import ConfigParserPaternal


class DataApprovalParm(ConfigParserPaternal):

    # 初始化所有ini配置文件字段
    def __init__(self):
        ConfigParserPaternal.__init__(self)
        # 读取配置文件参数
        self.cfg.read('..\\data_param_ini\\data_approval_ini.ini', encoding='utf-8')

    # 返回订货审批单单号
    def return_approval_num_id(self):
        return self.cfg.get('APPROVAL', 'approval_num_id')

    # 订货审批单表头
    def get_approval_hdr(self):
        return self.cfg.get('APPROVAL', 'approval_hdr_param')

    # 获取订货审批单件数
    def get_approval_item_conversion_qty_param(self):
        return self.cfg.get('APPROVAL', 'get_approval_item_conversion_qty_param')

    # 订货审批单表体
    def get_approval_dtl(self):
        return self.cfg.get('APPROVAL', 'approval_dtl_param')

    # 订货审批单物物流方式
    def get_logistics_type(self):
        return self.cfg.get('APPROVAL', 'logistics_type')

    # 获取订货审批单表头门店
    def get_sub_unit_num_id(self):
        return self.cfg.get('APPROVAL', 'sub_unit_num_id')
