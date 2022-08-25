from calendar import week
import datetime
from string import Template
import numpy 

def lifestyle_tips_function(data):
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
    for unix in data['step_count']['timestamps']:
        str_datetime_obj = datetime.datetime.fromtimestamp(unix).strftime('%Y-%m-%dT%H:%M:%S')
        datetime_obj = datetime.datetime.strptime(str_datetime_obj, '%Y-%m-%dT%H:%M:%S')
        datetime_timestamps.append(datetime_obj)

    dict_values = {}
    for key in datetime_timestamps:
        for value in data['step_count']['value']:
            dict_values[key] = value
            data['step_count']['value'].remove(value)
            break  
    
    print(dict_values)
    # get all hr values in each time range  
    def steps_in_range(beginning_window, ending_window):
        list = [] 
        for timestamp in dict_values.keys(): 
            if timestamp > beginning_window and timestamp <= ending_window:
                list.append(dict_values[timestamp])
        return list

    steps_in_past_day_time = steps_in_range(
        past_day_time, 
        current_time, 
    )

    steps_in_past_two_days = steps_in_range(
        past_two_days_time, 
        current_time, 
    )

    steps_in_past_week = steps_in_range(
        past_week_time, 
        current_time, 
    )

    steps_in_past_month = steps_in_range(
        past_month_time, 
        current_time, 
    )

    print('processes timestamps')
    # print('test values', hr_in_past_day_time, hr_in_past_two_days, hr_in_past_week, hr_in_past_month)

    def steps_over_time(steps_in_period, steps_over_time, time_period):
        try: 
            avg_steps = sum(steps_in_period)/len(steps_in_period)
        except: 
            avg_steps = 1
        try: 
            avg_long_term_steps = sum(steps_over_time)/len(steps_over_time)
        except: 
            avg_long_term_steps = 1
        sum = 0 
        for value in steps_over_time:
          diff = abs(value - avg_long_term_steps) * abs(value - avg_long_term_steps)
          sum = sum + diff 
        st_dev_steps = numpy.std(steps_over_time)

        print('processes tips math')
        template_str_more = Template("Steps is higher than normal compared to $time_period.")
        template_str_less = Template("Steps is lower than normal compared to $time_period.")
        template_str_normal = Template("Steps is looking normal compared to $time_period.")

        if avg_steps > (avg_long_term_steps + 1.68 * st_dev_steps):
        # if avg_steps > (avg_long_term_steps):

            steps_level_tip = {
            'message': template_str_more.substitute(time_period=time_period),
            'importance': 2,
            'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
            }
            return steps_level_tip

        elif avg_steps < (avg_long_term_steps - 1.68 * st_dev_steps):
        # elif avg_steps < (avg_long_term_steps):

            steps_level_tip = {
            'message': template_str_less.substitute(time_period=time_period),
            'importance': 2,
            'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
            }
            return steps_level_tip

        else:
            steps_level_tip = {
            'message': template_str_normal.substitute(time_period=time_period),
            'importance': 0,
            'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
            } 
        return steps_level_tip

    print('gets tips')

    # # results for heartrate level tip 
    today_steps_vs_yesterday = steps_over_time(steps_in_past_day_time, steps_in_past_two_days, "yesterday")
    past_two_days_steps_vs_past_week = steps_over_time(steps_in_past_two_days, steps_in_past_week, "the past week") # 2/7 
    past_week_steps_vs_past_month = steps_over_time(steps_in_past_week, steps_in_past_month, "week")
    print('today steps', today_steps_vs_yesterday)
    print('past two day steps', past_two_days_steps_vs_past_week)
    print('this week steps', past_week_steps_vs_past_month)

    if (today_steps_vs_yesterday['importance'] > past_two_days_steps_vs_past_week['importance']
    and today_steps_vs_yesterday['importance'] > past_week_steps_vs_past_month['importance']):
        primary_steps_tip = today_steps_vs_yesterday
    elif (past_two_days_steps_vs_past_week['importance'] > today_steps_vs_yesterday['importance']
    and past_two_days_steps_vs_past_week['importance'] > past_week_steps_vs_past_month['importance']):
        primary_steps_tip = past_two_days_steps_vs_past_week
    elif (past_week_steps_vs_past_month['importance'] > today_steps_vs_yesterday['importance']
    and past_week_steps_vs_past_month['importance'] > past_two_days_steps_vs_past_week['importance']):
        primary_steps_tip = past_week_steps_vs_past_month
    elif today_steps_vs_yesterday:
        primary_steps_tip = today_steps_vs_yesterday
    else: 
        print('makes it here')
        primary_steps_tip = {
            'message': 'No steps data. Tap to see what might be the issue.',
            'importance': 0,
            'link': "https://www.nia.nih.gov/health/heart-health-and-aging"
            } 

    steps_tips = {
    'primary_steps_tip': primary_steps_tip,
    }
    print('steps tips here', steps_tips)
    return steps_tips