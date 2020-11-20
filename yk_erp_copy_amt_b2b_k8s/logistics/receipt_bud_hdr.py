import time
import requests
import json
from get_data_param.data_approval_param import DataApprovalParm
from get_data_param.data_pysql_param import DataPysql
from get_data_param.data_receipt_param import DataReceipt
from get_data_param.data_request_parm import DataRequest
from get_data_param.data_supply_aduit_param import DataSupplyAuditParam
from tool.pysql_connection_test import py_mysql
from tool.update_ini_test import Update


class SelectReceiptHdr:
    update = Update()
    data_supplyaduit = DataSupplyAuditParam()
    data_approval = DataApprovalParm()
    data_receipt = DataReceipt()
    file_pysql = "..\\data_param_ini\\data_pysql_ini.ini"
    file_request = "..\\data_param_ini\\data_request_ini.ini"
    file_receipt = "..\\data_param_ini\\data_receipt_num_id_ini.ini"
    file_so_num = "..\\data_param_ini\\data_so_num_id_ini.ini"
    # 切换连接的数据库
    update.update_ini('MYSQL_DATA', 'db', 'LOGISTICS', file_pysql)
    data_pysql = DataPysql()


    # 返回验收单号
    @staticmethod
    def __return_receipt_num_id():
        data_receipt = DataReceipt()
        receipt_num_id = list(eval(data_receipt.return_receipt_num_id()))
        return receipt_num_id

    # 更新验收单商品数量
    def update_item_num_qty(self):
        # 存储验收单参数
        receipt_bud_dtl = []
        receipt_num_id = self.__return_receipt_num_id()
        for i in range(len(receipt_num_id)):
            # 循环查询每个验收单门店和验收单体数量
            sql_select1 = "select reserved_no,series,item_num_id,sup_produce_date,package_qty,qty,sub_unit_num_id from wm_bl_receipt_bud_dtl where  reserved_no = " + str(
                receipt_num_id[i]) + " limit 2000"
            receipt_bud_dtl.append((list(py_mysql(self.data_pysql.get_pysqldata(), sql_select1))))
        # 进行验收操作
        for i in range(len(receipt_bud_dtl)):
            for j in range(len(receipt_bud_dtl[i])):
                # 验收单receipt_bud_dtl[i][j][0],表体series receipt_bud_dtl[i][j][1],商品编码receipt_bud_dtl[i][j][2],
                # 确认日期receipt_bud_dtl[i][j][3],件数receipt_bud_dtl[i][j][4],确认数量receipt_bud_dtl[i][j][5]
                # 验收门店receipt_bud_dtl[i][j][6]
                # 获取更新验收单表体参数
                update_receipt_qty_param = eval(self.data_receipt.get_update_dtl_qty_param())
                update_receipt_qty_param['user_num_id'] = 10369
                update_receipt_qty_param['sub_unit_num_id'] = receipt_bud_dtl[i][j][6]
                update_receipt_qty_param['reserved_no'] = receipt_bud_dtl[i][j][0]
                receipt_dtl_infos_list = update_receipt_qty_param['receipt_dtl_infos_list'][0]
                receipt_dtl_infos_list['series'] = receipt_bud_dtl[i][j][1]
                receipt_dtl_infos_list['item_num_id'] = receipt_bud_dtl[i][j][2]
                receipt_dtl_infos_list['sup_produce_date'] = receipt_bud_dtl[i][j][3]
                receipt_dtl_infos_list['package_qty'] = str(receipt_bud_dtl[i][j][4])
                receipt_dtl_infos_list['confirm_all_qty'] = str(receipt_bud_dtl[i][j][5])
                self.update.update_ini('DATA', 'method', 'ykcloud.wm.receipt.updateConfirmallqty', self.file_request)
                # list格式转化为json格式  json.dumps(update_receipt_qty_param)
                self.update.update_ini('DATA', 'params', json.dumps(update_receipt_qty_param), self.file_request)
                data_request = DataRequest()
                req = requests.post(data_request.get_data()['url'], data_request.get_data())
                print('验收单号:', receipt_bud_dtl[i][j][0], '表体对应的series:', receipt_bud_dtl[i][j][1], '验收单数量保存:',
                      req.json()['message'])

    # 验收单收货
    def receipt_finish(self):
        list_data = []
        receipt_num_ids = self.__return_receipt_num_id()
        self.update.update_ini('DATA', 'method', 'ykcloud.wm.receipt.finish', self.file_request)
        logistics_type = eval(self.data_approval.get_approval_hdr())['logistics_type']
        receipt_num_dtl_params = eval(self.data_receipt.get_receipt_num_hdr_params())
        # 查询验收单的门店
        for i in range(len(receipt_num_ids)):
            sql_select = "select  reserved_no,sub_unit_num_id from wm_bl_receipt_bud_hdr where reserved_no =" + str(
                receipt_num_ids[i])
            list_data.append(py_mysql(self.data_pysql.get_pysqldata(), sql_select))
            receipt_num_dtl_params['reserved_no'] = list_data[i][0][0]
            receipt_num_dtl_params['sub_unit_num_id'] = list_data[i][0][1]
            self.update.update_ini('DATA', 'params', json.dumps(receipt_num_dtl_params), self.file_request)
            data_request = DataRequest()
            # 设置2秒延迟，等待采购单确认状态完成
            time.sleep(2)
            req = requests.post(data_request.get_data()['url'], data_request.get_data())
            print('验收单:', list_data[i][0][0], '门店:', list_data[i][0][1], '全部收货:', req.json()['message'])
        # 如果商品物流方式为直通查询发货单并更新到so参数配置文件中
        if logistics_type == "2" :
            # 获取配置表中的so_list
            so_num_id_list_1 = []
            # 存放获取的so_list
            so_num_id_list_2 = []
            self.update.update_ini('MYSQL_DATA', 'db', 'TENANORD', self.file_pysql)
            data_pysql = DataPysql()
            sql_select = "select distinct so_num_id from sd_bl_so_hdr where apply_num_id =" + str(receipt_num_ids[0])
            so_num_id_list_1.append(list(py_mysql(data_pysql.get_pysqldata(), sql_select)))
            for i in range(len(so_num_id_list_1[0])):
                # 获取直通单据验收单产生的发货单
                so_num_id_list_2.append(so_num_id_list_1[0][i][0])
            if so_num_id_list_2:
                self.update.update_ini('SO_NUM_ID_PARAM', 'zt_so_num_id', str(so_num_id_list_2), self.file_so_num)
                self.update.update_ini('SO_NUM_ID_PARAM', 'so_num_id_list', str(so_num_id_list_2), self.file_so_num)
                print('验收单:%s产生发货单如下:%s' % (receipt_num_ids[0], so_num_id_list_2))

        '''
        if logistics_type == '2':
            sub_unit_num_ids =[]
            for i in range(len(receipt_num_ids)):
                sql_select1 = "select distinct sub_unit_num_id from wm_bl_receipt_bud_hdr where reserved_no =" + str(receipt_num_ids[i])
                sub_unit_num_ids.append(PySql.py_mysql(data,sql_select1))
            for j in range(len(sub_unit_num_ids)):
                if sub_unit_num_ids[j][0][0]==100049:
                    for i in range(len(receipt_num_ids)):
                        sql_select2 = "select distinct reserved_no,sub_unit_num_id from wm_bl_receipt_bud_dtl where reserved_no ="+ str(receipt_num_ids[i])
                        list_data.append(PySql.py_mysql(data,sql_select2))
                        receipt_num_dtl_params['reserved_no'] = list_data[i][0][0]
                        receipt_num_dtl_params['sub_unit_num_id'] = 100049
                        self.update.update_ini('DATA','params',json.dumps(receipt_num_dtl_params))
                        data = Data()
                        req = requests.post(data.data['url'],data.data)
                        print('验收单:',list_data[i][0][0],'门店:',100049,'全部收货:',req.json()['message'])
            '''

