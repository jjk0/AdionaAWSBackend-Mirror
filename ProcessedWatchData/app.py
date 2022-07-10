import json
from re import template
import urllib.parse
import boto3
from string import Template 
# from helpers.train_agitation import train_agitation_function
# from helpers.sleep_algorithm import sleep_analysis_function
# from helpers.tips import tips_function
from helpers.create_agitation_master import create_agitation_master_file

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    processed_bucket = event['Records'][0]['s3']['bucket']['name']
    processed_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    mobile_bucket = "mobile-app-ready-data"
    
    print("processed key", processed_key)
    id = processed_key[0:5]

    def create_string(filename): 
        template_str = Template('$ID/$filename')
        file_key = template_str.substitute(ID=id, filename=filename)
        return file_key

    def get_file(bucket, file_key): 
        try: 
            raw_response = s3.get_object(Bucket=bucket, Key=file_key)
            raw_content = raw_response["Body"]
            processed_bucket_data = json.loads(raw_content.read())
            # print('JSON from raw s3 retrieved:', processed_bucket_data)
            return processed_bucket_data
        except Exception as e: 
            print(e)
            print("The ", file_key, " file does not exist.")
    
    # From processed-adiona-watch-app-data bucket, get the following files: 
    sensor_file_key = create_string("accData.json")
    lifestyle_file_key = create_string("lifestyleData.json")
    hr_file_key = create_string("hrData.json")
    res_file_key = create_string("respiratoryData.json")

    # From adiona-trained-models bucket, get the following files: 
    agitation_model = create_string("trainedModel.pkl")

    # From mobile-app-ready-data bucket, get the following files: 
    sleep_file_key = create_string("sleepData.json")
    ground_truth_ag_file_key = create_string("agitationGroundTruth.json")
    predicted_ag_file_key = create_string("predictedAgitation.json")
    corrected_ag_file_key = create_string("correctedAgitation.json")
    master_ag_file_key = create_string("masterAgitation.json")
    tips_file_key = create_string("tips.json")

    try: 
        acc_data = get_file(processed_bucket, sensor_file_key)
        lifestyle_data = get_file(processed_bucket, lifestyle_file_key)
        hr_data = get_file(processed_bucket, hr_file_key)
        res_data = get_file(processed_bucket, res_file_key)
        sleep_data = get_file(mobile_bucket, sleep_file_key)
        ground_truth_agitation = get_file(mobile_bucket, ground_truth_ag_file_key)
        predicted_agitation = get_file(mobile_bucket, predicted_ag_file_key)
        corrected_agitation = get_file(mobile_bucket, corrected_ag_file_key)
        master_agitation = get_file(mobile_bucket, master_ag_file_key)

        agitation_data = [ground_truth_agitation, predicted_agitation, corrected_agitation]
        tips_data = [lifestyle_data, hr_data, res_data, sleep_data, master_agitation]
        print("function makes it to here.", tips_data)

        # agitation_master_data = create_agitation_master_file(mobile_bucket, agitation_data, master_ag_file_key)
        # print('Agitation master function runs. See the results here:', agitation_master_data)

        # sleep_results = sleep_analysis_function(mobile_bucket, acc_data, sleep_data, sleep_file_key)
        # tips_results = tips_function(processed_bucket, mobile_bucket, tips_data)

        # agitation_model_results = train_agitation_function(processed_bucket, trained_model_bucket, sensor_file_key, ground_truth_ag_file_key, agitation_model)
        # print('FUNCTION EXECUTED SUCCESSFULLY:', agitation_model_results)


        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(processed_key, processed_bucket))
        raise e    
