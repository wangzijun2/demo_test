import json
import requests
from tool.update_ini_test import Update
from get_data_param.data_request_parm import DataRequest
from get_data_param.data_b2b_cust_param import DataCustParm


class CreateCustUnit:
    update = Update()
    # 请求参数配置文件
    file_request = "..\\data_param_ini\\data_request_ini.ini"
    # b2b客户参数配置文件
    file_cust_unit_params = "..\\data_param_ini\\data_b2b_cust_unit_ini.ini"

    # 获取b2b客户做单单号并写入配置文件
    def get_cust_unit_reserved_no(self):
        self.update.update_ini('DATA', 'method', 'gb.core.sequence.client.series.newGet', self.file_request)
        self.update.update_ini('DATA', 'params', '{"series_name":"mdms_bl_cust_unit_reserved_no"}',
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        reserved = req.json()
        # 写入b2b客户单号到参数配置文件中
        # print(reserved)
        self.update.update_ini('CUST_DATA', 'cust_unit_reserved_no', str(reserved['sequence_num']),
                               self.file_cust_unit_params)
        return reserved['sequence_num']

    # 获取b2b客户cort_num_id
    def get_cust_unit_no(self):
        self.update.update_ini('DATA', 'method', 'ykcloud.md.automic.sequence.get', self.file_request)
        self.update.update_ini('DATA', 'params', '{"series_name":"auto_mdms_o_unit_unit_num_id"}',
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        reserved = req.json()
        return reserved['sequence_num']

    # 获取b2b客户cort_num_id
    def get_cust_cort_no(self):
        self.update.update_ini('DATA', 'method', 'ykcloud.md.automic.sequence.get', self.file_request)
        self.update.update_ini('DATA', 'params', '{"series_name":"auto_mdms_o_cort_cort_num_id"}',
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        reserved = req.json()
        return reserved['sequence_num']

    # 保存b2b客户信息
    def save_cust_unit(self):
        # 获取cust保存信息 str格式转为dist格式
        cust_unit_param = json.loads(DataCustParm().return_cust_unit_params())
        cust_unit_param['reserved_no'] = self.get_cust_unit_reserved_no()
        cust_unit_param['theme'] = '新增' + str(cust_unit_param['reserved_no'])
        cust_unit_param['unit_num_id'] = self.get_cust_unit_no()
        cust_unit_param['cort_num_id'] = self.get_cust_cort_no()
        cust_unit_param['unit_name'] = 'test客户' + str(cust_unit_param['unit_num_id'])
        cust_unit_param['cort_name'] = 'test核算公司' + str(cust_unit_param['cort_num_id'])
        cust_unit_param['user_num_id'] = 1
        cust_unit_param['cus_name'] = 'test联系人'
        cust_unit_param['legal_behf'] = 'test法人'
        self.update.update_ini('DATA', 'method', 'ykcloud.md.cust.unit.save', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps(cust_unit_param), self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('新增客户:', req.json()['message'], ', 客户编号:', cust_unit_param['unit_num_id'],
              '单据号:', cust_unit_param['reserved_no'])
        # 更新b2b客户参数信息到配置文件
        self.update.update_ini('CUST_DATA', 'params', json.dumps(cust_unit_param ,ensure_ascii=False),
                               self.file_cust_unit_params)

    # 业务审核
    def yw_cust_unit_audit(self):
        # 获取客户做单编号
        reserved_no = DataCustParm().return_cust_unit_reserved_no()
        self.update.update_ini('DATA', 'method', 'ykcloud.md.cust.unit.confirm', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps({"reserved_no": str(reserved_no), "user_num_id": 1}),
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('业务审核:', req.json()['message'])

    # 财务审核
    def cw_cust_unit_audit(self):
        # 获取客户做单编号
        reserved_no = DataCustParm().return_cust_unit_reserved_no()
        self.update.update_ini('DATA', 'method', 'ykcloud.md.cust.unit.audit', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps({"reserved_no": str(reserved_no), "user_num_id": 1}),
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('财务审核:', req.json()['message'])
