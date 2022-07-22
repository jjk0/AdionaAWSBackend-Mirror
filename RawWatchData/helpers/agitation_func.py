import json
from operator import truediv
import boto3
import pickle 
from datetime import timedelta
import datetime 
from dateutil import parser
import time 
import pandas as pd 
s3 = boto3.client('s3')

def agitation_function(bucket, trained_model_key, quantizer_file_key, ground_truth_key, displayed_data_key, data): 

    try: 
        print(bucket) 
        print(ground_truth_key) 
        ground_truth = s3.get_object(Bucket=bucket, Key=ground_truth_key)
        processed_ground_truth = ground_truth["Body"]
        json_ground_truth = json.loads(processed_ground_truth.read())
        print('Ground truth agitation JSON from processed s3 retrieved:', json_ground_truth)
        ground_truth_array = json_ground_truth.get("ground_truth", {})
    
        if len(ground_truth_array) < 5:
            print('json ground truth is less than 5. No prediction attempted.')
            return json_ground_truth
        else: 
            new_x = data.get("acceleration", {}).get("x_val", None)
            new_y = data.get("acceleration", {}).get("y_val", None)
            new_z = data.get("acceleration", {}).get("z_val", None)
            freq = data.get("acceleration", {}).get("frequency", None)
            str_date = data.get("acceleration", {}).get("startQueryTime", None) 
            if not str_date: 
                str_date = str(datetime.datetime.now() ) 
            new_date = parser.parse(str_date)
            new_timestamps = []
            time_val = 0 

            # for x in new_x: 
            #     incremented_date = new_date + timedelta(seconds = time_val/freq)
            #     unix = time.mktime(incremented_date.timetuple())
            #     new_timestamps.append(unix)
            #     time_val += 1 

            # retrieve model and run processed data through model below 
            try: 
                pickled_qtz = s3.get_object(Bucket="adiona-trained-models", Key=quantizer_file_key)
                pickled_ag_algorithm = s3.get_object(Bucket="adiona-trained-models", Key=trained_model_key)
                _qtz = pickle.loads(pickled_qtz["Body"].read())
                model = pickle.loads(pickled_ag_algorithm["Body"].read())
                print('this is the model', model)

                test_data = {
                    'x_val': new_x, 
                    'y_val': new_y, 
                    'z_val': new_z 
                }
                test_df = pd.DataFrame(test_data)

                # TODO: should normalize in consistent fashion 
                def normalize(df): 
                    return (df - df.mean() / df.std() )
                quantized_test = _qtz.transform(normalize(test_df))
                final_test = pd.concat([q for q in quantized_test], axis=1)
                # in future, add symbolic derivative 
                print('model again', model)
                predicted_labels = model.predict(final_test)

                if sum(predicted_labels) > 0: 
                    print("predicted agitation")
                    return (True, str_date) 
                else: 
                    print('no agitation')
                    return (False, str_date)

            except Exception as e:
                print(e)
                print('No trained agitation model available.')
                return 
        

            if result[0] == True:
                try: 
                    displayed_agitation = s3.get_object(Bucket=bucket, Key=displayed_data_key)
                    processed_displayed_truth = displayed_agitation["Body"]
                    alg_predicted_agitation = json.loads(processed_displayed_truth.read())
                    print('Agitation JSON from processed s3 retrieved:', alg_predicted_agitation)
                    old_episodes = alg_predicted_agitation.get("episodes", {})
                    old_episodes.append(result[1])
                    
                    alg_predicted_agitation = {
                        "episodes": old_episodes
                    }

                    finalData = json.dumps(alg_predicted_agitation).encode("UTF-8")
                    s3.put_object(Body=finalData, Bucket=bucket, Key=displayed_data_key)
                    print("JSON file uploaded successfully.")
                    return finalData
                except: 
                    alg_predicted_agitation = {
                        "episodes": [result[1]],
                    } 
                    finalData = json.dumps(alg_predicted_agitation).encode("UTF-8")
                    s3.put_object(Body=finalData, Bucket=bucket, Key=displayed_data_key)
                    print('no existing displayed truth JSON, new file created')
                    return finalData
        
    except Exception as e: 
        print(e)
        json_ground_truth = {
            "ground_truth": [
                ("2022-06-12T10:33:25"),
                ("2022-06-12T10:33:25"),
                ("2022-06-12T10:33:25"),
                ("2022-06-12T10:33:25"),
                ("2022-06-12T10:33:25"),
                ("2022-06-12T10:33:25"),
                ("2022-06-12T10:33:25"),
                ("2022-06-12T10:33:25"),
                ("2022-06-12T10:33:25"),
            ]
        }
        print('no existing ground truth data, new file created', json_ground_truth)
        finalData = json.dumps(json_ground_truth).encode("UTF-8")
        s3.put_object(Body=finalData, Bucket=bucket, Key=ground_truth_key)
        print("new JSON file uploaded successfully.")
        return finalData