from datetime import timedelta
from dateutil import parser
import time 
import json
import boto3
s3 = boto3.client('s3')

def acc_function(bucket, key, data): 

    new_x = data.get("acceleration", {}).get("x_val", None)
    new_y = data.get("acceleration", {}).get("y_val", None)
    new_z = data.get("acceleration", {}).get("z_val", None)
    freq = int(data.get("acceleration", {}).get("frequency", None))
    str_date = data.get("metaData", {}).get("startQueryTime", None) 
    start_time = parser.parse(str_date)
    new_timestamps = []
    time_val = 0 
    unix_time = float(time.mktime(start_time.timetuple())*1000)

    for x in new_x: 
        unix_time += time_val/freq*1000
        new_timestamps.append(unix_time)
        time_val += 1000
    print('time val array', new_timestamps)

    try: 
        processed_response = s3.get_object(Bucket=bucket, Key=key)
        processed_content = processed_response["Body"]
        processed_jsonobj = json.loads(processed_content.read())
        # print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
        print('Sensor JSON from processed s3 retrieved:')

        old_x = processed_jsonobj.get("acceleration", {}).get("x_val", None) 
        old_y = processed_jsonobj.get("acceleration", {}).get("y_val", None) 
        old_z = processed_jsonobj.get("acceleration", {}).get("z_val", None)
        old_timestamps = processed_jsonobj.get("acceleration", {}).get("timestamps", None) 
        total_x = old_x + new_x 
        total_y = old_y + new_y
        total_z = old_z + new_z
        total_timestamps = old_timestamps + new_timestamps

        aggregate_json = { 
            "acceleration": {
                "x_val": total_x,
                "y_val": total_y,
                "z_val": total_z,
                "timestamps": total_timestamps
            },
        }
        print('data successfully aggregated.')

    except: 
        aggregate_json = {
            "acceleration": {
                "x_val": new_x,
                "y_val": new_y,
                "z_val": new_z,
                "timestamps": new_timestamps
            },
        }
        print('no existing JSON, new sensor file created', aggregate_json)

    finalData = json.dumps(aggregate_json).encode("UTF-8")
    s3.put_object(Body=finalData, Bucket=bucket, Key=key)
    print("JSON file uploaded successfully.")
    return finalData