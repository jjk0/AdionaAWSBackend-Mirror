import json
from operator import truediv
import boto3
import pickle 
s3 = boto3.client('s3')

def agitation_function(bucket, trained_model_key, ground_truth_key, displayed_data_key, data): 

    try: 
        ground_truth = s3.get_object(Bucket=bucket, Key=ground_truth_key)
        processed_ground_truth = ground_truth["Body"]
        json_ground_truth = json.loads(processed_ground_truth.read())
        print('Ground truth agitation JSON from processed s3 retrieved:', json_ground_truth)
    
        if len(json_ground_truth) > 15:
            print('json ground truth is less than 15')
            return json_ground_truth
        else: 
            # preprocess data (aka raw_jsonobj) here 
            dummy_val = data 
            dummy_val = "placeholder"
            print('the data is longer than 15')
            # retrieve model and run processed data through model below 
            ag_algorithm = s3.get_object(Bucket="adiona-trained-models", Key=trained_model_key)
            
            # processed_ag_algorithm = ag_algorithm["Body"]
            # loaded_model = pickle.load(open(processed_ag_algorithm, 'rb'))
            # result = loaded_model.score(x_data, y_data)
            # https://cloud.google.com/ai-platform/prediction/docs/exporting-for-prediction#pickle
            # https://datascience.stackexchange.com/questions/71880/upload-model-to-s3 

            # formatted_result = results <some formatting function> (dummy formatted_result below)

            formatted_result = {
                "agitation": "",
                "time": ""
            }

            formatted_result["agitation"] = "true"
            formatted_result["time"] = "2022-06-12T10:33:25"
            print
            if formatted_result["agitation"] == "true":
                try: 
                    displayed_agitation = s3.get_object(Bucket=bucket, Key=displayed_data_key)
                    processed_displayed_truth = displayed_agitation["Body"]
                    json_displayed_truth = json.loads(processed_displayed_truth.read())
                    print('Agitation JSON from processed s3 retrieved:', json_displayed_truth)
                    json_displayed_truth.append(formatted_result)
                    finalData = json.dumps(json_displayed_truth).encode("UTF-8")
                    s3.put_object(Body=finalData, Bucket=bucket, Key=displayed_data_key)
                    print("JSON file uploaded successfully.")
                    return finalData
                except: 
                    json_displayed_truth = [] 
                    json_displayed_truth.append(formatted_result)
                    finalData = json.dumps(json_displayed_truth).encode("UTF-8")
                    s3.put_object(Body=finalData, Bucket=bucket, Key=displayed_data_key)
                    print('no existing displayed truth JSON, new file created')
                    return finalData
        
    except Exception as e: 
        print(e)
        json_ground_truth = []
        print('no existing ground truth data, new file created', json_ground_truth)
        finalData = json.dumps(json_ground_truth).encode("UTF-8")
        s3.put_object(Body=finalData, Bucket=bucket, Key=ground_truth_key)
        print("JSON file uploaded successfully.")
        return finalData