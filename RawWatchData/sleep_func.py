import json
from operator import truediv
import boto3
import pickle 
from datetime import timedelta
from dateutil import parser
import time 
s3 = boto3.client('s3')

def sleep_function(bucket, sleep_data_key, data): 

    try:     
        new_x = data.get("acceleration", {}).get("x_val", None)
        new_y = data.get("acceleration", {}).get("y_val", None)
        new_z = data.get("acceleration", {}).get("z_val", None)
        freq = data.get("acceleration", {}).get("frequency", None)
        str_date = data.get("acceleration", {}).get("startQueryTime", None) 
        new_date = parser.parse(str_date)
        new_timestamps = []
        time_val = 0 

        for x in new_x: 
            incremented_date = new_date + timedelta(seconds = time_val/freq)
            unix = time.mktime(incremented_date.timetuple())
            new_timestamps.append(unix)
            time_val += 1 


        # retrieve model and run processed data through model below 
        try: 
            # some sleep algorithm here 
            result = {
                "asleep": True, 
                "start_time_1": "2022-06-12T10:33:25",
                "end_time_1": "2022-06-13T10:33:25",
                "start_time_2": "2022-06-12T10:33:25",
                "end_time_2": "2022-06-13T10:33:25"
            }
        except: 
            print('No trained sleep model available.')
            return 
        
        if result["asleep"] == True:
            try: 
                raw_old_sleep = s3.get_object(Bucket=bucket, Key=sleep_data_key)
                old_sleep = raw_old_sleep["Body"]
                old_sleep_json = json.loads(old_sleep.read())
                print('Agitation JSON from processed s3 retrieved:', old_sleep_json)
                old_episodes = old_sleep_json.get("sleep_episodes", {})
                old_episodes.append(result)

                old_sleep_json = {
                    "episodes": old_episodes
                }

                finalData = json.dumps(old_sleep_json).encode("UTF-8")
                s3.put_object(Body=finalData, Bucket=bucket, Key=sleep_data_key)
                print("JSON file uploaded successfully.")
                return finalData
            except: 
                old_sleep_json = {
                    "sleep_episodes": [result],
                } 
                finalData = json.dumps(old_sleep_json).encode("UTF-8")
                s3.put_object(Body=finalData, Bucket=bucket, Key=sleep_data_key)
                print('no existing displayed truth JSON, new file created')
                return finalData
    
    except Exception as e: 
        print(e)
        json_sleep = {
            "sleep_episodes": [result]
        }
        print('no existing ground truth data, new file created', json_sleep)
        finalData = json.dumps(json_sleep).encode("UTF-8")
        s3.put_object(Body=finalData, Bucket=bucket, Key=sleep_data_key)
        print("new JSON file uploaded successfully.")
        return finalData