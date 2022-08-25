import json
from string import Template
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):

    mobile_bucket = 'adiona-user-profile-data'
    
    file_type = event["headers"]["content-type"]
    context = event["requestContext"]
    file_send_time = context["time"]
    method = context["http"]["method"]

    modified_file_send_time = file_send_time.replace('/', '-')
    body = event["body"]
    processed_body = json.loads(body)
    user_id = processed_body["metaData"]["user_id"]
    
    profile_status = "succeeded"
    error = []  
    
    if method == "POST": 

        try: 
            profile_template = Template('$id/profileData.json')
            profile_key = profile_template.substitute(id=user_id)
            print('Here is profile key', profile_key)
            profile_response = s3.get_object(Bucket=mobile_bucket, Key=profile_key)
            profile = profile_response["Body"]
            processed_profiles = json.loads(profile.read())
            print('here is profile data', processed_profiles)
            print('profile succeeded')
        except Exception as e: 
            profile_status = "failed"
            print('failed to get profile')
            print(e)

    if profile_status == "succeeded": 
        print('profile retrieved')
        return {
            'statusCode': 200,
            'body': json.dumps(processed_profiles)
        } 
        
    else: 
        print('failed to get profile')
        return {
            'statusCode': 400,
            # 'body': json.dumps("this call failed.")
            'body': json.dumps(processed_profiles)

        }
    # print('something happened')

    # return {
    #     'statusCodee': 200,
    #     'body': json.dumps(event)
    # }
    
