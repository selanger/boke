import calendar
import datetime
now = datetime.datetime.now()

year = now.year
month = now.month
last_day = calendar.monthrange(year,month)[1]   ## 最后一天
## 拼接
start = datetime.date(year,month,1)
print (start)

end = datetime.date(year,month,last_day)
print (end)

## 转date


a = {"name":"hello","age":19}
print ("namename" in a.keys())
a = {"name":5,"age":19,"name3":26,"age3":3,"name4":26}
#  找到最大的value
## 找到对应的key

b=[]
for key,value in a.items():
    if value==max(a.values()):
        print(key,value)
        b.append(key)














