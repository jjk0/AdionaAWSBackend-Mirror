from concurrent.futures import process
import json
import boto3
s3 = boto3.client('s3')
from string import Template 
from tips.lifestyle_tips import lifestyle_tips_function
from tips.heart_tips import heart_tips_function
from tips.respiratory_tips import respiratory_tips_function
from tips.sleep_tips import sleep_tips_function 
from tips.agitation_tips import agitation_tips_function
from tips.mobility_tips import mobility_tips_function


########### TO DO: USE DYNAMO DATA TO IMPROVE THIS FUNCTION ##############
############## THIS DATA INCLUES PROFILE DATA AND MANUAL DATA FROM DAILY DIARY 



def tips_function(processed_bucket, mobile_bucket, data_list): 
# data_list = [lifestyle_data_key, sleep_data_key, hr_data_key, respiratory_data_key, agitation_data_key] 

    # def get_data(index, bucket):
    #     raw = s3.get_object(Bucket=bucket, Key=data_list[index])
    #     processed_data = raw["Body"]
    #     readable_data = json.loads(processed_data.read())
    #     print(Template('Data frm index $index retrieved successfully.'))
    #     return readable_data

    try:   
        lifestyle_data = data_list[0]
        # sleep_data = get_data(1, mobile_bucket)  
        # hr_data = get_data(2, processed_bucket)  
        # respiratory_data = get_data(3, processed_bucket)  
        # agitation_data = get_data(4, mobile_bucket)

        lifestyle_tips = lifestyle_tips_function(lifestyle_data)
        print('this worked.')

        ############# rank all tips' priorities ############
        ############# write tips to display in main tips section ############


    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(bucket))
        raise e  