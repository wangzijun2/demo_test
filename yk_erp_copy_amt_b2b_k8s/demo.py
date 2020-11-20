# list_dict = [{'company': '东方圆通', 'loan_num': 1, 'loan_money': 80}, {'company': '晋之政', 'loan_num': 1, 'loan_money': 85}, {'company': '荣盛金丰', 'loan_num': 1, 'loan_money': 67}]
#
# for i in list_dict:
#     print(i['company'])
#     print(i['loan_num'])
#     print(i['loan_money'])
# import datetime
#
#
# def get_seven_day():
#     # today = datetime.datetime.now().replace(hour=23, minute=59, second=59)
#     today = datetime.datetime.now()
#     print(today)
#     # seven_day = today + datetime.timedelta(days=7 - 1)
#     # seven_day = str(seven_day)[0:11]
#     # print(seven_day)
#     # return seven_day
# get_seven_day()

import datetime
from dateutil.relativedelta import relativedelta
d = datetime.datetime.now()
print((datetime.datetime.now() - relativedelta(years=-1)).strftime('%Y-%m-%d'))