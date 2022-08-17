from calendar import week
import datetime
from string import Template
import numpy 

def hr_tips_function(data):
    # time frames 
    current_time = datetime.datetime.now()
    past_day_time = current_time - datetime.timedelta(hours=12)
    past_two_days_time = current_time - datetime.timedelta(days=2)
    past_week_time = current_time - datetime.timedelta(days=7)
    past_month_time = current_time - datetime.timedelta(days=30)
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

    def hr_over_time(hr_in_period, hr_over_time, time_period):
        avg_hr = numpy.mean(hr_in_period)
        avg_long_term_hr = numpy.mean(hr_over_time)
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
            'importance': 1,
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

    # results for heartrate level tip 
    today_hr_vs_yesterday = hr_over_time(hr_in_past_day_time, hr_in_past_two_days, "yesterday")
    past_two_days_hr_vs_past_week = hr_over_time(hr_in_past_two_days, hr_in_past_week, "the past week") # 2/7 
    past_week_hr_vs_past_month = hr_over_time(hr_in_past_week, hr_in_past_month, "week")
    print('today agitation', today_hr_vs_yesterday)
    print('past two day agitation', past_two_days_hr_vs_past_week)
    print('this week agitation', past_week_hr_vs_past_month)

    if (today_hr_vs_yesterday['importance'] > past_two_days_hr_vs_past_week['importance']
    and today_hr_vs_yesterday['importance'] > past_week_hr_vs_past_month['importance']):
        primary_hr_tip = today_hr_vs_yesterday
    elif (past_two_days_hr_vs_past_week['importance'] > today_hr_vs_yesterday['importance']
    and past_two_days_hr_vs_past_week['importance'] > past_week_hr_vs_past_month['importance']):
        primary_hr_tip = past_two_days_hr_vs_past_week
    elif (past_week_hr_vs_past_month['importance'] > today_hr_vs_yesterday['importance']
    and past_week_hr_vs_past_month['importance'] > past_two_days_hr_vs_past_week['importance']):
        primary_hr_tip = past_week_hr_vs_past_month
    else:
        primary_hr_tip = today_hr_vs_yesterday

    hr_tips = {
    'primary_hr_tip': primary_hr_tip,
    }
    print('HR tips here', hr_tips)
    return hr_tips