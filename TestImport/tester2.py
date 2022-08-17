from calendar import week
import datetime
from string import Template
import numpy

# data = {'hr': 
#   [
  #   '2022-07-11T10:30:25', 
  #  '2022-07-11T10:45:25', 
  #  '2022-07-14T10:00:25', 
  #  '2022-07-15T10:30:25', 
  #  '2022-07-20T10:00:25', 
  #  '2022-07-27T10:30:25', 
  #  '2022-07-30T10:00:25', 
  #  '2022-08-01T10:33:25', 
  #  '2022-08-04T10:47:25', 
  #  '2022-08-05T12:30:25', 
  #  '2022-08-05T12:30:25'
  #  ]
  # }

data = {"heart_rate": 
    {"value": [50,54,76,90,82,55,60,62,65], 
     "timestamps": [
       1658118642.0,
       1658507800.0,
       1659901000.0,
       1659902000.0,
       1659903000.0,
       1659904000.0,
       1659905000.0,
       1659906000.0,
       1659907000.0,
       1659907800.0
      ]
    }
}

# time frames 
current_time = datetime.datetime.now()
past_day_time = current_time - datetime.timedelta(hours=12)
past_two_days_time = current_time - datetime.timedelta(days=2)
past_week_time = current_time - datetime.timedelta(days=7)
past_month_time = current_time - datetime.timedelta(days=30)
# timeframes = [
#   current_time,
#   past_day_time,
#   past_two_days_time,
#   past_week_time,
#   past_month_time
# ]
past_day_time_array = []
past_two_days_array = []
past_week_array = []
past_months_array = [] 

# convert datetime unix strings to readable datetime object
datetime_timestamps = []
for unix in data['heart_rate']['timestamps']:
  str_datetime_obj = datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%dT%H:%M:%S')
  datetime_obj = datetime.datetime.strptime(str_datetime_obj, '%Y-%m-%dT%H:%M:%S')
  datetime_timestamps.append(datetime_obj)

dict_values = {}
for key in datetime_timestamps:
    for value in data['heart_rate']['value']:
        dict_values[key] = value
        data['heart_rate']['value'].remove(value)
        break  
  
print(dict_values)
# get all hr values in each time range  
def hr_in_range(beginning_window, ending_window):
  list = [] 
  for timestamp in dict_values.keys(): 
    if timestamp > beginning_window and timestamp <= ending_window:
      list.append(dict_values[timestamp])
  return list

hr_in_past_day_time = hr_in_range(
  past_day_time, 
  current_time, 
)

hr_in_past_two_days = hr_in_range(
  past_two_days_time, 
  current_time, 
)

hr_in_past_week = hr_in_range(
  past_week_time, 
  current_time, 
)

hr_in_past_month = hr_in_range(
  past_month_time, 
  current_time, 
)

# print('test values', hr_in_past_day_time, hr_in_past_two_days, hr_in_past_week, hr_in_past_month)

def agitation_over_time(hr_in_period, hr_over_time, time_period):
  avg_hr = sum(hr_in_period)/len(hr_in_period)
  avg_long_term_hr = sum(hr_over_time)/len(hr_over_time)
  # sum = 0 
  # for value in hr_over_time:
  #   diff = abs(value - avg_long_term_hr) * abs(value - avg_long_term_hr)
  #   sum = sum + diff 
  st_dev_hr = numpy.std(hr_over_time)

  template_str_more = Template("Heartrate is higher than normal compared to $time_period.")
  template_str_less = Template("Heartrate is lower than normal compared to $time_period.")
  template_str_normal = Template("Heartrate is looking normal compared to $time_period.")

  if avg_hr > (avg_long_term_hr + 1.68 * st_dev_hr):
    hr_level_tip = {
      'message': template_str_more.substitute(time_period=time_period),
      'importance': 2,
      'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
    }
    return hr_level_tip

  elif avg_hr < (avg_long_term_hr - 1.68 * st_dev_hr):
    hr_level_tip = {
      'message': template_str_less.substitute(time_period=time_period),
      'importance': 2,
      'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
    }
    return hr_level_tip

  else:
    hr_level_tip = {
      'message': template_str_normal.substitute(time_period=time_period),
      'importance': 0,
      'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
    } 
  return hr_level_tip


# # results for heartrate level tip 
today_hr_vs_yesterday = agitation_over_time(hr_in_past_day_time, hr_in_past_two_days, "yesterday")
past_two_days_hr_vs_past_week = agitation_over_time(hr_in_past_two_days, hr_in_past_week, "the past week") # 2/7 
past_week_hr_vs_past_month = agitation_over_time(hr_in_past_week, hr_in_past_month, "week")
print('today agitation', today_hr_vs_yesterday)
print('past two day agitation', past_two_days_hr_vs_past_week)
print('this week agitation', past_week_hr_vs_past_month)

# # longer term trends 
# if (today_hr_vs_yesterday['importance'] > past_two_days_hr_vs_past_week['importance'] 
# and past_two_days_hr_vs_past_week['importance'] > past_week_hr_vs_past_month['importance']):
#   agitation_trends_tip = {
#     'message': "you need help, this is acute.",
#     'importance': 5,
#     'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#   }
# elif (today_hr_vs_yesterday['importance'] == 0
# and past_two_days_hr_vs_past_week['importance'] == 0
# and past_week_hr_vs_past_month['importance'] == 0):
#   agitation_trends_tip = {
#     'message': "No change in behavior patterns.",
#     'importance': 1,
#     'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#   }
# elif (today_hr_vs_yesterday['importance'] == 1
# and past_two_days_hr_vs_past_week['importance'] == 1
# and past_week_hr_vs_past_month['importance'] == 1):
#   agitation_trends_tip = {
#     'message': "Decreasing behavior pattern over past month.",
#     'importance': 2,
#     'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#   }
# elif (today_hr_vs_yesterday['importance'] == 2
# and past_two_days_hr_vs_past_week['importance'] == 2
# and past_week_hr_vs_past_month['importance'] == 2):
#   agitation_trends_tip = {
#     'message': "Increasing behavior patterns.",
#     'importance': 4,
#     'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#   }
# else: 
#   agitation_trends_tip = {
#     'message': "No discernable pattern.",
#     'importance': 0,
#     'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#   }

# if today_hr_vs_yesterday['importance'] > agitation_trends_tip['importance']:
#   primary_agitation_tip = today_hr_vs_yesterday
#   secondary_agitation_tip = agitation_trends_tip
# else:
#   primary_agitation_tip = agitation_trends_tip
#   secondary_agitation_tip = today_hr_vs_yesterday

# agitation_tips = {
#   'primary_agitation_tip': primary_agitation_tip,
#   'secondary_agitation_tip': secondary_agitation_tip
# }

# print('final agitation tips', agitation_tips)






# hr_in_past_day_time = hr_in_range(
#   past_day_time, 
#   current_time, 
#   past_day_time_array, 
#   datetime_timestamps
# )

# hr_in_past_two_days = hr_in_range(
#   past_two_days_time, 
#   current_time, 
#   past_two_days_array, 
#   datetime_timestamps
# )

# hr_in_past_week = hr_in_range(
#   past_week_time, 
#   current_time, 
#   past_week_array, 
#   datetime_timestamps
# )

# hr_in_past_month = hr_in_range(
#   past_month_time, 
#   current_time, 
#   past_months_array, 
#   datetime_timestamps
# )

# determine whether how many hr are occuring relative to longer timeframes 
# def agitation_over_time(hr_in_period, hr_over_time, divide_by_val, time_period):
#   avg_hr = len(hr_over_time) / divide_by_val

#   template_str_more = Template("There's more agitation than usual in the past $time_period.")
#   template_str_less = Template("There's less agitation than usual in the past $time_period.")
#   template_str_normal = Template("Agitation has been about the same in the past $time_period.")

#   if len(hr_in_period) > avg_hr:
#     hr_level_tip = {
#       'message': template_str_more.substitute(time_period=time_period),
#       'importance': 2,
#       'link': "https://www.webmd.com/alzheimers/guide/treating-agitation"
#     }
#     return hr_level_tip

#   elif len(hr_in_period) < avg_hr:
#     hr_level_tip = {
#       'message': template_str_less.substitute(time_period=time_period),
#       'importance': 1,
#       'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#     }
#     return hr_level_tip

#   elif len(hr_in_period) == avg_hr:
#     hr_level_tip = {
#       'message': template_str_normal.substitute(time_period=time_period),
#       'importance': 0,
#       'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#     } 
#   return hr_level_tip
 
# # results for agitation frequency tip 
# today_hr_vs_yesterday = agitation_over_time(hr_in_past_day_time, hr_in_past_two_days, 2, "day")
# past_two_days_hr_vs_past_week = agitation_over_time(hr_in_past_two_days, hr_in_past_week, 0.2857, "two days") # 2/7 
# past_week_hr_vs_past_month = agitation_over_time(hr_in_past_week, hr_in_past_month, 2, "week")
# print('today agitation', today_hr_vs_yesterday)
# print('past two day agitation', past_two_days_hr_vs_past_week)
# print('this week agitation', past_week_hr_vs_past_month)

# # longer term trends 
# if (today_hr_vs_yesterday['importance'] > past_two_days_hr_vs_past_week['importance'] 
# and past_two_days_hr_vs_past_week['importance'] > past_week_hr_vs_past_month['importance']):
#   agitation_trends_tip = {
#     'message': "you need help, this is acute.",
#     'importance': 5,
#     'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#   }
# elif (today_hr_vs_yesterday['importance'] == 0
# and past_two_days_hr_vs_past_week['importance'] == 0
# and past_week_hr_vs_past_month['importance'] == 0):
#   agitation_trends_tip = {
#     'message': "No change in behavior patterns.",
#     'importance': 1,
#     'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#   }
# elif (today_hr_vs_yesterday['importance'] == 1
# and past_two_days_hr_vs_past_week['importance'] == 1
# and past_week_hr_vs_past_month['importance'] == 1):
#   agitation_trends_tip = {
#     'message': "Decreasing behavior pattern over past month.",
#     'importance': 2,
#     'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#   }
# elif (today_hr_vs_yesterday['importance'] == 2
# and past_two_days_hr_vs_past_week['importance'] == 2
# and past_week_hr_vs_past_month['importance'] == 2):
#   agitation_trends_tip = {
#     'message': "Increasing behavior patterns.",
#     'importance': 4,
#     'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#   }
# else: 
#   agitation_trends_tip = {
#     'message': "No discernable pattern.",
#     'importance': 0,
#     'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
#   }

# if today_hr_vs_yesterday['importance'] > agitation_trends_tip['importance']:
#   primary_agitation_tip = today_hr_vs_yesterday
#   secondary_agitation_tip = agitation_trends_tip
# else:
#   primary_agitation_tip = agitation_trends_tip
#   secondary_agitation_tip = today_hr_vs_yesterday

# agitation_tips = {
#   'primary_agitation_tip': primary_agitation_tip,
#   'secondary_agitation_tip': secondary_agitation_tip
# }

# print('final agitation tips', agitation_tips)
