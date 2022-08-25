from calendar import week
import datetime
from string import Template

def agitation_tips_function(data):
    # time frames 
    current_time = datetime.datetime.now()
    past_day_time = current_time - datetime.timedelta(hours=12)
    past_two_days_time = current_time - datetime.timedelta(days=2)
    past_week_time = current_time - datetime.timedelta(days=7)
    past_month_time = current_time - datetime.timedelta(days=30)
    timeframes = [
        current_time,
        past_day_time,
        past_two_days_time,
        past_week_time,
        past_month_time
    ]
    past_day_time_array = []
    past_two_days_array = []
    past_week_array = []
    past_months_array = [] 

    # convert datetime strings to datetime object
    datetime_timestamps = []
    for string in data['episodes']:
        datetime_obj = datetime.datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')
        datetime_timestamps.append(datetime_obj)

    # get all timestamps in range 
    def episodes_in_range(beginning_window, ending_window, array, timestamps):
        for timestamp in timestamps: 
            if timestamp > beginning_window and timestamp <= ending_window:
                array.append(timestamp)
        return array
    
    episodes_in_past_day_time = episodes_in_range(
    past_day_time, 
    current_time, 
    past_day_time_array, 
    datetime_timestamps
    )

    episodes_in_past_two_days = episodes_in_range(
    past_two_days_time, 
    current_time, 
    past_two_days_array, 
    datetime_timestamps
    )

    episodes_in_past_week = episodes_in_range(
    past_week_time, 
    current_time, 
    past_week_array, 
    datetime_timestamps
    )

    episodes_in_past_month = episodes_in_range(
    past_month_time, 
    current_time, 
    past_months_array, 
    datetime_timestamps
    )

    # determine whether how many episodes are occuring relative to longer timeframes 
    def agitation_over_time(episodes_in_period, episodes_over_time, divide_by_val, time_period):
        avg_episodes = len(episodes_over_time) / divide_by_val

        template_str_more = Template("There's more agitation than usual in the past $time_period.")
        template_str_less = Template("There's less agitation than usual in the past $time_period.")
        template_str_normal = Template("Agitation has been about the same in the past $time_period.")

        if len(episodes_in_period) > avg_episodes:
            agitation_frequency_tip = {
            'message': template_str_more.substitute(time_period=time_period),
            'importance': 2,
            'link': "https://www.webmd.com/alzheimers/guide/treating-agitation"
            }
            return agitation_frequency_tip

        elif len(episodes_in_period) < avg_episodes:
            agitation_frequency_tip = {
            'message': template_str_less.substitute(time_period=time_period),
            'importance': 1,
            'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
            }
            return agitation_frequency_tip

        elif len(episodes_in_period) == avg_episodes:
            agitation_frequency_tip = {
            'message': template_str_normal.substitute(time_period=time_period),
            'importance': 0,
            'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
            } 
        return agitation_frequency_tip
    
    # results for agitation frequency tip 
    today_agitation = agitation_over_time(episodes_in_past_day_time, episodes_in_past_two_days, 2, "day")
    past_two_days_agitation = agitation_over_time(episodes_in_past_two_days, episodes_in_past_week, 0.2857, "two days") # 2/7 
    this_week_agitation = agitation_over_time(episodes_in_past_week, episodes_in_past_month, 2, "week")
    print('today agitation', today_agitation)
    print('past two day agitation', past_two_days_agitation)
    print('this week agitation', this_week_agitation)

    # longer term trends 
    if (today_agitation['importance'] > past_two_days_agitation['importance'] 
    and past_two_days_agitation['importance'] > this_week_agitation['importance']):
        agitation_trends_tip = {
            'message': "you need help, this is acute.",
            'importance': 5,
            'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
        }
    elif (today_agitation['importance'] == 0
    and past_two_days_agitation['importance'] == 0
    and this_week_agitation['importance'] == 0):
        agitation_trends_tip = {
            'message': "No change in behavior patterns.",
            'importance': 1,
            'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
        }
    elif (today_agitation['importance'] == 1
    and past_two_days_agitation['importance'] == 1
    and this_week_agitation['importance'] == 1):
        agitation_trends_tip = {
            'message': "Decreasing behavior pattern over past month.",
            'importance': 2,
            'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
        }
    elif (today_agitation['importance'] == 2
        and past_two_days_agitation['importance'] == 2
        and this_week_agitation['importance'] == 2):
        agitation_trends_tip = {
            'message': "Increasing behavior patterns.",
            'importance': 4,
            'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
        }
    else: 
        agitation_trends_tip = {
            'message': "No discernable pattern.",
            'importance': 0,
            'link': "https://www.alz.org/help-support/caregiving/stages-behaviors/anxiety-agitation"
        }

    if today_agitation['importance'] > agitation_trends_tip['importance']:
        primary_agitation_tip = today_agitation
        secondary_agitation_tip = agitation_trends_tip
    else:
        primary_agitation_tip = agitation_trends_tip
        secondary_agitation_tip = today_agitation

    agitation_tips = {
        'primary_agitation_tip': primary_agitation_tip,
        'secondary_agitation_tip': secondary_agitation_tip
    }

    print('final agitation tips', agitation_tips)
    return agitation_tips

