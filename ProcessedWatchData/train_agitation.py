import json
import pickle 
import boto3
s3 = boto3.client('s3')

def train_agitation_function(from_bucket, model_bucket, sensor_data_key, ground_truth_data_key, file_key): 

    # retrieve sensor and ground truth data 
    # train model 
    # export model as pkl 

    try: 
        raw_sensor_data = s3.get_object(Bucket=from_bucket, Key=sensor_data_key)
        processed_sensor_data = raw_sensor_data["Body"]
        raw_ground_truth_data = s3.get_object(Bucket=from_bucket, Key=ground_truth_data_key)
        processed_ground_truth_data = raw_ground_truth_data["Body"]
        sensor_data = json.loads(processed_ground_truth_data.read())
        ground_truth_data = json.loads(processed_sensor_data.read())
        print('Sensor data retrieved:', sensor_data)
        print('Ground truth data retrieved:', ground_truth_data)

        # train model 
        # store trained model in variable named model, dummy var below 
        model = sensor_data

        print('Model trained successfully.')
        uploadable_model = pickle.dumps(model)
        s3.put_object(Body=uploadable_model, Bucket=model_bucket, Key=file_key)
        print('Model uploaded to S3 bucket successfully.')
        return model

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(sensor_data_key, model_bucket))
        raise e    

    