from dateutil import parser
import time 
import json
import boto3
s3 = boto3.client('s3')

def res_function(bucket, key, data): 
    try: 
        new_res_rates = data.get("respiratory_rate", {}).get("values", None)
        res_rates_times = data.get("respiratory_rate", {}).get("timestamps", None) 
        new_res_rates_timestamps = [] 

        for val in res_rates_times: 
            parsed_time = parser.parse(val)
            unix = time.mktime(parsed_time.timetuple())
            new_res_rates_timestamps.append(unix)
            print(new_res_rates_timestamps)
        res_rates_exists = True 

        if len(new_res_rates_timestamps) < 1:
            res_rates_exists = False 
            print("No res_rates available in this file.")

    except: 
        res_rates_exists = False 
        print("No res_rates available in this file.")

    try: 
        new_oxygen_saturation = data.get("oxygen_saturation", {}).get("values", None)
        oxygen_saturation_times = data.get("oxygen_saturation", {}).get("timestamps", None) 
        new_oxygen_saturation_timestamps = [] 
        print('res rate times', oxygen_saturation_times)

        for val in oxygen_saturation_times: 
            parsed_time = parser.parse(val)
            unix = time.mktime(parsed_time.timetuple())
            new_oxygen_saturation_timestamps.append(unix)
            print(new_oxygen_saturation_timestamps)
        bloodox_exists = True 

        if len(oxygen_saturation_times) < 1:
            bloodox_exists = False 
            print("No bloodox available in this file.")
        print('makes it to here')
    except: 
        bloodox_exists = False 
        print("No bloodox available in this file.")

    if ((res_rates_exists==True) and (bloodox_exists==True)): 

        try: 
            processed_response = s3.get_object(Bucket=bucket, Key=key)
            processed_content = processed_response["Body"]
            processed_jsonobj = json.loads(processed_content.read())
            print(type(processed_jsonobj))
            print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
            old_res_rates = processed_jsonobj.get("respiratory_rate", {}).get("values", None) 
            if len(old_res_rates) < 1: 
                old_res_rates = [] 
            old_res_rates_timestamps = processed_jsonobj.get("respiratory_rate", {}).get("timestamps", None) 

            total_res_rates = old_res_rates + new_res_rates
            total_res_rates_timestamps = old_res_rates_timestamps + new_res_rates_timestamps

            old_oxygen_saturation = processed_jsonobj.get("oxygen_saturation", {}).get("values", None) 
            if len(old_oxygen_saturation) < 1: 
                old_oxygen_saturation = [] 
            old_oxygen_saturation_timestamps = processed_jsonobj.get("oxygen_saturation", {}).get("timestamps", None) 
            total_oxygen_saturation = old_oxygen_saturation + new_oxygen_saturation
            total_oxygen_saturation_timestamps = old_oxygen_saturation_timestamps + new_oxygen_saturation_timestamps


            aggregate_json = { 
                "respiratory_rate": {
                    "values": total_res_rates,
                    "timestamps": total_res_rates_timestamps
                },
                "oxygen_saturation": {
                    "values": total_oxygen_saturation,
                    "timestamps": total_oxygen_saturation_timestamps
                }
            }

        except Exception as e: 
            print(e)
            aggregate_json = {
                "respiratory_rate": {
                    "values": new_res_rates,
                    "timestamps": new_res_rates_timestamps
                },
                "oxygen_saturation": {
                    "values": new_oxygen_saturation,
                    "timestamps": new_oxygen_saturation_timestamps
                }           
            }
            print('no existing JSON, new sensor file wih res_rates and bloodox created', aggregate_json)
        
    elif res_rates_exists==True: 

        try: 
            processed_response = s3.get_object(Bucket=bucket, Key=key)
            processed_content = processed_response["Body"]
            processed_jsonobj = json.loads(processed_content.read())
            print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
            old_res_rates = processed_jsonobj.get("respiratory_rate", {}).get("values", None) 
            old_res_rates_timestamps = processed_jsonobj.get("respiratory_rate", {}).get("timestamps", None) 
            total_res_rates = old_res_rates + new_res_rates
            total_res_rates_timestamps = old_res_rates_timestamps + new_res_rates_timestamps
            print('timestamps retrieved', old_res_rates, old_res_rates_timestamps)

            old_oxygen_saturation = processed_jsonobj.get("oxygen_saturation", {}).get("values", None) 
            old_oxygen_saturation_timestamps = processed_jsonobj.get("oxygen_saturation", {}).get("timestamps", None) 
            print('empty bloodox retrieved', old_oxygen_saturation, old_oxygen_saturation_timestamps)

            aggregate_json = { 
                "respiratory_rate": {
                    "values": total_res_rates,
                    "timestamps": total_res_rates_timestamps
                },
                "oxygen_saturation": {
                    "values": old_oxygen_saturation,
                    "timestamps": old_oxygen_saturation_timestamps
                }
            }

        except: 
            aggregate_json = {
                "respiratory_rate": {
                    "values": new_res_rates,
                    "timestamps": new_res_rates_timestamps
                },
                "oxygen_saturation": {
                    "values": [],
                    "timestamps": []
                }           
            }
            print('no existing JSON, new sensor file wih res_rates created', aggregate_json)

    elif bloodox_exists==True: 
        try: 
            processed_response = s3.get_object(Bucket=bucket, Key=key)
            processed_content = processed_response["Body"]
            processed_jsonobj = json.loads(processed_content.read())
            print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
            old_res_rates = processed_jsonobj.get("respiratory_rate", {}).get("values", None) 
            old_res_rates_timestamps = processed_jsonobj.get("respiratory_rate", {}).get("timestamps", None) 
            print('res rates', old_res_rates, old_res_rates_timestamps)

            old_oxygen_saturation = processed_jsonobj.get("oxygen_saturation", {}).get("values", None) 
            old_oxygen_saturation_timestamps = processed_jsonobj.get("oxygen_saturation", {}).get("timestamps", None) 
            print('old ox rates', old_oxygen_saturation, old_oxygen_saturation_timestamps)
            total_oxygen_saturation = old_oxygen_saturation + new_oxygen_saturation
            total_oxygen_saturation_timestamps = old_oxygen_saturation_timestamps + new_oxygen_saturation_timestamps
            print('total ox', total_oxygen_saturation, total_oxygen_saturation_timestamps)


            aggregate_json = { 
                "respiratory_rate": {
                    "values": old_res_rates,
                    "timestamps": old_res_rates_timestamps
                },
                "oxygen_saturation": {
                    "values": total_oxygen_saturation,
                    "timestamps": total_oxygen_saturation_timestamps
                }
            }

        except: 
            print('running except block')
            aggregate_json = {
                "respiratory_rate": {
                    "s": [],
                    "timestamps": []
                },
                "oxygen_saturation": {
                    "values": new_oxygen_saturation,
                    "timestamps": new_oxygen_saturation_timestamps
                }           
            }
            print('no existing JSON, new sensor file wih bloodox created', aggregate_json)

    finalData = json.dumps(aggregate_json).encode("UTF-8")
    s3.put_object(Body=finalData, Bucket=bucket, Key=key)
    print("JSON file uploaded successfully.")
    return finalData
