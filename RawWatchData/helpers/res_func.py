from dateutil import parser
import time 
import json
import boto3
s3 = boto3.client('s3')

def res_function(bucket, key, data): 

    new_res_rate = data.get("respiratory_rate", {}).get("value", None)
    res_rate_times = data.get("respiratory_rate", {}).get("queryTime", None) 
    new_bloodox = data.get("oxygen_saturation", {}).get("value", None)
    new_res_rate_timestamps = [] 
    print('res rate times', res_rate_times)

    for val in res_rate_times: 
        parsed_time = parser.parse(val)
        unix = time.mktime(parsed_time.timetuple())
        new_res_rate_timestamps.append(unix)
        print(new_res_rate_timestamps)

    try: 
        processed_response = s3.get_object(Bucket=bucket, Key=key)
        processed_content = processed_response["Body"]
        processed_jsonobj = json.loads(processed_content.read())
        print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
        old_res_rate = processed_jsonobj.get("respiratory_rate", {}).get("value", None) 
        old_res_timestamps = processed_jsonobj.get("respiratory_rate", {}).get("timestamps", None) 
        total_res_rate = old_res_rate + new_res_rate
        total_res_rate_timestamps = old_res_timestamps + new_res_rate_timestamps

        old_bloodox = processed_jsonobj.get("oxygen_saturation", {}).get("value", None) 
        total_bloodox = old_bloodox + new_bloodox


        aggregate_json = { 
            "respiratory_rate": {
                "value": total_res_rate,
                "timestamps": total_res_rate_timestamps
            },
            "oxygen_saturation": {
                "value": total_bloodox,
                "timestamps": total_res_rate_timestamps
            }
        }

    except: 
        aggregate_json = {
            "respiratory_rate": {
                "value": new_res_rate,
                "timestamps": new_res_rate_timestamps
            },
            "oxygen_saturation": {
                "value": new_bloodox,
                "timestamps": new_res_rate_timestamps
            }           
        }
        print('no existing JSON, new sensor file created', aggregate_json)

    finalData = json.dumps(aggregate_json).encode("UTF-8")
    s3.put_object(Body=finalData, Bucket=bucket, Key=key)
    print("JSON file uploaded successfully.")
    return finalData
