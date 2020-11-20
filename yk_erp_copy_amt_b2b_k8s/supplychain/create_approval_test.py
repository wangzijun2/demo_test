import datetime
import json
import time
import requests
from get_data_param.data_param import DataParm
from mdm.create_protocol_item_test import CreateProtocolItem
from tool.pysql_connection import py_mysql
from tool.update_ini import Update


class CreateApproval:
    update = Update()

    # 写入订货审批单号到配置文件
    def write_approval_reserved(self):
        self.update.update_ini('DATA', 'method', 'gb.core.sequence.client.series.newGet')
        self.update.update_ini('DATA', 'params', '{"series_name":"scm_bl_approval_hdr_approval_num_id"}')
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        approval_num_id = req.json()['sequence_num']
        self.update.update_ini('APPROVAL', 'approval_num_id', str(approval_num_id))
        return approval_num_id

    # 返回采购订货审批单号
    @staticmethod
    def get_approval_num_id():
        data = DataParm()
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
        logistics_type = input('请输入采购订单表头物流方式：1表示直送，2表示直通:')
        now_date = datetime.datetime.now().strftime('%Y-%m-%d')
        approval_num_id = self.get_approval_num_id()
        supply_info = CreateProtocolItem().get_supply_info()
        data = DataParm()
        approval_hdr_params = eval(data.get_approval_hdr())
        approval_hdr_params['approval_num_id'] = approval_num_id
        approval_hdr_params['supply_unit_num_id'] = supply_info['supply_unit_num_id']
        approval_hdr_params['settlement_type'] = supply_info['settlement_type']
        approval_hdr_params['begin_day'] = supply_info['begin_day'][0:10]
        approval_hdr_params['end_day'] = supply_info['end_day'][0:10]
        approval_hdr_params['order_date'] = now_date
        approval_hdr_params['delivery_date'] = self.get_seven_day()
        approval_hdr_params['remark'] = 'test-demo'
        approval_hdr_params['user_num_id'] = 10369
        approval_hdr_params['logistics_type'] = logistics_type
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.approval.hdr.save')
        self.update.update_ini('DATA', 'params', json.dumps(approval_hdr_params))
        # 把表头的物流方式写入配置文件
        self.update.update_ini('APPROVAL', 'logistics_type', logistics_type)
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        print('采购订货审批单表头保存:', req.json()['message'], '，表头单号:', approval_num_id)
        return logistics_type

    # 获取商品件装数
    def get_approval_item_conversion_qty(self, sub_unit_num_id, item_num_id):
        data = DataParm()
        approval_item_conversion_qty_param = json.loads(data.get_approval_item_conversion_qty_param())
        approval_item_conversion_qty_param['sub_unit_num_id'] = sub_unit_num_id
        approval_item_conversion_qty_param['barcode'] = item_num_id
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.hand.replenish.product.get')
        self.update.update_ini('DATA', 'params', json.dumps(approval_item_conversion_qty_param))
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        if len(req.json()['data']) < 1:
            print(req.json()['message'])
            return False
        else:
            return req.json()['data'][0]['conversion_qty']

    # 采购订货审批单表体保存
    def save_approval_dtl(self):
        approval_num_id = self.get_approval_num_id()
        data = DataParm()
        count = 0
        logistics_type = data.get_logistics_type()
        approval_dtl_params = eval(data.get_approval_dtl())
        item_num_id_list = list(eval(data.return_item_num_id_list()))
        sub_unit_num_ids = list(eval(data.get_sub_unit_num_ids()))
        approval_dtl_params['approval_num_id'] = approval_num_id
        approval_dtl_params['order_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        approval_dtl_params['user_num_id'] = 10369
        # 表头物流方式为直送，走门店直送还是大仓自采
        if logistics_type == '1':
            logistics_sign = input('是否选择大仓自采/门店直送：1表示大仓自采，2表示门店直送:')
            # 大仓自采（大仓直送）
            if logistics_sign == str(1):
                for i in range(len(item_num_id_list)):
                    package_qty = input('请输入%s的商品配送件数:' % item_num_id_list[i])
                    conversion_qty = self.get_approval_item_conversion_qty(100049, item_num_id_list[i])
                    if conversion_qty:
                        approval_dtl_params['item_num_id'] = item_num_id_list[i]
                        approval_dtl_params['ord_sub_unit_num_id'] = 100049
                        approval_dtl_params['package_qty'] = int(package_qty)
                        approval_dtl_params['qty'] = int(package_qty) * int(conversion_qty)
                        self.update.update_ini('DATA', 'method', 'ykcloud.scm.approval.dtl.save')
                        self.update.update_ini('DATA', 'params', json.dumps(approval_dtl_params))
                        data = DataParm()
                        req = requests.post(data.get_data()['url'], data.get_data())
                        print('商品:', item_num_id_list[i], '门店:', 100049, '保存:', req.json()['message'], 'series行号:',
                              req.json()['series'])
            # 门店直送
            if logistics_sign == str(2):
                zs_sum_max = input('请输入订货审批单直送门店类型批量商品件数：')
                for i in range(len(item_num_id_list)):
                    approval_dtl_params['item_num_id'] = item_num_id_list[i]
                    for j in range(len(sub_unit_num_ids)):
                        conversion_qty = self.get_approval_item_conversion_qty(sub_unit_num_ids[j], item_num_id_list[i])
                        if conversion_qty:
                            approval_dtl_params['ord_sub_unit_num_id'] = sub_unit_num_ids[j]
                            approval_dtl_params['package_qty'] = int(zs_sum_max)
                            approval_dtl_params['qty'] = int(zs_sum_max) * int(conversion_qty)
                            self.update.update_ini('DATA', 'method', 'ykcloud.scm.approval.dtl.save')
                            self.update.update_ini('DATA', 'params', json.dumps(approval_dtl_params))
                            data = DataParm()
                            req = requests.post(data.get_data()['url'], data.get_data())
                            count = count + 1
                            print('商品:', item_num_id_list[i], '门店:', sub_unit_num_ids[j], '保存:', req.json()['message'],
                                  'series行号:', req.json()['series'])
        # 物流方式为直通
        if logistics_type == '2':
            zt_sum_max = input('请输入订货审批单直通到店类型批量到店商品件数：')
            for i in range(len(item_num_id_list)):
                approval_dtl_params['item_num_id'] = item_num_id_list[i]
                for j in range(len(sub_unit_num_ids)):
                    conversion_qty = self.get_approval_item_conversion_qty(sub_unit_num_ids[j], item_num_id_list[i])
                    if conversion_qty:
                        approval_dtl_params['package_qty'] = int(zt_sum_max)
                        approval_dtl_params['qty'] = int(zt_sum_max) * int(conversion_qty)
                        approval_dtl_params['ord_sub_unit_num_id'] = sub_unit_num_ids[j]
                        self.update.update_ini('DATA', 'method', "ykcloud.scm.approval.dtl.save")
                        self.update.update_ini('DATA', 'params', json.dumps(approval_dtl_params))
                        data = DataParm()
                        req = requests.post(data.get_data()['url'], data.get_data())
                        count = count + 1
                        print('商品:', item_num_id_list[i], '门店:', sub_unit_num_ids[j], '保存:', req.json()['message'],
                              'series行号:', req.json()['series'])

    # 采购订货审批单审核
    def approval_audit(self):
        approval_params = {}
        data = DataParm()
        approval_num_id = self.get_approval_num_id()
        approval_params['sub_unit_num_id'] = 100049
        approval_params['order_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        approval_params['approval_num_id'] = approval_num_id
        approval_params['logistics_type'] = data.get_logistics_type()
        approval_params['auto_audit_sign'] = 0
        approval_params['user_num_id'] = 10369
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.approval.order.by.buyer.audit')
        self.update.update_ini('DATA', 'params', json.dumps(approval_params))
        data = DataParm()
        req = requests.post(data.get_data()['url'], data.get_data())
        print('单据:%s审核:%s' % (approval_num_id, req.json()['message']))

    # 把采购单号写入ini配置文件
    def write_po_num_id(self):
        # 存放采购单号
        list_values = []
        self.update.update_ini('MYSQL_DATA', 'db', 'SUPPLYCHAIN')
        data = DataParm()
        approval_num_id = data.return_approval_num_id()
        # 循环查询是否生成了采购单号
        while True:
            time.sleep(1)
            sql = "select DISTINCT po_num_id from scm_bl_approval_dtl where approval_num_id = " + approval_num_id
            return_values = py_mysql(data, sql)
            if len(return_values) > 0:
                for i in range(len(return_values)):
                    list_values.append(list(return_values[i])[0])
                    self.update.update_ini('GET_PO_NIM_ID', 'po_num_id', str(list_values))
                print("订货审批单:", approval_num_id, "写入采购单号:", list_values)
                break

    # 返回采购单号
    @staticmethod
    def return_po_num_id():
        data = DataParm()
        po_num_id = list(eval(data.return_po_num_id()))
        return po_num_id


# c = CreateApproval()
# c.write_approval_reserved()
# c.create_approval_hdr()
# c.save_approval_dtl()
# c.approval_audit()
# c.write_po_num_id()
