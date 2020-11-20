import datetime
import time

import requests
import json
from get_data_param.data_dist_approval_param import DataDistApprovalParm
from get_data_param.data_pysql_param import DataPysql
from get_data_param.data_request_parm import DataRequest
from tool.pysql_connection_test import py_mysql
from tool.update_ini_test import Update


class CreateDistApproval:
    update = Update()
    data_dist_approval = DataDistApprovalParm()
    file_pysql = "..\\data_param_ini\\data_pysql_ini.ini"
    file_request = "..\\data_param_ini\\data_request_ini.ini"
    file_dist_approval = "..\\data_param_ini\\data_dist_approval_ini.ini"
    file_so_num = "..\\data_param_ini\\data_so_num_id_ini.ini"

    # 写入配送审批单号到配置文件
    def __write_dist_approval_reserved(self):
        self.update.update_ini('DATA', 'method', 'gb.core.sequence.client.series.newGet', self.file_request)
        self.update.update_ini('DATA', 'params', '{"series_name":"scm_bl_dist_approval_hdr_approval_num_id"}', self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        reserved = req.json()
        self.update.update_ini('DIST_APPROVAL', 'dist_approval_num_id', str(reserved['sequence_num']), self.file_dist_approval)
        return reserved['sequence_num']

    # 获取配送审批单号
    @staticmethod
    def __dist_approval_num_id():
        data_dist_approval = DataDistApprovalParm()
        dist_approval_num_id = data_dist_approval.get_dis_approval_num_id()
        return dist_approval_num_id

    @staticmethod
    # 获取当前时间后指定天数的日期时间
    def __get_delivery_date(effective_days):
        today = datetime.datetime.now().replace(hour=23, minute=59, second=59)
        date_time = today + datetime.timedelta(days=effective_days - 1)
        delivery_date = str(date_time)[0:19]
        return delivery_date

    # 创建配送审批单表头
    def create_dist_approval_hdr(self):
        storage_num_id = input('请输入配送逻辑仓：')
        settlement_type = input('请输入商品结算方式：')
        dist_approval_param = json.loads(self.data_dist_approval.get_dis_approval_hdr_param())
        dist_approval_param['approval_num_id'] = self.__write_dist_approval_reserved()
        dist_approval_param['order_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        dist_approval_param['settlement_type'] = settlement_type
        dist_approval_param['storage_num_id'] = storage_num_id
        dist_approval_param['effective_days'] = 7
        dist_approval_param['delivery_date'] = self.__get_delivery_date(7)
        dist_approval_param['user_num_id'] = str(10369)
        dist_approval_param['remark'] = "测试单据"
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.dist.approval.hdr.save', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps(dist_approval_param), self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('新增配送审批单%s,单号:%s' % (req.json()['message'], dist_approval_param['approval_num_id']))

    # 获取配送审批单商品件装数
    def __get_item_conversion_qty(self, sub_unit_num_id, item_num_id):
        dis_approval_conversion_qty_param = json.loads(self.data_dist_approval.get_dis_approval_item_conversion_qty_param())
        dis_approval_conversion_qty_param['order_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        dis_approval_conversion_qty_param['sub_unit_num_id'] = sub_unit_num_id
        dis_approval_conversion_qty_param['barcode'] = item_num_id
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.distribution.product.get', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps(dis_approval_conversion_qty_param), self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        if len(req.json()['data']) == 0:
            print(req.json()['message'])
            return False
        else:
            return req.json()['data'][0]['conversion_qty']

    # 创建配送审批单表体
    def create_dist_approval_dtl(self):
        while True:
            sub_unit_num_id = input('请输入配送门店编码:')
            item_num_id = input('请输入商品编码:')
            package_qty = input('请输入商品配送件数:')
            conversion_qty = self.__get_item_conversion_qty(sub_unit_num_id, item_num_id)
            if conversion_qty:
                dist_approval_dtl_param = json.loads(self.data_dist_approval.get_dist_approval_dtl_param())
                dist_approval_dtl_param['package_qty'] = package_qty
                dist_approval_dtl_param['item_num_id'] = item_num_id
                dist_approval_dtl_param['approval_num_id'] = self.__dist_approval_num_id()
                dist_approval_dtl_param['ord_sub_unit_num_id'] = sub_unit_num_id
                dist_approval_dtl_param['qty'] = int(package_qty) * int(conversion_qty)
                # 获取当天时间
                dist_approval_dtl_param['order_date'] = str(datetime.datetime.now())[0:10]
                self.update.update_ini('DATA', 'method', 'ykcloud.scm.dist.approval.dtl.save', self.file_request)
                self.update.update_ini('DATA', 'params', json.dumps(dist_approval_dtl_param), self.file_request)
                data_rquest = DataRequest()
                req = requests.post(data_rquest.get_data()['url'], data_rquest.get_data())
                print('保存:%s,行号:%s' % (req.json()["message"], req.json()["series"]))
            a = input('是否退出录入，输入数字 "1" 退出录入，"2" 继续录入:')
            if int(a) == 1:
                break

    # 配送审批单审核
    def dist_approval_audit(self):
        dist_approval_audit_param = json.loads(self.data_dist_approval.get_dist_approval_audit_param())
        dist_approval_audit_param['approval_num_id'] = self.__dist_approval_num_id()
        dist_approval_audit_param['user_num_id'] = str(10369)
        dist_approval_audit_param['sub_unit_num_id'] = str(100049)
        dist_approval_audit_param['order_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
        dist_approval_audit_param['auto_audit_sign'] = 0
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.distribution.approval.order.by.buyer.audit', self.file_request)
        self.update.update_ini('DATA', 'params', json.dumps(dist_approval_audit_param), self.file_request)
        data_request = DataRequest()
        req = requests.post(data_request.get_data()['url'], data_request.get_data())
        print('单据审核中……')
        time.sleep(5)
        print('单据:%s审核:%s' % (dist_approval_audit_param['approval_num_id'], req.json()["message"]))

    # 写入so单号到配置文件
    def write_so_num_ids(self):
        list_so_num_ids = []
        self.update.update_ini('MYSQL_DATA', 'db', 'SUPPLYCHAIN', self.file_pysql)
        dist_approval_num_id = self.__dist_approval_num_id()
        data_pysql = DataPysql()
        sql_select1 = "select distinct so_num_id from scm_bl_dist_approval_dtl where approval_num_id =  " + str(dist_approval_num_id)
        so_num_ids = list(py_mysql(data_pysql.get_pysqldata(), sql_select1))
        for i in so_num_ids:
            time.sleep(2)
            list_so_num_ids.append(i[0])
        print('生成的so单:%s' % (str(list_so_num_ids)))
        self.update.update_ini('SO_NUM_IDS', 'so_num_ids', str(list_so_num_ids), self.file_dist_approval)
        # 把生成的so单号写入so配置文件中
        self.update.update_ini('SO_NUM_ID_PARAM', 'ps_so_num_id', str(list_so_num_ids), self.file_so_num)
        self.update.update_ini('SO_NUM_ID_PARAM', 'so_num_id_list', str(list_so_num_ids), self.file_so_num)
