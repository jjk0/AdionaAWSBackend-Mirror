import json
import boto3
s3 = boto3.client('s3')
from string import Template 

def create_agitation_master_file(bucket, all_agitation_files, master_key): 

    try: 
        ground_truth_agitation = all_agitation_files[0]
        predicted_agitation = all_agitation_files[1]
        corrected_agitation = all_agitation_files[2]
        master = s3.get_object(Bucket=bucket, Key=master_key)
        processed_data = master["Body"]
        readable_data = json.loads(processed_data.read())
        print(Template('Data from $master_key retrieved successfully.'))

        predicted_agitation_array = predicted_agitation['episodes']
        false_positives = corrected_agitation['false_positives']
        false_negatives = corrected_agitation['false_negatives']
        for false_positive in false_positives:
            predicted_agitation_array.remove(false_positive)
        master_data = ground_truth_agitation['ground_truth'] + predicted_agitation_array + false_negatives
        print('MASTER DATA HERE! Should be longer than 1.')
        readable_data['episodes'] = master_data
        jsonData = json.dumps(readable_data).encode("UTF-8")
        s3.put_object(Body=jsonData, Bucket=bucket, Key=master_key)
        print("JSON file uploaded successfully.")
        return readable_data

    except: 
        print(Template("No master file $master_key exists."))
        master_data = {
            "episodes": []
        }       
        print('New master file created', master_data)
        jsonData = json.dumps(master_data).encode("UTF-8")
        s3.put_object(Body=jsonData, Bucket=bucket, Key=master_key)
        print("new JSON file uploaded successfully.")
        return master_data
    # this is dangerous because you don't handle cases where the initial try call fails due to other factors than the file not existing   