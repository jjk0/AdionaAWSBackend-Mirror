from concurrent.futures import process
import json
import boto3
s3 = boto3.client('s3')
from string import Template 
# from tips.lifestyle_tips import lifestyle_tips_function
# from tips.heart_tips import heart_tips_function
# from tips.respiratory_tips import respiratory_tips_function
# from tips.sleep_tips import sleep_tips_function 
# from tips.agitation_tips import agitation_tips_function
# from tips.mobility_tips import mobility_tips_function


########### TO DO: USE DYNAMO DATA TO IMPROVE THIS FUNCTION ##############
############## THIS DATA INCLUES PROFILE DATA AND MANUAL DATA FROM DAILY DIARY 



def tips_function(processed_bucket, mobile_bucket, tips_input_data, agitation_tips_function, hr_tips_function): 
    print('tips input data agitation', tips_input_data['agitation'])

    def get_data(index, bucket):
        raw = s3.get_object(Bucket=bucket, Key=tips_input_data[index])
        processed_data = raw["Body"]
        readable_data = json.loads(processed_data.read())
        template_readout = Template('Data from $index retrieved successfully.')
        print(template_readout.substitute(index=index))
        return readable_data

    try:   
        agitation_data = get_data('agitation', mobile_bucket)
        agitation_tips = agitation_tips_function(agitation_data)
        print('agitation tips', agitation_tips)
    except Exception as e: 
        print(e)
        print('Agitation data unavailable for tips.')
    
    try: 
        hr_data = get_data('heart', mobile_bucket)
        heart_tips = hr_tips_function(hr_data)
        print('heart tips data', heart_tips)
    except Exception as e: 
        print(e)
        print('Heart data unavailable for tips.')  
    
    # try:   
    #     sleep = get_data('sleep', mobile_bucket)
    #     print('sleep tips', sleep)
    # except Exception as e: 
    #     print(e)
    #     print('Sleep data unavailable for tips.')
    
    # try:   
    #     lifestyle = get_data('lifesetyle', mobile_bucket)
    #     print('lifestyle tips', lifestyle)
    # except Exception as e: 
    #     print(e)
    #     print('Lifestyle data unavailable for tips.')

    # try:   
    #     heart = get_data('heart', mobile_bucket)
    #     print('heart tips', heart)
    # except Exception as e: 
    #     print(e)
    #     print('Heart data unavailable for tips.')
    
        ############# rank all tips' priorities ############
        ############# write tips to display in main tips section ############


    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(bucket))
        raise e  