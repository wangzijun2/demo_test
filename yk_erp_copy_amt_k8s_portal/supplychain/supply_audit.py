import datetime
import json
import time
import requests
from get_data_param.data_approval_param import DataApprovalParm
from get_data_param.data_pysql_param import DataPysql
from get_data_param.data_request_parm import DataRequest
from tool.update_ini_test import Update
from tool.pysql_connection_test import py_mysql
from get_data_param.data_supply_aduit_param import DataSupplyAuditParam


class SupplyAudit:
    update = Update()
    data_approval = DataApprovalParm()
    file_pysql = "..\\data_param_ini\\data_pysql_ini.ini"
    file_request = "..\\data_param_ini\\data_request_ini.ini"
    file_supply = "..\\data_param_ini\\data_supply_audit_ini.ini"
    file_receipt = "..\\data_param_ini\\data_receipt_num_id_ini.ini"
    update.update_ini('MYSQL_DATA', 'db', 'SUPPLYCHAIN', file_pysql)
    data_pysql = DataPysql()

    # 把采购单号写入ini配置文件

    def __write_po_num_id(self):
        # 存放采购单号
        global return_values
        list_values = []
        # self.update.update_ini('MYSQL_DATA', 'db', 'SUPPLYCHAIN', self.file_pysql)
        approval_num_id = self.data_approval.return_approval_num_id()
        count = 0
        # 循环3秒查询是否生成了采购单号
        while count < 3:
            sql = "select DISTINCT po_num_id from scm_bl_approval_dtl where approval_num_id = " + approval_num_id
            return_values = py_mysql(self.data_pysql.get_pysqldata(), sql)
            time.sleep(1)
            count += 1
        for i in range(len(return_values)):
            list_values.append(list(return_values[i])[0])
        print(list_values)
        if len(list_values) > 0:
            self.update.update_ini('GET_PO_NIM_ID', 'po_num_id', str(list_values), self.file_supply)
            print("订货审批单:", approval_num_id, "写入采购单号:", list_values)
            return True
        else:
            print("订货审批单%s,未查询到对于的采购单号" % approval_num_id)
            return False

    # 返回采购单号
    @staticmethod
    def __return_po_num_id():
        data = DataSupplyAuditParam()
        return list(eval(data.return_po_num_id()))

    # 供应商确认
    def __api_auto_po_num_id(self, list_po_num_id):
        # 供应商确认时间（当天）
        sup_produce_date = str(datetime.datetime.now())[0:10]
        sub_num_id_list = []
        order_date_list = []
        data_approval = DataApprovalParm()
        data_supply = DataSupplyAuditParam()
        logistics_type = eval(data_approval.get_approval_hdr())['logistics_type']
        # 获取供应商确认入参
        sup_po_dtl_params = eval(data_supply.get_auto_sup_po_dtl())
        self.update.update_ini('DATA', 'method', 'ykcloud.scm.purchase.order.delivery.date.confirm', self.file_request)
        for i in range(len(list_po_num_id)):
            sql_select1 = "select distinct sub_unit_num_id from scm_bl_po_sup_dtl where po_num_id = " + str(
                list_po_num_id[i])
            sql_select2 = "select distinct order_date from scm_bl_po_sup_dtl where po_num_id = " + str(
                list_po_num_id[i])
            sub_num_id_list.append(py_mysql(self.data_pysql.get_pysqldata(), sql_select1))
            order_date_list.append(py_mysql(self.data_pysql.get_pysqldata(), sql_select2))
            # 查询采购单号对应的门店和创建日期
            sub_num_id_list[i] = sub_num_id_list[i][0][0]
            order_date_list[i] = order_date_list[i][0][0].strftime("%Y-%m-%d")
        # 当订货审批单是直送的情况
        if logistics_type == '1':
            # 循环请求采购单确认接口
            for i in range(len(sub_num_id_list)):
                sup_po_dtl_params['user_num_id'] = 10369
                sup_po_dtl_params['sub_unit_num_id'] = sub_num_id_list[i]
                sup_po_dtl_params['po_num_id'] = list_po_num_id[i]
                sup_po_dtl_params['order_date'] = order_date_list[i]
                sup_po_dtl_params['sup_confirm_date'] = sup_produce_date
                # print(json.dumps(sup_po_dtl_params),type(sup_po_dtl_params))
                self.update.update_ini('DATA', 'params', json.dumps(sup_po_dtl_params), self.file_request)
                # 每次跟新请求入参都需要重新读取请求参数配置文件
                data_request = DataRequest()
                req = requests.post(data_request.get_data()['url'], data_request.get_data())
                print('采购单号:', list_po_num_id[i], '供应商确认接口返回:', req.json()['message'])
                time.sleep(1)
        # 当订货审批单是直通的情况
        if logistics_type == '2':
            for i in range(len(list_po_num_id)):
                sup_po_dtl_params['user_num_id'] = 10369
                sup_po_dtl_params['sub_unit_num_id'] = 100049
                sup_po_dtl_params['po_num_id'] = list_po_num_id[i]
                sup_po_dtl_params['order_date'] = order_date_list[0]
                sup_po_dtl_params['sup_confirm_date'] = sup_produce_date
                self.update.update_ini('DATA', 'params', json.dumps(sup_po_dtl_params), self.file_request)
                # 每次跟新请求入参都需要重新读取请求参数配置文件
                data_request = DataRequest()
                req = requests.post(data_request.get_data()['url'], data_request.get_data())
                print('采购单号:', list_po_num_id[i], '供应商确认接口返回:', req.json()['message'])
                time.sleep(1)
        # 验收单写入配置文件
        self.write_receipt_num_id()
        return True

    # 更新待供应商确认的数量和时间
    def auto_po_num_id(self):
        # 写入采购单成功后进行供应商确认操作
        if self.__write_po_num_id():
            # self.update.update_ini('MYSQL_DATA', 'db', 'SUPPLYCHAIN', self.file_pysql)
            # 获取采购单号
            list_po_num_id = self.__return_po_num_id()
            if list_po_num_id != 0:
                # 供应商确认时间（当天）
                sup_produce_date = str(datetime.datetime.now())[0:10]
                list_data = []
                for i in range(len(list_po_num_id)):
                    sql_select = "select series,qty from scm_bl_po_sup_dtl where po_num_id = " + str(list_po_num_id[i]) + " limit 10000"
                    # 查询采购单下单数量
                    list_data.append(py_mysql(self.data_pysql.get_pysqldata(), sql_select))
                # series值：list_data[0][0][0] qty值：list_data[0][0][1]，循环取值更新确认数量
                for i in range(len(list_data)):
                    for j in range(len(list_data[0])):
                        series = list_data[i][j][0]
                        sup_confirm_total_qty = list_data[i][j][1]
                        sql_update1 = "update scm_bl_po_sup_dtl set sup_confirm_total_qty = " + str(
                            sup_confirm_total_qty) + " where series = " + str(series)
                        sql_update2 = "update scm_bl_po_sup_dtl set sup_produce_date = " + "'" + sup_produce_date + "'" + " where series = " + str(
                            series)
                        # 使用update语句更新采购单数量和确认生产日期
                        py_mysql(self.data_pysql.get_pysqldata(), sql_update1)
                        py_mysql(self.data_pysql.get_pysqldata(), sql_update2)
                        print('对应的series:', series, '供应商确认数量更新成功:', sup_confirm_total_qty, '生产日期更新为:',
                              "'" + sup_produce_date + "'")
            self.__api_auto_po_num_id(list_po_num_id)
        else:
            print("该订货审批单未查询到采购单！")

    # 验收单写入配置文件
    def write_receipt_num_id(self):
        self.update.update_ini('MYSQL_DATA', 'db', 'LOGISTICS', self.file_pysql)
        data_pysql = DataPysql()
        # 用来存放验收单号
        po_num_id_list = list(self.__return_po_num_id())
        print('po_num_id', po_num_id_list)
        receipt_list = []
        for i in po_num_id_list:
            sql_select = "select reserved_no from wm_bl_receipt_bud_hdr where po_num_id = " + str(i)
            receipt_hdr_list = py_mysql(data_pysql.get_pysqldata(), sql_select)
            receipt_list.append(receipt_hdr_list[0][0])
        self.update.update_ini('RECEIPT_DATE_PARAMS', 'receipt_num_id', str(receipt_list), self.file_receipt)
        print('写入验收单配置文件:', receipt_list)
