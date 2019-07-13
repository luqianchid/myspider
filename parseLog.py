import re
import time
start = time.time()
Day = {}
Hour = {}
pattern = '''(?:\[(?P<datetime>[^\[\]]+)\])''' # 匹配 
# 计算小时
# with open('access.log.1',encoding='utf-8') as f: 
f = open('access.log.1',encoding='utf-8')
for line in f:
    log_hour = re.findall(pattern,line)[0][:14]
    if log_hour in Hour.keys():
        Hour[log_hour] += 1
    else:
        Hour.setdefault(log_hour,1)
print(Hour)
#计算日期
for i in Hour.keys():
    date = i.split(':')[0]
    if date in Day.keys():        
        Day[date] += Hour[i]
    else:
        Day.setdefault(date,Hour[i])
print(Day)
end = time.time()
print('%.2f'%(end-start))
