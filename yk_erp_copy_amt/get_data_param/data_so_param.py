from tool.configparser_paternal import ConfigParserPaternal


class DataSoParam(ConfigParserPaternal):

    # 初始化所有ini配置文件字段
    def __init__(self):
        ConfigParserPaternal.__init__(self)
        # 读取配置文件参数
        self.cfg.read('..\\data_param_ini\\data_so_num_id_ini.ini', encoding='utf-8')

    def return_so_num_id(self):
        # 获取so单号
        return self.cfg.get('SO_NUM_ID_PARAM', 'so_num_id_list')

    def get_so_dtl_update_qty(self):
        # 更新so单表体数量
        return self.cfg.get('SO_NUM_ID_PARAM', 'so_num_id_update_qty_param')

    def get_so_finish(self):
        # so发货入参
        return self.cfg.get('SO_NUM_ID_PARAM', 'so_finish_param')