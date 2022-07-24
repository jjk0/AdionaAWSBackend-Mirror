from dateutil import parser
import time 
import json
import boto3
s3 = boto3.client('s3')

def lifestyle_function(bucket, key, data): 
    try: 
        new_steps = data.get("step_count", {}).get("values", None)
        steps_times = data.get("step_count", {}).get("timestamps", None) 
        new_steps_timestamps = [] 

        for val in steps_times: 
            parsed_time = parser.parse(val)
            unix = time.mktime(parsed_time.timetuple())
            new_steps_timestamps.append(unix)
            print(new_steps_timestamps)
        steps_exists = True 

        if len(new_steps_timestamps) < 1:
            steps_exists = False 
            print("No steps available in this file.")


    except: 
        steps_exists = False 
        print("No steps available in this file.")

    try: 
        new_active_energy_burned = data.get("active_energy_burned", {}).get("values", None)
        active_energy_burned_times = data.get("active_energy_burned", {}).get("timestamps", None) 
        new_energy_burned_timestamps = [] 
        print('res rate times', active_energy_burned_times)

        for val in active_energy_burned_times: 
            parsed_time = parser.parse(val)
            unix = time.mktime(parsed_time.timetuple())
            new_energy_burned_timestamps.append(unix)
            print(new_energy_burned_timestamps)
        energy_exists = True 

        if len(active_energy_burned_times) < 1:
            energy_exists = False 
            print("No energy available in this file.")

    except: 
        energy_exists = False 
        print("No active energy available in this file.")

    if ((steps_exists==True) and (energy_exists==True)): 

        try: 
            processed_response = s3.get_object(Bucket=bucket, Key=key)
            processed_content = processed_response["Body"]
            processed_jsonobj = json.loads(processed_content.read())
            print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
            old_steps = processed_jsonobj.get("step_count", {}).get("values", None) 
            old_steps_timestamps = processed_jsonobj.get("step_count", {}).get("timestamps", None) 

            total_steps = old_steps + new_steps
            total_steps_timestamps = old_steps_timestamps + new_steps_timestamps

            old_energy_burned = processed_jsonobj.get("active_energy_burned", {}).get("values", None) 
            old_energy_burned_timestamps = processed_jsonobj.get("active_energy_burned", {}).get("timestamps", None) 
            total_energy_burned = old_energy_burned + new_active_energy_burned
            total_energy_burned_timestamps = old_energy_burned_timestamps + new_energy_burned_timestamps


            aggregate_json = { 
                "step_count": {
                    "values": total_steps,
                    "timestamps": total_steps_timestamps
                },
                "active_energy_burned": {
                    "values": total_energy_burned,
                    "timestamps": total_energy_burned_timestamps
                }
            }

        except: 
            aggregate_json = {
                "step_count": {
                    "values": new_steps,
                    "timestamps": new_steps_timestamps
                },
                "active_energy_burned": {
                    "values": new_active_energy_burned,
                    "timestamps": new_energy_burned_timestamps
                }           
            }
            print('no existing JSON, new sensor file wih steps and energy created', aggregate_json)
        
    elif steps_exists==True: 

        try: 
            processed_response = s3.get_object(Bucket=bucket, Key=key)
            processed_content = processed_response["Body"]
            processed_jsonobj = json.loads(processed_content.read())
            print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
            old_steps = processed_jsonobj.get("step_count", {}).get("values", None) 
            old_steps_timestamps = processed_jsonobj.get("step_count", {}).get("timestamps", None) 
            total_steps = old_steps + new_steps
            total_steps_timestamps = old_steps_timestamps + new_steps_timestamps
            print('timestamps retrieved', old_steps, old_steps_timestamps)

            old_energy_burned = processed_jsonobj.get("active_energy_burned", {}).get("values", None) 
            old_energy_burned_timestamps = processed_jsonobj.get("active_energy_burned", {}).get("timestamps", None) 
            print('empty energy retrieved', old_energy_burned, old_energy_burned_timestamps)

            aggregate_json = { 
                "step_count": {
                    "values": total_steps,
                    "timestamps": total_steps_timestamps
                },
                "active_energy_burned": {
                    "values": old_energy_burned,
                    "timestamps": old_energy_burned_timestamps
                }
            }

        except: 
            aggregate_json = {
                "step_count": {
                    "values": new_steps,
                    "timestamps": new_steps_timestamps
                },
                "active_energy_burned": {
                    "values": [],
                    "timestamps": []
                }           
            }
            print('no existing JSON, new sensor file wih steps created', aggregate_json)

    elif energy_exists==True: 
        try: 
            processed_response = s3.get_object(Bucket=bucket, Key=key)
            processed_content = processed_response["Body"]
            processed_jsonobj = json.loads(processed_content.read())
            print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
            old_steps = processed_jsonobj.get("step_count", {}).get("values", None) 
            old_steps_timestamps = processed_jsonobj.get("step_count", {}).get("timestamps", None) 

            old_energy_burned = processed_jsonobj.get("active_energy_burned", {}).get("values", None) 
            old_energy_burned_timestamps = processed_jsonobj.get("active_energy_burned", {}).get("timestamps", None) 
            total_energy_burned = old_energy_burned + new_active_energy_burned
            total_energy_burned_timestamps = old_energy_burned_timestamps + new_energy_burned_timestamps


            aggregate_json = { 
                "step_count": {
                    "values": old_steps,
                    "timestamps": old_steps_timestamps
                },
                "active_energy_burned": {
                    "values": total_energy_burned,
                    "timestamps": total_energy_burned_timestamps
                }
            }

        except: 
            aggregate_json = {
                "step_count": {
                    "values": [],
                    "timestamps": []
                },
                "active_energy_burned": {
                    "values": new_active_energy_burned,
                    "timestamps": new_energy_burned_timestamps
                }           
            }
            print('no existing JSON, new sensor file wih steps and energy created', aggregate_json)

    finalData = json.dumps(aggregate_json).encode("UTF-8")
    s3.put_object(Body=finalData, Bucket=bucket, Key=key)
    print("JSON file uploaded successfully.")
    return finalData
