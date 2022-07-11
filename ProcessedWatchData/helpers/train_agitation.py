import json
import pickle 
import boto3
import pandas as pd 
from timesmash import Quantizer, SymbolicDerivative
from sklearn.ensemble import RandomForestClassifier
import time 
import datetime 
s3 = boto3.client('s3')

def train_agitation_function(from_bucket, model_bucket, sensor_data_key, ground_truth_data_key, model_file_key, quantizer_file_key): 

    # retrieve sensor and ground truth data 
    # train model 
    # export model and quantizer as pkl 

    try: 
        raw_sensor_data = s3.get_object(Bucket=from_bucket, Key=sensor_data_key)
        processed_sensor_data = raw_sensor_data["Body"]
        raw_ground_truth_data = s3.get_object(Bucket=from_bucket, Key=ground_truth_data_key)
        processed_ground_truth_data = raw_ground_truth_data["Body"]
        sensor_data = json.loads(processed_sensor_data.read())
        ground_truth_data = json.loads(processed_ground_truth_data.read())['ground_truth']
        print('Sensor data retrieved:', sensor_data)
        print('Ground truth data retrieved:', ground_truth_data)

        ACC_TYPES = ['x_val', 'y_val', 'z_val']
        acc_data = sensor_data['acceleration']

        def normalize(df): 
            return (df - df.mean() / df.std() )

        # temp fix for the imbalance in timestamps vs. acc data points 
        num_timestamps = len(acc_data['timestamps'])
        for acc in ACC_TYPES: 
            acc_data[acc] = acc_data[acc][:num_timestamps]

        acc_df = pd.DataFrame(acc_data)[ACC_TYPES]  

        # define agitation timestamps in Unix 
        unix_agitation_timestamps = [time\
            .mktime(datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")\
            .timetuple()) for ts in ground_truth_data]

        # determine which rows of acc_df are agitation, which not 
        labels = [any([(ts >= acc_ts and ts <= acc_ts + 50) \
            for acc_ts in unix_agitation_timestamps]) for ts in acc_data['timestamps']]

        print("HERE")

        # quantize 
        _qtz = Quantizer(n_quantizations = 2) 
        quantized_train = _qtz.\
            fit_transform(normalize(acc_df), \
            label=labels)

        final_train = pd.concat([q for q in quantized_train], axis=1)
        # TODO: bring this back and test for non-repetitive data 
        # train_features, _ = SymbolicDerivative().fit_transform(
        #     train=q_train, test=None, label=labels
        # ) 

        print("HERE 2")

        model = RandomForestClassifier(
            n_estimators=1000,
            max_depth=None,
            min_samples_leaf=70,
            class_weight = {
                True: 180, 
                False: 1
            },
            verbose=2,
            random_state=42
        ).fit(final_train, labels)
        model=sensor_data

        print('Model trained successfully.')
        uploadable_model = pickle.dumps(model)
        s3.put_object(Body=uploadable_model, Bucket=model_bucket, Key=model_file_key)
        print('Model uploaded to S3 bucket successfully.')

        uploadable_quantizer = pickle.dumps(_qtz) 
        s3.put_object(Body=uploadable_quantizer, Bucket=model_bucket, Key=quantizer_file_key)
        print('Quantizer uploaded to S3 bucket successfully.')
        return model

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(sensor_data_key, model_bucket))
        raise e    

    