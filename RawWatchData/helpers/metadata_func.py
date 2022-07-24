from dateutil import parser
import time 
import json
import boto3
s3 = boto3.client('s3')

def metadata_function (bucket, key, data): 

    device_ID = data.get("metaData", {}).get("device_ID", None)
    new_connectivity = data.get("metaData", {}).get("connectivity_status", None) 
    new_time = data.get("metaData", {}).get("start_date", None)

    new_metadata_timestamps = [] 
    parsed_time = parser.parse(new_time)
    unix = time.mktime(parsed_time.timetuple())
    new_metadata_timestamps.append(unix)
    print(new_metadata_timestamps)

    try: 
        processed_response = s3.get_object(Bucket=bucket, Key=key)
        processed_content = processed_response["Body"]
        processed_jsonobj = json.loads(processed_content.read())
        print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
        old_device_ID = processed_jsonobj.get("metadata", {}).get("device_ID", None) 
        old_connectivity_status = processed_jsonobj.get("metadata", {}).get("connectivity_status", None) 
        old_start_times = processed_jsonobj.get("metadata", {}).get("start_date", None) 
        all_device_ID = old_device_ID + device_ID
        all_connectivity_status = old_connectivity_status + new_connectivity
        total_metadata_timestamps = old_start_times + new_metadata_timestamps

        aggregate_json = { 
            "metadata": {
                "device_ID": all_device_ID,
                "connectivity_status": all_connectivity_status,
                "start_date": total_metadata_timestamps
            },
        }

    except: 
        print('entered except block')
        aggregate_json = { 
            "metadata": {
                "device_ID": device_ID,
                "connectivity_status": new_connectivity,
                "start_date": new_metadata_timestamps
            },
        }
        print('no existing JSON, new metadata file created', aggregate_json)

    finalData = json.dumps(aggregate_json).encode("UTF-8")
    s3.put_object(Body=finalData, Bucket=bucket, Key=key)
    print("JSON metadata file uploaded successfully.")
    return finalData
