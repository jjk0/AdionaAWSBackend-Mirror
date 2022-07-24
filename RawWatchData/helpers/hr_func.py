# 

# from dateutil import parser
# import time 
# import json
# import boto3
# s3 = boto3.client('s3')

# def hr_function(bucket, key, data): 

#     new_heart_rates = data.get("heart_rate", {}).get("values", None)
#     heart_rates_times = data.get("heart_rate", {}).get("timestamps", None) 
#     new_heart_rate_variability = data.get("heart_rate_variability", {}).get("values", None)
#     heart_rate_variability_times = data.get("heart_rate_variability", {}).get("timestamps", None) 

#     new_heart_rates_timestamps = [] 
#     print('hr rate times', heart_rates_times)
#     new_heart_rate_variability_timestamps = [] 
#     print('blood ox times', heart_rate_variability_times)

#     for val in heart_rates_times: 
#         parsed_time = parser.parse(val)
#         unix = time.mktime(parsed_time.timetuple())
#         new_heart_rates_timestamps.append(unix)
#         print(new_heart_rates_timestamps)
#     for val in heart_rate_variability_times: 
#         parsed_time = parser.parse(val)
#         unix = time.mktime(parsed_time.timetuple())
#         new_heart_rate_variability_timestamps.append(unix)
#         print(new_heart_rate_variability_timestamps)


#     try: 
#         processed_response = s3.get_object(Bucket=bucket, Key=key)
#         processed_content = processed_response["Body"]
#         processed_jsonobj = json.loads(processed_content.read())
#         print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
#         old_heart_rates = processed_jsonobj.get("heart_rate", {}).get("values", None) 
#         old_heart_rates_timestamps = processed_jsonobj.get("heart_rate", {}).get("timestamps", None) 

#         total_heart_rates = old_heart_rates + new_heart_rates
#         total_heart_rates_timestamps = old_heart_rates_timestamps + new_heart_rates_timestamps

#         old_heart_rate_variability = processed_jsonobj.get("heart_rate_variability", {}).get("values", None) 
#         old_heart_rate_variability_timestamps = processed_jsonobj.get("heart_rate_variability", {}).get("timestamps", None) 
#         total_heart_rate_variability = old_heart_rate_variability + new_heart_rate_variability
#         total_heart_rate_variability_timestamps = old_heart_rate_variability_timestamps + new_heart_rate_variability_timestamps


#         aggregate_json = { 
#             "heart_rate": {
#                 "value": total_heart_rates,
#                 "timestamps": total_heart_rates_timestamps
#             },
#             "heart_rate_variability": {
#                 "value": total_heart_rate_variability,
#                 "timestamps": total_heart_rate_variability_timestamps
#             }
#         }

#     except: 
#         aggregate_json = {
#             "heart_rate": {
#                 "value": new_heart_rates,
#                 "timestamps": new_heart_rates_timestamps
#             },
#             "heart_rate_variability": {
#                 "value": new_heart_rate_variability,
#                 "timestamps": new_heart_rate_variability_timestamps
#             }           
#         }
#         print('no existing JSON, new sensor file created', aggregate_json)

#     finalData = json.dumps(aggregate_json).encode("UTF-8")
#     s3.put_object(Body=finalData, Bucket=bucket, Key=key)
#     print("JSON file uploaded successfully.")
#     return finalData


from dateutil import parser
import time 
import json
import boto3
s3 = boto3.client('s3')

def hr_function(bucket, key, data): 
    try: 
        new_heart_rates = data.get("heart_rate", {}).get("values", None)
        heart_rates_times = data.get("heart_rate", {}).get("timestamps", None) 
        new_heart_rates_timestamps = [] 

        for val in heart_rates_times: 
            parsed_time = parser.parse(val)
            unix = time.mktime(parsed_time.timetuple())
            new_heart_rates_timestamps.append(unix)
            print(new_heart_rates_timestamps)
        heart_rates_exists = True 

        if len(new_heart_rates_timestamps) < 1:
            heart_rates_exists = False 
            print("No heart_rates available in this file.")

    except: 
        heart_rates_exists = False 
        print("No heart_rates available in this file.")

    try: 
        new_heart_rate_variability = data.get("heart_rate_variability", {}).get("values", None)
        heart_rate_variability_times = data.get("heart_rate_variability", {}).get("timestamps", None) 
        new_heart_rate_variability_timestamps = [] 
        print('hr rate times', heart_rate_variability_times)

        for val in heart_rate_variability_times: 
            parsed_time = parser.parse(val)
            unix = time.mktime(parsed_time.timetuple())
            new_heart_rate_variability_timestamps.append(unix)
            print(new_heart_rate_variability_timestamps)
        heart_rate_variability_exists = True 

        if len(heart_rate_variability_times) < 1:
            heart_rate_variability_exists = False 
            print("No bloodox available in this file.")
        print('makes it to here')
    except: 
        heart_rate_variability_exists = False 
        print("No bloodox available in this file.")

    if ((heart_rates_exists==True) and (heart_rate_variability_exists==True)): 

        try: 
            processed_response = s3.get_object(Bucket=bucket, Key=key)
            processed_content = processed_response["Body"]
            processed_jsonobj = json.loads(processed_content.read())
            print(type(processed_jsonobj))
            print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
            old_heart_rates = processed_jsonobj.get("heart_rate", {}).get("values", None) 
            if len(old_heart_rates) < 1: 
                old_heart_rates = [] 
            old_heart_rates_timestamps = processed_jsonobj.get("heart_rate", {}).get("timestamps", None) 

            total_heart_rates = old_heart_rates + new_heart_rates
            total_heart_rates_timestamps = old_heart_rates_timestamps + new_heart_rates_timestamps

            old_heart_rate_variability = processed_jsonobj.get("heart_rate_variability", {}).get("values", None) 
            if len(old_heart_rate_variability) < 1: 
                old_heart_rate_variability = [] 
            old_heart_rate_variability_timestamps = processed_jsonobj.get("heart_rate_variability", {}).get("timestamps", None) 
            total_heart_rate_variability = old_heart_rate_variability + new_heart_rate_variability
            total_heart_rate_variability_timestamps = old_heart_rate_variability_timestamps + new_heart_rate_variability_timestamps


            aggregate_json = { 
                "heart_rate": {
                    "values": total_heart_rates,
                    "timestamps": total_heart_rates_timestamps
                },
                "heart_rate_variability": {
                    "values": total_heart_rate_variability,
                    "timestamps": total_heart_rate_variability_timestamps
                }
            }

        except Exception as e: 
            print(e)
            aggregate_json = {
                "heart_rate": {
                    "values": new_heart_rates,
                    "timestamps": new_heart_rates_timestamps
                },
                "heart_rate_variability": {
                    "values": new_heart_rate_variability,
                    "timestamps": new_heart_rate_variability_timestamps
                }           
            }
            print('no existing JSON, new sensor file wih heart_rates and bloodox created', aggregate_json)
        
    elif heart_rates_exists==True: 

        try: 
            processed_response = s3.get_object(Bucket=bucket, Key=key)
            processed_content = processed_response["Body"]
            processed_jsonobj = json.loads(processed_content.read())
            print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
            old_heart_rates = processed_jsonobj.get("heart_rate", {}).get("values", None) 
            old_heart_rates_timestamps = processed_jsonobj.get("heart_rate", {}).get("timestamps", None) 
            total_heart_rates = old_heart_rates + new_heart_rates
            total_heart_rates_timestamps = old_heart_rates_timestamps + new_heart_rates_timestamps
            print('timestamps retrieved', old_heart_rates, old_heart_rates_timestamps)

            old_heart_rate_variability = processed_jsonobj.get("heart_rate_variability", {}).get("values", None) 
            old_heart_rate_variability_timestamps = processed_jsonobj.get("heart_rate_variability", {}).get("timestamps", None) 
            print('empty bloodox retrieved', old_heart_rate_variability, old_heart_rate_variability_timestamps)

            aggregate_json = { 
                "heart_rate": {
                    "values": total_heart_rates,
                    "timestamps": total_heart_rates_timestamps
                },
                "heart_rate_variability": {
                    "values": old_heart_rate_variability,
                    "timestamps": old_heart_rate_variability_timestamps
                }
            }

        except: 
            aggregate_json = {
                "heart_rate": {
                    "values": new_heart_rates,
                    "timestamps": new_heart_rates_timestamps
                },
                "heart_rate_variability": {
                    "values": [],
                    "timestamps": []
                }           
            }
            print('no existing JSON, new sensor file wih heart_rates created', aggregate_json)

    elif heart_rate_variability_exists==True: 
        try: 
            processed_response = s3.get_object(Bucket=bucket, Key=key)
            processed_content = processed_response["Body"]
            processed_jsonobj = json.loads(processed_content.read())
            print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
            old_heart_rates = processed_jsonobj.get("heart_rate", {}).get("values", None) 
            old_heart_rates_timestamps = processed_jsonobj.get("heart_rate", {}).get("timestamps", None) 
            print('hr rates', old_heart_rates, old_heart_rates_timestamps)

            old_heart_rate_variability = processed_jsonobj.get("heart_rate_variability", {}).get("values", None) 
            old_heart_rate_variability_timestamps = processed_jsonobj.get("heart_rate_variability", {}).get("timestamps", None) 
            print('old ox rates', old_heart_rate_variability, old_heart_rate_variability_timestamps)
            total_heart_rate_variability = old_heart_rate_variability + new_heart_rate_variability
            total_heart_rate_variability_timestamps = old_heart_rate_variability_timestamps + new_heart_rate_variability_timestamps
            print('total ox', total_heart_rate_variability, total_heart_rate_variability_timestamps)


            aggregate_json = { 
                "heart_rate": {
                    "values": old_heart_rates,
                    "timestamps": old_heart_rates_timestamps
                },
                "heart_rate_variability": {
                    "values": total_heart_rate_variability,
                    "timestamps": total_heart_rate_variability_timestamps
                }
            }

        except: 
            print('running except block')
            aggregate_json = {
                "heart_rate": {
                    "s": [],
                    "timestamps": []
                },
                "heart_rate_variability": {
                    "values": new_heart_rate_variability,
                    "timestamps": new_heart_rate_variability_timestamps
                }           
            }
            print('no existing JSON, new sensor file wih bloodox created', aggregate_json)

    finalData = json.dumps(aggregate_json).encode("UTF-8")
    s3.put_object(Body=finalData, Bucket=bucket, Key=key)
    print("JSON file uploaded successfully.")
    return finalData
