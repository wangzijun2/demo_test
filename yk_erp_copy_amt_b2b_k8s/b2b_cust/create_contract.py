import datetime
import json
import requests
from tool.update_ini_test import Update
from get_data_param.data_request_parm import DataRequest
from get_data_param.data_b2b_contract_param import DataContractParm


class CreateContract:
    update = Update()
    # 请求参数配置文件
    file_request = "..\\data_param_ini\\data_request_ini.ini"
    # b2b客户参数配置文件
    file_cust_unit_params = "..\\data_param_ini\\data_b2b_cust_contract_ini.ini"

    # 新增b2b销售合同做单单号
    def create_contract_reserved_no(self):
        self.update.update_ini('DATA', 'method', 'gb.core.sequence.client.series.newGet', self.file_request)
        self.update.update_ini('DATA', 'params', '{"series_name":"scm_bl_contract_apply_reserved_no"}',
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        reserved = req.json()
        # 写入b2b客户单号到参数配置文件中
        # print(reserved)
        self.update.update_ini('CONTRACT_DATA', 'contract_reserved_no', str(reserved['sequence_num']),
                               self.file_cust_unit_params)
        return reserved['sequence_num']

    # 查询客户cust信息1(查询cust客户信息）
    def select_cust_param_1(self):
        # 定义客户信息参数返回标识
        cust_results_param = {}
        cust_unit_id = input('请输入客户编号：')
        self.update.update_ini('DATA', 'method', 'gb.cexport.data.export', self.file_request)
        self.update.update_ini('DATA', 'params',
                               '{"sql_id":"YKERP-B2B-1000","on_line":true,"input_param":{"unit_num_id":' + cust_unit_id + '},"page_num":1,"page_size":1000}',
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        # 获取客户信息明细
        cust_results = req.json()['results'][0]
        # cust_results_param.append(cust_results['cort_name'])
        # 客户结算编号
        cust_results_param['cort_num_id'] = cust_results['cort_num_id']
        # 客户编号
        cust_results_param['unit_num_id'] = cust_results['unit_num_id']
        # 客户等级
        cust_results_param['cus_level'] = cust_results['cus_level']
        # 客户区域
        cust_results_param['cus_area'] = cust_results['cus_area']
        # 客户分类
        cust_results_param['cus_category'] = cust_results['cus_category']
        # 客户 结算方式(实销实结，日结，周结，月结)
        cust_results_param['settlement_cycle'] = cust_results['settlement_cycle']
        # 客户名称
        cust_results_param['unit_name'] = cust_results['unit_name']
        return cust_results_param

    # 查询客户cort信息2(客户cort信息)
    def select_cust_param_2(self):
        cust_results_param = self.select_cust_param_1()
        self.update.update_ini('DATA', 'method', 'gb.cexport.data.export', self.file_request)
        self.update.update_ini('DATA', 'params',
                               '{"sql_id":"YKERP-SCM-SALE-CONTRACT-CORT","on_line":true,"input_param":'
                               '{"cort_num_id":' + str(
                                   cust_results_param['cort_num_id']) + '},"page_num":1,"page_size":0}',
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        # 添加核算公司
        cust_results_param['cort_name'] = req.json()['results'][0]['cort_name']
        return cust_results_param

    # b2b销售合同保存
    def save_contract(self):
        head_sub_unit_num_id = input("请输入销售合同绑定的总部编码：\n")
        # 获取b2b客户信息
        cust_param_dict = self.select_cust_param_2()
        # 获取b2b销售合同保存入参
        contract_param = json.loads(DataContractParm().return_contract_param())
        # 更新入参，获取销售合同做单单号
        contract_param['reserved_no'] = self.create_contract_reserved_no()
        # 更新当前日期
        contract_param['make_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        contract_param['begin_day'] = datetime.datetime.now().strftime('%Y-%m-%d')
        # 获取当前后一年日期
        contract_param['end_day'] = str(datetime.datetime.now() + datetime.timedelta(365))[0:10]
        # 获取输入的总部编码
        contract_param['head_sub_unit_num_id'] = head_sub_unit_num_id
        # 是否信用管控
        contract_param['is_credit'] = 1
        # 销售合同做单单号
        contract_param['reserved_id'] = contract_param['reserved_no']
        # 客户核算公司
        contract_param['cus_cort_name'] = cust_param_dict['cort_name']
        # 客户名称
        contract_param['cus_unit_name'] = cust_param_dict['unit_name']
        # 客户核算编号
        contract_param['cus_cort_num_id'] = cust_param_dict['cort_num_id']
        # 客户编号
        contract_param['cus_unit_num_id'] = cust_param_dict['unit_num_id']
        # 客户 结算方式(实销实结，日结，周结，月结), 默认写死为2 日结，付款方式默认为现金
        contract_param['settlement_cycle'] = 2
        # 客户等级 默认带出客户值，接口不做修改
        contract_param['cus_level'] = cust_param_dict['cus_level']
        # 客户区域
        contract_param['cus_area'] = cust_param_dict['cus_area']
        # 客户分类
        contract_param['cus_category'] = cust_param_dict['cus_category']
        # 物理合同默认写死为客户名称
        contract_param['reserved_physical_id'] = cust_param_dict['unit_name']
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.supply.b2b.contract.save', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps(contract_param, ensure_ascii=False), self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('新增销售合同:', req.json()['message'], '销售合同单号:', contract_param['reserved_no'])
        # 更新b2b客户编码到配置文件中
        self.update.update_ini('CONTRACT_DATA', 'login_name_unit_num_id', str(cust_param_dict['unit_num_id']),
                               self.file_cust_unit_params)

    # 制单审核
    def zd_contract_audit(self):
        contract_reserved_no = DataContractParm().return_contract_reserved()
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.b2b.contract.status.update', self.file_request)
        self.update.update_ini('DATA', 'params',
                               json.dumps(
                                   {"reserved_no": str(contract_reserved_no), "status_num_id": 6, "user_num_id": 1}),
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('销售合同制单审核:', req.json()['message'], '合同单号:', contract_reserved_no)

    # 业务审核
    def yw_contract_audit(self):
        contract_reserved_no = DataContractParm().return_contract_reserved()
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.b2b.contract.status.update', self.file_request)
        self.update.update_ini('DATA', 'params',
                               json.dumps({"reserved_no": str(contract_reserved_no), "status_num_id": 2,
                                           "user_num_id": 1}),
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('销售合同业务审核:', req.json()['message'], '合同单号:', contract_reserved_no)

    # 财务审核
    def cw_contract_audit(self):
        contract_reserved_no = DataContractParm().return_contract_reserved()
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.b2b.supply.contract.audit', self.file_request)
        self.update.update_ini('DATA', 'params',
                               json.dumps({"user_num_id": 1, "reserved_no": str(contract_reserved_no)}),
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('销售合同业务审核:', req.json()['message'], '合同单号:', contract_reserved_no)

    # 建立b2b销售合同账号
    def create_contract_user(self):
        unit_num_user = DataContractParm().return_unit_num_id()
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.supply.account.create', self.file_request)
        self.update.update_ini('DATA', 'params',
                               json.dumps({"user_num_id": 1, "main_org": "/机构/客户", "phone": "null",
                                           "email": "null", "login_name": unit_num_user, "name": "test客户1051",
                                           "unit_num_id": unit_num_user}, ensure_ascii=False),
                               self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('销售合同建立账号:', req.json()['message'], '登录账号:', 's' + unit_num_user)
