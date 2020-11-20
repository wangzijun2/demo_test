import datetime
import json
import requests
from mdm.create_protocal_item import CreateProtocolItem
from tool.update_ini_test import Update
from get_data_param.data_approval_param import DataApprovalParm
from get_data_param.data_request_parm import DataRequest
from get_data_param.data_protocol_item_param import DataMdm


class CreateApproval:
    update = Update()
    # 请求参数配置文件
    file_request = "..\\data_param_ini\\data_request_ini.ini"
    # 订货审批单参数配置文件
    file_approval = "..\\data_param_ini\\data_approval_ini.ini"

    # 写入订货审批单号到配置文件
    def write_approval_reserved(self):
        self.update.update_ini('DATA', 'method', 'gb.core.sequence.client.series.newGet', self.file_request)
        self.update.update_ini('DATA', 'params', '{"series_name":"scm_bl_approval_hdr_approval_num_id"}',
                               self.file_request)
        data = DataRequest()
        req = requests.post(data.get_data()['url'], data.get_data())
        # print(req.json())
        approval_num_id = req.json()['sequence_num']
        # print(approval_num_id)
        self.update.update_ini('APPROVAL', 'approval_num_id', str(approval_num_id), self.file_approval)
        # return approval_num_id

    # 返回采购订货审批单号
    @staticmethod
    def get_approval_num_id():
        data = DataApprovalParm()
        approval_num_id = data.return_approval_num_id()
        return approval_num_id

    # 获取当前时间后七天的日期时间
    @staticmethod
    def get_seven_day():
        today = datetime.datetime.now().replace(hour=23, minute=59, second=59)
        seven_day = today + datetime.timedelta(days=7 - 1)
        seven_day = str(seven_day)[0:19]
        return seven_day

    # 采购订货审批单表头保存
    def create_approval_hdr(self):
        self.write_approval_reserved()
        logistics_type = input('请输入采购订单表头物流方式：1表示直送，2表示直通:')
        now_date = datetime.datetime.now().strftime('%Y-%m-%d')
        approval_num_id = self.get_approval_num_id()
        supply_info = CreateProtocolItem().get_supply_info()
        data = DataApprovalParm()
        approval_hdr_params = eval(data.get_approval_hdr())
        sub_unit_num_id = input("请输入订货门店:")
        approval_hdr_params['approval_num_id'] = approval_num_id
        approval_hdr_params['sub_unit_num_id'] = sub_unit_num_id
        approval_hdr_params['supply_unit_num_id'] = supply_info['supply_unit_num_id']
        approval_hdr_params['settlement_type'] = supply_info['settlement_type']
        approval_hdr_params['begin_day'] = supply_info['begin_day'][0:10]
        approval_hdr_params['end_day'] = supply_info['end_day'][0:10]
        approval_hdr_params['order_date'] = now_date
        approval_hdr_params['delivery_date'] = self.get_seven_day()
        approval_hdr_params['remark'] = 'test-demo'
        approval_hdr_params['user_num_id'] = 1
        approval_hdr_params['logistics_type'] = logistics_type
        # 更新总部字段到配置文件
        self.update.update_ini('APPROVAL', 'sub_unit_num_id', str(sub_unit_num_id), self.file_approval)
        # 分配方式字段
        # if logistics_type == '1':
        #     approval_hdr_params['so_from_type'] = 3
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.approval.hdr.save', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps(approval_hdr_params), self.file_request)
        # 把表头的物流方式写入配置文件
        self.update.update_ini('APPROVAL', 'logistics_type', logistics_type, self.file_approval)
        self.update.update_ini('APPROVAL', 'approval_hdr_param', json.dumps(approval_hdr_params), self.file_approval)
        data = DataRequest()
        req = requests.post(data.get_data()['url'], data.get_data())
        print('采购订货审批单表头保存:', req.json()['message'], '，表头单号:', approval_num_id)

    # 获取商品件装数
    def get_approval_item_conversion_qty(self, sub_unit_num_id, item_num_id):
        data = DataApprovalParm()
        approval_item_conversion_qty_param = json.loads(data.get_approval_item_conversion_qty_param())
        approval_item_conversion_qty_param['sub_unit_num_id'] = sub_unit_num_id
        approval_item_conversion_qty_param['barcode'] = item_num_id
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.hand.replenish.product.get', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps(approval_item_conversion_qty_param), self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        if len(req.json()['data']) < 1:
            print('补货查询商品信息报错：' + req.json()['message'])
            return False
        else:
            return req.json()['data'][0]['conversion_qty']

    # 采购订货审批单表体保存
    def save_approval_dtl(self):
        approval_num_id = self.get_approval_num_id()
        data_approval = DataApprovalParm()
        # data_protocol = DataMdm()
        # count = 0
        logistics_type = data_approval.get_logistics_type()
        # 获取配置保存表体参数
        approval_dtl_params = json.loads(data_approval.get_approval_dtl())
        # 获取采购协议的商品和门店
        # item_num_id_list = list(eval(data_protocol.return_item_num_id_list()))
        # sub_unit_num_ids = list(eval(data_protocol.get_sub_unit_num_ids()))
        approval_dtl_params['approval_num_id'] = approval_num_id
        approval_dtl_params['order_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        approval_dtl_params['user_num_id'] = 1
        # 表头物流方式为直送，走门店直送还是大仓自采
        if logistics_type == '1':
            sub_unit_num_id = data_approval.get_sub_unit_num_id()
            logistics_sign = input('是否选择大仓自采/门店直送：1表示大仓自采，2表示门店直送:')
            # 大仓自采（大仓直送）
            if logistics_sign == str(1):
                while True:
                    item_num_id_list = input("请输入要补货的商品编码（输入0表示退出补货）:")
                    if item_num_id_list == '0':
                        break
                    package_qty = input('请输入%s的商品配送件数:' % item_num_id_list)
                    conversion_qty = self.get_approval_item_conversion_qty(sub_unit_num_id, item_num_id_list)
                    if conversion_qty:
                        approval_dtl_params['item_num_id'] = item_num_id_list
                        approval_dtl_params['ord_sub_unit_num_id'] = sub_unit_num_id
                        approval_dtl_params['sub_unit_num_id'] = sub_unit_num_id
                        approval_dtl_params['package_qty'] = int(package_qty)
                        approval_dtl_params['conversion_qty'] = conversion_qty
                        approval_dtl_params['qty'] = int(package_qty) * int(conversion_qty)
                        self.update.update_ini('DATA', 'method', 'ykcloud.scm.approval.dtl.save', self.file_request)
                        self.update.update_ini('DATA', 'params', json.dumps(approval_dtl_params, ensure_ascii=False),
                                               self.file_request)
                        data_request = DataRequest()
                        req = requests.post(data_request.get_data()['url'], data_request.get_data())
                        print('商品:', item_num_id_list, '门店:', sub_unit_num_id, '保存:', req.json()['message'],
                              'series行号:',
                              req.json()['series'])
            else:
                print("暂不支持")

        #     # 门店直送
        #     if logistics_sign == str(2):
        #         zs_sum_max = input('请输入订货审批单直送门店类型批量商品件数：')
        #         for i in range(len(item_num_id_list)):
        #             approval_dtl_params['item_num_id'] = item_num_id_list[i]
        #             for j in range(len(sub_unit_num_ids)):
        #                 conversion_qty = self.get_approval_item_conversion_qty(sub_unit_num_ids[j], item_num_id_list[i])
        #                 if conversion_qty:
        #                     approval_dtl_params['ord_sub_unit_num_id'] = sub_unit_num_ids[j]
        #                     approval_dtl_params['package_qty'] = int(zs_sum_max)
        #                     approval_dtl_params['qty'] = int(zs_sum_max) * int(conversion_qty)
        #                     self.update.update_ini('DATA', 'method', 'ykcloud.scm.approval.dtl.save', self.file_request)
        #                     self.update.update_ini('DATA', 'params', json.dumps(approval_dtl_params), self.file_request)
        #                     data_request = DataRequest()
        #                     req = requests.post(data_request.get_data()['url'], data_request.get_data())
        #                     count = count + 1
        #                     print('商品:', item_num_id_list[i], '门店:', sub_unit_num_ids[j], '保存:', req.json()['message'],
        #                           'series行号:', req.json()['series'])
        # # 物流方式为直通
        # if logistics_type == '2':
        #     zt_sum_max = input('请输入订货审批单直通到店类型批量到店商品件数：')
        #     for i in range(len(item_num_id_list)):
        #         approval_dtl_params['item_num_id'] = item_num_id_list[i]
        #         for j in range(len(sub_unit_num_ids)):
        #             conversion_qty = self.get_approval_item_conversion_qty(sub_unit_num_ids[j], item_num_id_list[i])
        #             if conversion_qty:
        #                 approval_dtl_params['package_qty'] = int(zt_sum_max)
        #                 approval_dtl_params['qty'] = int(zt_sum_max) * int(conversion_qty)
        #                 approval_dtl_params['ord_sub_unit_num_id'] = sub_unit_num_ids[j]
        #                 self.update.update_ini('DATA', 'method', "ykcloud.scm.approval.dtl.save", self.file_request)
        #                 self.update.update_ini('DATA', 'params', json.dumps(approval_dtl_params), self.file_request)
        #                 data_request = DataRequest()
        #                 req = requests.post(data_request.get_data()['url'], data_request.get_data())
        #                 count = count + 1
        #                 print('商品:', item_num_id_list[i], '门店:', sub_unit_num_ids[j], '保存:', req.json()['message'],
        #                       'series行号:', req.json()['series'])

    # 采购订货审批单审核
    def approval_audit(self):
        approval_params = {}
        data_approval = DataApprovalParm()
        approval_num_id = self.get_approval_num_id()
        approval_params['sub_unit_num_id'] = data_approval.get_sub_unit_num_id()
        approval_params['order_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        approval_params['approval_num_id'] = approval_num_id
        approval_params['logistics_type'] = data_approval.get_logistics_type()
        approval_params['auto_audit_sign'] = 0
        approval_params['user_num_id'] = 1
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.approval.order.by.buyer.audit', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps(approval_params), self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('单据:%s 审核:%s' % (approval_num_id, req.json()['message']))
