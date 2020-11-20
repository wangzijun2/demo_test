import datetime
import json
import requests
from dateutil.relativedelta import relativedelta
from get_data_param.data_request_parm import DataRequest
from tool.update_ini_test import Update
from get_data_param.data_supply_create_param import SupplyCreateParam


class CreateSupplyUnit:
    supply_reserved = ''
    supply_unit_id = ''
    update = Update()
    # 请求参数配置文件
    file_request = "..\\data_param_ini\\data_request_ini.ini"
    # 采购合同参数配置文件
    file_protocol_item = "..\\data_param_ini\\data_create_supply_ini.ini"

    # 获取采购合同单号
    def get_supply_reserved(self):
        self.update.update_ini('DATA', 'method', 'gb.core.sequence.client.series.newGet', self.file_request)
        self.update.update_ini('DATA', 'params', '{"series_name":"scm_bl_contract_apply_reserved_no"}',
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        reserved = req.json()['sequence_num']
        self.supply_reserved = reserved
        # return reserved

    # 获取供应商单号
    def get_supply_unit_id(self):
        self.update.update_ini('DATA', 'method', 'ykcloud.md.automic.sequence.get', self.file_request)
        self.update.update_ini('DATA', 'params', '{"series_name":"auto_mdms_o_unit_unit_num_id"}',
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        reserved = req.json()['sequence_num']
        self.supply_unit_id = reserved
        # return reserved

    # 获取采购合同表体信息
    def get_supply_unit_id_param(self):
        self.get_supply_reserved()
        self.get_supply_unit_id()
        supply_name = input("请输入供应商合同名称：")
        data = SupplyCreateParam()
        supply_data_param = data.return_supply_contract_save_param()
        # 把str类型的json转为dict类型
        supply_data_param = json.loads(supply_data_param)
        supply_data_param['reserved_no'] = self.supply_reserved
        supply_data_param['batch_no'] = self.supply_reserved
        supply_data_param['supply_unit_num_id'] = self.supply_unit_id
        supply_data_param['contract_name'] = supply_name
        supply_data_param['supply_unit_name'] = supply_name
        # 获取当前年月日
        supply_data_param['begin_day'] = datetime.datetime.now().strftime('%Y-%m-%d')
        supply_data_param['make_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        # 获取当前时间后一年日期
        supply_data_param['end_day'] = (datetime.datetime.now() - relativedelta(years=-1)).strftime('%Y-%m-%d')
        supply_data_param['make_empe_num_id'] = 1
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.supply.contract.save', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps(supply_data_param),
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('新增合同' + req.json()['message'] + '合同编号：' + str(supply_data_param['reserved_no'])
              , '供应商编码：' + str(self.supply_unit_id))


c = CreateSupplyUnit()
c.get_supply_unit_id_param()
