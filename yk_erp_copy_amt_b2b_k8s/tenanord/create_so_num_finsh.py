import json
import time
import requests
from get_data_param.data_pysql_param import DataPysql
from get_data_param.data_request_parm import DataRequest
from get_data_param.data_so_param import DataSoParam
from tool.pysql_connection_test import py_mysql
from tool.update_ini_test import Update


class SoFinish:
    update = Update()
    data_so_param = DataSoParam()
    file_pysql = "..\\data_param_ini\\data_pysql_ini.ini"
    file_request = "..\\data_param_ini\\data_request_ini.ini"
    file_so_num = "..\\data_param_ini\\data_so_num_id_ini.ini"
    file_receipt_num = "..\\data_param_ini\\data_receipt_num_id_ini.ini"
    # 先更新数据库
    update.update_ini('MYSQL_DATA', 'db', 'TENANORD', file_pysql)
    data_pysql = DataPysql()

    # so更新表体数量
    def update_so_dtl_qty(self):
        # 定义存放so表体栏位信息
        so_num_id_list = []
        # 定义存放so单表体的列表
        so_um_id_dtls = []
        so_dtl_update_qty_param = eval(self.data_so_param.get_so_dtl_update_qty())
        # 存放获取的so列表
        so_num_ids = eval(self.data_so_param.return_so_num_id())
        # 根据对应的so查询对于的商品并更新数量
        for i in range(len(so_num_ids)):
            sql_select2 = "select so_num_id,series,item_num_id,lock_qty,packing_qty from sd_bl_so_dtl where so_num_id = " + str(
                so_num_ids[i])
            so_um_id_dtls.append(list(py_mysql(self.data_pysql.get_pysqldata(), sql_select2)))
        for i in range(len(so_um_id_dtls)):
            # 单独添加到so_num_id_list列表中
            so_num_id_list.append(so_um_id_dtls[i][0][0])
            for j in range(len(so_um_id_dtls[i])):
                # so单号
                so_dtl_update_qty_param['so_num_id'] = so_um_id_dtls[i][j][0]
                # so单体series号
                so_dtl_update_qty_param['so_dtl_info_list'][0]['series'] = so_um_id_dtls[i][j][1]
                # item_num_id编码
                so_dtl_update_qty_param['so_dtl_info_list'][0]['item_num_id'] = so_um_id_dtls[i][j][2]
                # 商品锁库数
                so_dtl_update_qty_param['so_dtl_info_list'][0]['lock_qty'] = str(so_um_id_dtls[i][j][3])
                # 商品装箱数
                so_dtl_update_qty_param['so_dtl_info_list'][0]['packing_qty'] = str(so_um_id_dtls[i][j][3])
                self.update.update_ini('DATA', 'method', 'ykcloud.so.packing.qty.update', self.file_request)
                self.update.update_ini('DATA', 'params', json.dumps(so_dtl_update_qty_param), self.file_request)
                data_request = DataRequest()
                req = requests.post(data_request.get_data()['url'], data_request.get_data())
                print('对应发货单号: %s' % so_um_id_dtls[i][j][0] + '单体数量保存:', req.json()['message'])

    # so批量发货
    def so_finish(self):
        so_num_ids = eval(self.data_so_param.return_so_num_id())
        self.update.update_ini('DATA', 'method', 'ykcloud.wm.ship.so.finish', self.file_request)
        so_finish_param = eval(self.data_so_param.get_so_finish())
        for i in so_num_ids:
            time.sleep(2)
            so_finish_param['so_num_id'] = i
            self.update.update_ini('DATA', 'params', json.dumps(so_finish_param), self.file_request)
            data_request = DataRequest()
            req = requests.post(data_request.get_data()['url'], data_request.get_data())
            print('对应发货单号:%s' % i, '发货:%s' % req.json()['message'])

    # 发货后查询下级门店验收单，并写入到验收单配置文件
    def select_next_receipt_num_id(self):
        self.update.update_ini('MYSQL_DATA', 'db', 'LOGISTICS', self.file_pysql)
        data_pysql = DataPysql()
        next_receipt_num_id = []
        so_num_ids = eval(self.data_so_param.return_so_num_id())
        for i in so_num_ids:
            time.sleep(3)
            sql_select = " select receipt_no from wm_bl_ship_hdr where so_num_id =" + str(i)
            next_receipt_num_id.append(list(py_mysql(data_pysql.data, sql_select)[0])[0])
        self.update.update_ini('RECEIPT_DATE_PARAMS', 'next_receipt_num_ids', str(next_receipt_num_id), self.file_receipt_num)
        self.update.update_ini('RECEIPT_DATE_PARAMS', 'receipt_num_id', str(next_receipt_num_id), self.file_receipt_num)
        print('下级验收单:%s' % next_receipt_num_id)
