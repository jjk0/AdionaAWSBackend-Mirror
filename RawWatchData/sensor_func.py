import json
import boto3
s3 = boto3.client('s3')

def sensor_function(bucket, key, data): 

    # run data variable through other data manipulation function here 
    # output format TBD
    # dummy data:
    # results = {
    #     "id": "11111",
    #     "type": "refund",
    #     "amount": 1.22,
    #     "date": "2022-06-09T06:19:04Z"
    # }

    try: 
        processed_response = s3.get_object(Bucket=bucket, Key=key)
        processed_content = processed_response["Body"]
        processed_jsonobj = json.loads(processed_content.read())
        print('Sensor JSON from processed s3 retrieved:', processed_jsonobj)
    except: 
        processed_jsonobj = []
        print('no existing JSON, new sensor file created', processed_jsonobj)
    
    processed_jsonobj.append(data) 
    finalData = json.dumps(processed_jsonobj).encode("UTF-8")
    s3.put_object(Body=finalData, Bucket=bucket, Key=key)
    print("JSON file uploaded successfully.")
    return finalData