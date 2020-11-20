import pymysql


# from后面接的是文件目录 import后面接的是类
# from get_data_param.get_data_param import Data


def py_mysql(data, sql):
    try:
        # mysql连接参数
        db = pymysql.connect(data['host'], data['user'], data['passwd'], data['db'], data['port'])
    # 捕获数据库连接超时异常问题
    except pymysql.connections.err.OperationalError:
        # 重新连接
        db = pymysql.connect(data['host'], data['user'], data['passwd'], data['db'], data['port'])
    # 获取游标
    cursor = db.cursor()
    # 执行SQL语句
    cursor.execute(sql)
    # 获取sql执行的结果(fetchall()获取全部返回行，fetchone()返回多行)
    data_param = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 提交到数据库执行
    db.commit()
    # 返回结果
    # 关闭mysql连接
    db.close()
    return data_param