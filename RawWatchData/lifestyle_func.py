from dateutil import parser
import time 
import json
import boto3
s3 = boto3.client('s3')

def lifestyle_function(bucket, key, data): 

    new_steps = data.get("step_count", {}).get("value", None)
    steps_times = data.get("step_count", {}).get("queryTime", None) 
    new_calories = data.get("calories", {}).get("value", None)
    new_steps_timestamps = [] 
    print('res rate times', steps_times)

    for val in steps_times: 
        parsed_time = parser.parse(val)
        unix = time.mktime(parsed_time.timetuple())
        new_steps_timestamps.append(unix)
        print(new_steps_timestamps)

    try: 
        processed_response = s3.get_object(Bucket=bucket, Key=key)
        processed_content = processed_response["Body"]
        processed_jsonobj = json.loads(processed_content.read())
        print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
        old_steps = processed_jsonobj.get("step_count", {}).get("value", None) 
        old_steps_timestamps = processed_jsonobj.get("step_count", {}).get("timestamps", None) 
        total_steps = old_steps + new_steps
        total_steps_timestamps = old_steps_timestamps + new_steps_timestamps

        old_calories = processed_jsonobj.get("calories", {}).get("value", None) 
        total_calories = old_calories + new_calories


        aggregate_json = { 
            "step_count": {
                "value": total_steps,
                "timestamps": total_steps_timestamps
            },
            "calories": {
                "value": total_calories,
                "timestamps": total_steps_timestamps
            }
        }

    except: 
        aggregate_json = {
            "step_count": {
                "value": new_steps,
                "timestamps": new_steps_timestamps
            },
            "calories": {
                "value": new_calories,
                "timestamps": new_steps_timestamps
            }           
        }
        print('no existing JSON, new sensor file created', aggregate_json)

    finalData = json.dumps(aggregate_json).encode("UTF-8")
    s3.put_object(Body=finalData, Bucket=bucket, Key=key)
    print("JSON file uploaded successfully.")
    return finalData
