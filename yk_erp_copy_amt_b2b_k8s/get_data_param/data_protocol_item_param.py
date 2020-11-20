from tool.configparser_paternal import ConfigParserPaternal


class DataMdm(ConfigParserPaternal):

    # 初始化所有ini配置文件字段
    def __init__(self):
        ConfigParserPaternal.__init__(self)
        # 读取配置文件参数
        self.supply_param = {}
        self.cfg.read('..\\data_param_ini\\data_protocol_item_ini.ini', encoding='utf-8')

    # 供应商信息
    def get_supply_info(self):
        # 采购协议供应商信息
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
