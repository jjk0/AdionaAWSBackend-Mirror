import json
from operator import truediv
import boto3
import pickle 
from datetime import timedelta
from dateutil import parser
import time 
s3 = boto3.client('s3')

def agitation_function(bucket, trained_model_key, ground_truth_key, displayed_data_key, data): 

    try: 
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
            new_date = parser.parse(str_date)
            new_timestamps = []
            time_val = 0 

            for x in new_x: 
                incremented_date = new_date + timedelta(seconds = time_val/freq)
                unix = time.mktime(incremented_date.timetuple())
                new_timestamps.append(unix)
                time_val += 1 

            # retrieve model and run processed data through model below 
            try: 
                ag_algorithm = s3.get_object(Bucket="adiona-trained-models", Key=trained_model_key)
                processed_ag_algorithm = ag_algorithm["Body"]
                # loaded_model = pickle.load(open(processed_ag_algorithm, 'rb'))
                # result = loaded_model.score(x_data, y_data)
                # https://cloud.google.com/ai-platform/prediction/docs/exporting-for-prediction#pickle
                # https://datascience.stackexchange.com/questions/71880/upload-model-to-s3 
                result = (True, "2022-06-12T10:33:25")
            except: 
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