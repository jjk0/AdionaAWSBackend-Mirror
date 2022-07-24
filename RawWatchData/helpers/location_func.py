from dateutil import parser
import time 
import json
import boto3
s3 = boto3.client('s3')

def location_function(bucket, key, data): 

    new_longitude = data.get("locations", {}).get("longitude", None)
    new_latitude = data.get("locations", {}).get("latitude", None)
    new_time = data.get("locations", {}).get("timestamp", None) 
    new_location_timestamps = [] 
    for val in new_time: 
        parsed_time = parser.parse(val)
        unix = time.mktime(parsed_time.timetuple())
        new_location_timestamps.append(unix)
        print(new_location_timestamps)

    try: 
        processed_response = s3.get_object(Bucket=bucket, Key=key)
        processed_content = processed_response["Body"]
        processed_jsonobj = json.loads(processed_content.read())
        print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
        old_longitude = processed_jsonobj.get("locations", {}).get("longitude", None) 
        old_latitude = processed_jsonobj.get("locations", {}).get("latitude", None) 
        old_timestamps = processed_jsonobj.get("locations", {}).get("timestamps", None) 
        all_longitude = old_longitude + new_longitude
        all_latitude = old_latitude + new_latitude
        total_location_timestamps = old_timestamps + new_location_timestamps

        aggregate_json = { 
            "locations": {
                "longitude": all_longitude,
                "latitude": all_latitude,
                "timestamps": total_location_timestamps
            },
        }

    except: 
        aggregate_json = {
            "locations": {
                "longitude": new_longitude,
                "latitude": new_latitude,
                "timestamps": new_location_timestamps
            },
        }
        print('no existing JSON, new location file created', aggregate_json)

    finalData = json.dumps(aggregate_json).encode("UTF-8")
    s3.put_object(Body=finalData, Bucket=bucket, Key=key)
    print("JSON location file uploaded successfully.")
    return finalData
