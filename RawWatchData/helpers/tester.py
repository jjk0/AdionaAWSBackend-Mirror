from datetime import timedelta
from tracemalloc import start
from dateutil import parser
import time 

start_time = parser.parse('2022-06-12T07:25:00Z')
print("raw time", start_time)

unix_time_milli = time.mktime(start_time.timetuple())*1000
unix_time = time.mktime(start_time.timetuple())

print("unix time", unix_time)
print("unix time milli", unix_time_milli)


# time_val = 10
# freq = 5
# # diff = timedelta(milliseconds=time_val/freq)
# diff = time_val/freq*1000
# print("differences", diff, type(diff))
# print(diff + unix_time)