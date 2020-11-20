from tool.configparser_paternal import ConfigParserPaternal


class DataDistApprovalParm(ConfigParserPaternal):

    # 初始化所有ini配置文件字段
    def __init__(self):
        ConfigParserPaternal.__init__(self)
        # 读取配置文件参数
        self.cfg.read('..\\data_param_ini\\data_dist_approval_ini.ini', encoding='utf-8')

    # 新增配送审批单单号
    def get_dis_approval_num_id(self):
        return self.cfg.get('DIST_APPROVAL', 'dist_approval_num_id')

    # 新增配送审批单单头入参
    def get_dis_approval_hdr_param(self):
        return self.cfg.get('DIST_APPROVAL', 'dist_approval_hdr_param')

    # 获取配送商品件装数
    def get_dis_approval_item_conversion_qty_param(self):
        return self.cfg.get('DIST_APPROVAL', 'get_dis_approval_item_conversion_qty_param')

    # 新增配送审批单表体入参
    def get_dist_approval_dtl_param(self):
        return self.cfg.get('DIST_APPROVAL', 'dist_approval_dtl_param')

    # 新增配送审批单单据审核
    def get_dist_approval_audit_param(self):
        return self.cfg.get('DIST_APPROVAL', 'dist_approval_audit_param')
