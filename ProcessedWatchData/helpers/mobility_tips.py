from calendar import week
import datetime
from string import Template
import numpy 

def mobility_tips_function(data):
    print('makes it to start of function')
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
    for unix in data['mobility']['timestamps']:
        str_datetime_obj = datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%dT%H:%M:%S')
        datetime_obj = datetime.datetime.strptime(str_datetime_obj, '%Y-%m-%dT%H:%M:%S')
        datetime_timestamps.append(datetime_obj)

    dict_values = {}
    for key in datetime_timestamps:
        for value in data['mobility']['fall_resolution']:
            dict_values[key] = value
            data['mobility']['fall_resolution'].remove(value)
            break  
    
    print(dict_values)
    # get all hr values in each time range  
    def falls_in_range(beginning_window, ending_window):
        list = [] 
        for timestamp in dict_values.keys(): 
            if timestamp > beginning_window and timestamp <= ending_window:
                list.append(dict_values[timestamp])
        return list

    falls_in_past_day_time = falls_in_range(
    past_day_time, 
    current_time, 
    )

    falls_in_past_two_days = falls_in_range(
    past_two_days_time, 
    current_time, 
    )

    falls_in_past_week = falls_in_range(
    past_week_time, 
    current_time, 
    )

    falls_in_past_month = falls_in_range(
    past_month_time, 
    current_time, 
    )

    # print('test values', hr_in_past_day_time, hr_in_past_two_days, hr_in_past_week, hr_in_past_month)

    def agitation_over_time(falls_in_period, falls_over_time, time_period):
        try: 
            avg_falls = sum(falls_in_period)/len(falls_in_period)
        except: 
            avg_falls = 1
        try: 
            avg_long_term_falls = sum(falls_over_time)/len(falls_over_time)
        except: 
            avg_long_term_falls = 1
        # sum = 0 
        # for value in hr_over_time:
        #   diff = abs(value - avg_long_term_hr) * abs(value - avg_long_term_hr)
        #   sum = sum + diff 
        # st_dev_falls = numpy.std(falls_over_time)

        template_str_more = Template("falls is higher than normal compared to $time_period.")
        template_str_less = Template("falls is lower than normal compared to $time_period.")
        template_str_normal = Template("falls is looking normal compared to $time_period.")

        if avg_falls > (avg_long_term_falls):
            falls_level_tip = {
            'message': template_str_more.substitute(time_period=time_period),
            'importance': 2,
            'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
            }
            return falls_level_tip

        elif avg_falls < (avg_long_term_falls):
            falls_level_tip = {
            'message': template_str_less.substitute(time_period=time_period),
            'importance': 2,
            'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
            }
            return falls_level_tip

        else:
            falls_level_tip = {
            'message': template_str_normal.substitute(time_period=time_period),
            'importance': 0,
            'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
            } 
        return falls_level_tip


    # # results for heartrate level tip 
    today_falls_vs_yesterday = agitation_over_time(falls_in_past_day_time, falls_in_past_two_days, "yesterday")
    past_two_days_falls_vs_past_week = agitation_over_time(falls_in_past_two_days, falls_in_past_week, "the past week") # 2/7 
    past_week_falls_vs_past_month = agitation_over_time(falls_in_past_week, falls_in_past_month, "week")
    print('today falls', today_falls_vs_yesterday)
    print('past two day falls', past_two_days_falls_vs_past_week)
    print('this week falls', past_week_falls_vs_past_month)

    if (today_falls_vs_yesterday['importance'] > past_two_days_falls_vs_past_week['importance']
    and today_falls_vs_yesterday['importance'] > past_week_falls_vs_past_month['importance']):
        primary_falls_tip = today_falls_vs_yesterday
    elif (past_two_days_falls_vs_past_week['importance'] > today_falls_vs_yesterday['importance']
    and past_two_days_falls_vs_past_week['importance'] > past_week_falls_vs_past_month['importance']):
        primary_falls_tip = past_two_days_falls_vs_past_week
    elif (past_week_falls_vs_past_month['importance'] > today_falls_vs_yesterday['importance']
    and past_week_falls_vs_past_month['importance'] > past_two_days_falls_vs_past_week['importance']):
        primary_falls_tip = past_week_falls_vs_past_month
    elif today_falls_vs_yesterday:
        primary_falls_tip = today_falls_vs_yesterday
    else: 
        print('makes it here')
        primary_falls_tip = {
            'message': 'No falls data. Tap to see what might be the issue.',
            'importance': 0,
            'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
            } 

    falls_tips = {
    'primary_falls_tip': primary_falls_tip,
    }
    print('falls tips here', falls_tips)
    return falls_tips