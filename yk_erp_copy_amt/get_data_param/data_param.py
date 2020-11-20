import configparser


class DataParm:
    # 定义读取配置文件数据
    cfg = configparser.ConfigParser()
    # 传参data
    data = {}
    # 采购协议供应商信息
    supply_param = {}
    # 供应商确认参数
    auto_sup_po_dtl = {}
    # 验收单号
    receipt_num_id = []
    # 验收单表头收货参数
    receipt_num_hdr_params = {}
    # 验收单表体更新数量参数
    update_dtl_qty_param = {}
    # so单号保存
    so_num_id = []

    # 初始化所有ini配置文件字段
    def __init__(self):
        # 读取配置文件参数
        self.cfg.read('..\\data_ini.ini')
        # Py_sql连接
        self.host = self.cfg.get('MYSQL_DATA', 'host')
        self.user = self.cfg.get('MYSQL_DATA', 'user')
        self.passwd = self.cfg.get('MYSQL_DATA', 'passwd')
        self.db = self.cfg.get('MYSQL_DATA', 'db')
        self.port = self.cfg.getint('MYSQL_DATA', 'port')

    # api接口入参
    def get_data(self):
        self.data['url'] = self.cfg.get('DATA', 'url')
        self.data['method'] = self.cfg.get('DATA', 'method')
        self.data['params'] = self.cfg.get('DATA', 'params')
        self.data['app_key'] = self.cfg.getint('DATA', 'app_key')
        self.data['convert_flag'] = self.cfg.get('DATA', 'convert_flag')
        return self.data

    # 供应商信息
    def get_supply_info(self):
        self.supply_param['supply_unit_num_id'] = self.cfg.get('GET_SUPPLY_INFO', 'supply_unit_num_id')
        self.supply_param['begin_day'] = self.cfg.get('GET_SUPPLY_INFO', 'begin_day')
        self.supply_param['end_day'] = self.cfg.get('GET_SUPPLY_INFO', 'end_day')
        self.supply_param['settlement_type'] = self.cfg.get('GET_SUPPLY_INFO', 'settlement_type')
        return self.supply_param

    # 采购协议表体
    def get_protocol_info(self):
        return self.cfg.get('PROTOCOL_DTL', 'params')

    # 执行机构(新增协议添加的门店)
    def get_sub_unit_num_ids(self):
        return self.cfg.get('ADD_SUB_ID', 'sub_unit_num_ids')

    # 获取采购协议单号
    def get_protocol_num(self):
        return self.cfg.get('GET_RESERVED', 'protocol_num_id')

    # 单个商品id
    def get_item_num_id(self):
        return self.cfg.get('GET_RESERVED', 'item_num_id')

    # 商品列表list
    def return_item_num_id_list(self):
        return self.cfg.get('GET_RESERVED', 'item_num_id_list')

    # 商品款式id列表
    def get_style_num_id(self):
        return self.cfg.get('PROTOCOL_DTL', 'style_num_id')

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

    # 采购订单单号
    def return_po_num_id(self):
        return self.cfg.get('GET_PO_NIM_ID', 'po_num_id')

    # 供应商确认参数
    def get_auto_sup_po_dtl(self):
        self.auto_sup_po_dtl = self.cfg.get('AUTO_SUP_PO_DTL', 'params')
        return self.auto_sup_po_dtl

    # 验收单单号
    def return_receipt_num_id(self):
        self.receipt_num_id = self.cfg.get('RECEIPT_NUM_ID', 'receipt_num_id')
        return self.receipt_num_id

    # 验收单表头收货参数
    def get_receipt_num_hdr_params(self):
        self.receipt_num_hdr_params = self.cfg.get('RECEIPT_DATL_PARAMS', 'receipt_num_hdr_params')
        return self.receipt_num_hdr_params

    # 验收单表体更新数量参数
    def get_update_dtl_qty_param(self):
        self.update_dtl_qty_param = self.cfg.get('RECEIPT_DATL_PARAMS', 'update_dtl_qty_param')
        return self.update_dtl_qty_param

    def get_so_num_ids(self):
        # so单号列表
        self.so_num_id = self.cfg.get('SO_NUM_ID', 'so_num_id')
        return self.so_num_id

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

