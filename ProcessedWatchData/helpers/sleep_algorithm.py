import json
import boto3
s3 = boto3.client('s3')

def sleep_analysis_function(mobile_bucket, acc_data, sleep_data, sleep_file_key): 

    try: 
        #acc_data variable has all acc data 
        #run through desired sleep algorithm for past 15 minutes of acc data

        print('sleep results available')
        # store results like the following dummy data: 
        new_sleep_results = {
            "episodes": 
            [
                {"asleep": True, "start_time": "2022-06-12T10:33:25", "end_time": "2022-06-13T10:33:25"},
                {"asleep": False, "start_time": "2022-06-12T10:33:25", "end_time": "2022-06-13T10:33:25"}, 
                {"asleep": True, "start_time": "2022-06-12T10:33:25", "end_time": "2022-06-13T10:33:25"}, 
                {"asleep": False, "start_time": "2022-06-12T10:33:25", "end_time": "2022-06-13T10:33:25"}
            ]
        }
        sleep_array = sleep_data['episodes']
        new_sleep_array = new_sleep_results['episodes']
        sleep_data['episodes'] = sleep_array + new_sleep_array
        jsonData = json.dumps(sleep_data).encode("UTF-8")
        s3.put_object(Body=jsonData, Bucket=mobile_bucket, Key=sleep_file_key)
        print("new JSON file uploaded successfully.")
        return sleep_data

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(sensor_data_key, model_bucket))
        raise e    

    