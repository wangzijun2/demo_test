import requests
from get_data_param.data_param import DataParm
from tool.update_ini import Update
import json


class CreateProtocolItem:
    update = Update()

    # 获取采购协议单号
    def __get_reserved(self):
        self.update.update_ini('DATA', 'method', 'gb.core.sequence.client.series.newGet')
        self.update.update_ini('DATA', 'params', '{"series_name":"scm_bl_protocol_reserved_no"}')
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        reserved = req.json()
        self.update.update_ini('GET_RESERVED', 'protocol_num_id', str(reserved['sequence_num']))
        return reserved['sequence_num']

    # 返回采购协议单号
    @staticmethod
    def return_protocol_num():
        data = DataParm()
        reserved_no = data.get_protocol_num()
        return reserved_no

    # 获取商品id
    def __get_item_num_id(self):
        self.update.update_ini('DATA', 'method', 'ykcloud.md.automic.sequence.get')
        self.update.update_ini('DATA', 'params', '{"series_name":"auto_mdms_p_product_basic_item_num_id"}')
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        item_num_id = req.json()['sequence_num']
        # 商品编码写入配置文件，方便获取商品条码
        self.update.update_ini('GET_RESERVED', 'item_num_id', str(item_num_id))
        return item_num_id

    # 获取商品款式style_id
    def __get_item_style_id(self):
        self.update.update_ini('DATA', 'method', 'ykcloud.md.automic.sequence.get')
        self.update.update_ini('DATA', 'params', '{"series_name":"auto_mdms_p_product_style_style_num_id"}')
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        item_style_id = req.json()['sequence_num']
        return item_style_id

    # 返回单个商品
    @staticmethod
    def return_item_num_id():
        data = DataParm()
        item_num_id = data.get_item_num_id()
        return item_num_id

    # 获取商品barcode
    def __get_item_barcode(self):
        params = {}
        item_num_id = self.return_item_num_id()
        params['item_num_id'] = item_num_id
        params['barcode_type'] = 1
        self.update.update_ini('DATA', 'method', 'ykcloud.prd.barcode.generate')
        self.update.update_ini('DATA', 'params', json.dumps(params))
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        barcode = req.json()
        return barcode['barcode']

    # 获取供应商信息
    def get_supply_info(self):
        supply_unit_num_id = input('请输入供应商:')
        self.update.update_ini('DATA', 'method', 'gb.cexport.data.export')
        # 代销供应商 3101000 购销供应商 3101052/3101233
        self.update.update_ini('DATA', 'params',
                               '{"sql_id":"YKERP-SCM-0238","on_line":true,"input_param":{"supply_unit_num_id":' + supply_unit_num_id + ',"privilege_flag":0 },"page_num":1,"page_size":0}')
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        supply_info = req.json()['results'][0]
        return supply_info

    # 保存采购协议表头
    def save_supply_hdr(self):
        # 采购协议单号
        reserved_no = self.__get_reserved()
        # 保存采购协议表头
        supply_info = self.get_supply_info()
        self.update.update_ini('GET_SUPPLY_INFO', 'supply_unit_num_id', str(supply_info['supply_unit_num_id']))
        self.update.update_ini('GET_SUPPLY_INFO', 'settlement_type', str(supply_info['settlement_type']))
        self.update.update_ini('GET_SUPPLY_INFO', 'supply_unit_name', str(supply_info['supply_unit_name']))
        self.update.update_ini('GET_SUPPLY_INFO', 'begin_day', str(supply_info['begin_day'])[0:10])
        self.update.update_ini('GET_SUPPLY_INFO', 'end_day', str(supply_info['end_day'])[0:10])
        data = DataParm()
        supply_param_dict = data.get_supply_info()
        supply_param_dict["reserved_no"] = str(reserved_no)
        supply_param_dict["user_num_id"] = str(10369)
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.bl.protocol.save')
        self.update.update_ini('DATA', 'params', json.dumps(supply_param_dict))
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        print('采购协议表头保存:', req.json()['message'], '，采购协议单号:', reserved_no)

    # 保存采购协议表体
    def save_supply_dtl(self):
        data = DataParm()
        count = 1
        item_num_id_list = []
        style_num_id_list = []
        max_count = input("请输入要新建商品的个数：")
        while count <= int(max_count):
            # 商品物流方式 1直送 2直通 3配送
            logistics_num_id = input("请输入该商品的物流方式：")
            if int(logistics_num_id) != 1 and int(logistics_num_id) != 2 and int(logistics_num_id) != 3:
                print("请输入正确的物流方式！")
                continue
            # 获取商品id
            item_num_id = self.__get_item_num_id()
            # 获取商品条码
            barcode = self.__get_item_barcode()
            # 获取款式id
            item_style_id = self.__get_item_style_id()
            # 获取商品和款式list
            item_num_id_list.append(item_num_id)
            style_num_id_list.append(item_style_id)
            # 获取采购协议表体入参
            protocol_dtl_info = data.get_protocol_info()
            # 字符串转为字典注意字符串里的格式
            protocol_dtl_info_dict = json.loads(protocol_dtl_info)
            # 传入单头，商品id/条码/名称
            protocol_dtl_info_dict['reserved_no'] = self.return_protocol_num()
            protocol_dtl_info_dict['save_bl_protocol_dtl_list'][0]['item_num_id'] = item_num_id
            protocol_dtl_info_dict['save_bl_protocol_dtl_list'][0]['barcode_1'] = barcode
            protocol_dtl_info_dict['save_bl_protocol_dtl_list'][0]['barcode1'] = barcode
            protocol_dtl_info_dict['save_bl_protocol_dtl_list'][0]['item_name'] = 'test' + str(item_num_id)
            protocol_dtl_info_dict['save_bl_protocol_dtl_list'][0]['sim_item_name'] = 'test' + str(item_num_id)
            protocol_dtl_info_dict['save_bl_protocol_dtl_list'][0]['logistics_num_id'] = str(logistics_num_id)
            protocol_dtl_info_dict['save_bl_protocol_dtl_list'][0]['style_num_id'] = str(item_style_id)
            # count计数累加
            count = count+1
            protocol_dtl_info_dict['user_num_id'] = 10369
            self.update.update_ini('DATA', 'method', 'ykcloud.scm.bl.protocol.dtl.save')
            self.update.update_ini('DATA', 'params', json.dumps(protocol_dtl_info_dict))
            data = DataParm()
            req = requests.post(data.get_data()['url'], data.get_data())
            print('采购协议表体保存:%s,商品编码:%s, 款式id:%s,物流方式:%s' %
                  (req.json()['message'], item_num_id, str(item_style_id), str(logistics_num_id)))
        self.update.update_ini('GET_RESERVED', 'item_num_id_list', str(item_num_id_list))
        self.update.update_ini('GET_RESERVED', 'style_num_id_list', str(style_num_id_list))

    # 添加执行机构
    def add_sub_unit(self):
        param = {}
        reserved_no = self.return_protocol_num()
        data = DataParm()
        sub_unit_num_ids = list(eval(data.get_sub_unit_num_ids()))
        param['reserved_no'] = reserved_no
        param['sub_unit_num_ids'] = sub_unit_num_ids
        param['user_num_id'] = 10369
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.bl.protocol.shop.save')
        self.update.update_ini('DATA', 'params', json.dumps(param))
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        print('添加执行机构:', req.json()['message'], '，添加有:', param['sub_unit_num_ids'])

    # 采购协议制单确认/业务审核/财务审核
    def zd_audit(self):
        param = {}
        reserved_no = self.return_protocol_num()
        param['reserved_no'] = str(reserved_no)
        param['user_num_id'] = 10369
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.bl.protocol.confirm')
        self.update.update_ini('DATA', 'params', json.dumps(param))
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        print('制单审核:', req.json()['message'], '，采购协议单号:', reserved_no)

    def yw_audit(self):
        param = {}
        reserved_no = self.return_protocol_num()
        param['reserved_no'] = str(reserved_no)
        param['user_num_id'] = 10369
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.protocol.bl.business.audit')
        self.update.update_ini('DATA', 'params', json.dumps(param))
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        print('业务审核:', req.json()['message'], '，采购协议单号:', reserved_no)

    def cw_audit(self):
        param = {}
        reserved_no = self.return_protocol_num()
        param['reserved_no'] = str(reserved_no)
        param['user_num_id'] = 10369
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.protocal.audit')
        self.update.update_ini('DATA', 'params', json.dumps(param))
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        print('财务审核:', req.json()['message'], '，采购协议单号:', reserved_no)
