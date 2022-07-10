from dateutil import parser
import time 
import json
import boto3
s3 = boto3.client('s3')

def hr_function(bucket, key, data): 

    new_hr = data.get("heart_rate", {}).get("value", None)
    hr_times = data.get("heart_rate", {}).get("queryTime", None) 
    new_hr_timestamps = [] 
    for val in hr_times: 
        parsed_time = parser.parse(val)
        unix = time.mktime(parsed_time.timetuple())
        new_hr_timestamps.append(unix)
        print(new_hr_timestamps)

    try: 
        processed_response = s3.get_object(Bucket=bucket, Key=key)
        processed_content = processed_response["Body"]
        processed_jsonobj = json.loads(processed_content.read())
        print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
        old_hr = processed_jsonobj.get("heart_rate", {}).get("value", None) 
        old_timestamps = processed_jsonobj.get("heart_rate", {}).get("timestamps", None) 
        total_hr = old_hr + new_hr
        total_hr_timestamps = old_timestamps + new_hr_timestamps

        aggregate_json = { 
            "heart_rate": {
                "value": total_hr,
                "timestamps": total_hr_timestamps
            },
        }

    except: 
        aggregate_json = {
            "heart_rate": {
                "value": new_hr,
                "timestamps": new_hr_timestamps
            },
        }
        print('no existing JSON, new sensor file created', aggregate_json)

    finalData = json.dumps(aggregate_json).encode("UTF-8")
    s3.put_object(Body=finalData, Bucket=bucket, Key=key)
    print("JSON file uploaded successfully.")
    return finalData
