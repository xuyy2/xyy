# coding:utf-8
import calendar

import datetime

month = 1
for month in range(1, 13):
    print(month)
    monthRange = calendar.monthrange(2018, month)
    print("%d 月有%d天" % (monthRange[0], monthRange[1]))
    month += 1
