import json
from string import Template
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):

    raw_bucket = 'raw-adiona-watch-app-data'
    mobile_bucket = 'mobile-app-ready-data'
    
    file_type = event["headers"]["content-type"]
    context = event["requestContext"]
    file_send_time = context["time"]
    method = context["http"]["method"]

    modified_file_send_time = file_send_time.replace('/', '-')
    body = event["body"]
    processed_body = json.loads(body)
    user_id = processed_body["metaData"]["user_id"]
    
    post_file_status = "succeeded"
    geofence_status = "succeeded"
    error = []  
    
    if method == "POST": 
        
        try: 
            template = Template('$id/$file_time.json')
            key = template.substitute(id=user_id, file_time=modified_file_send_time)
            print('here is post key', key)
            to_raw_s3_data = json.dumps(processed_body).encode("UTF-8")
            s3.put_object(Body=to_raw_s3_data, Bucket=raw_bucket, Key=key)
            post_file_status = "succeeded"
            print('main file succeeded')

        except Exception as e: 
            post_file_status = "failed"
            print('main file failed')
            print(e)

        try: 
            geofence_template = Template('$id/geofences.json')
            geo_key = geofence_template.substitute(id=user_id)
            print('Here is geofences key', geo_key)
            geofence_response = s3.get_object(Bucket=mobile_bucket, Key=geo_key)
            geofences = geofence_response["Body"]
            processed_geofences = json.loads(geofences.read())
            print('here are geofences', processed_geofences)
            print('geofences succeeded')
        except Exception as e: 
            geofence_status = "failed"
            print('geofences failed')
            print(e)

        
    if post_file_status == "succeeded" and geofence_status == "succeeded": 
        print('both worked')
        return {
            'statusCode': 200,
            'body': json.dumps(processed_geofences)
        }
        
    elif post_file_status == "succeeded": 
        print('only post file worked')
        return {
            'statusCode': 200,
            'body': json.dumps(processed_body)
        }
    
    elif geofence_status == "succeeded": 
        print('only geofences worked')
        return {
            'statusCode': 200,
            'body': json.dumps(processed_geofences)
        } 
        
    else: 
        print('nothing worked')
        return {
            'statusCode': 400,
            'body': json.dumps("this call failed.")
        }
    
