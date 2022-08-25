from concurrent.futures import process
import json
from re import template
import urllib.parse
import boto3
from string import Template 
# from helpers.train_agitation import train_agitation_function
# from helpers.sleep_algorithm import sleep_analysis_function
from helpers.tips import tips_function
from helpers.agitation_tips import agitation_tips_function
from helpers.heart_tips import hr_tips_function
from helpers.lifestyle_tips import lifestyle_tips_function
from helpers.mobility_tips import mobility_tips_function
# from helpers.create_agitation_master import create_agitation_master_file


##### NEED TO GET DYNAMODB DATA TO SEE MANUALLY UPLOADED AGITATION 
##### SET UP SEPARATE LAMBDA ON DYNAMO TO WRITE TO MOBILE APP BUCKET 

print('Loading function')

s3 = boto3.client('s3')
# dynamo = boto3.client('dynamodb')


def lambda_handler(event, context):
    processed_bucket = event['Records'][0]['s3']['bucket']['name']
    processed_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(processed_bucket) 
    print(processed_key) 
    mobile_bucket = "mobile-app-ready-data"
    trained_model_bucket = "adiona-trained-models"
    dynamo_geofences_table = "GeoFence-o76lfmasxnec5ftzmzuynnxuhi-dev"
    dynamo_agitation_table = "PatientAgitation-o76lfmasxnec5ftzmzuynnxuhi-dev"
    dynamo_watch_data_table = 'PatientWatchData-o76lfmasxnec5ftzmzuynnxuhi-dev'

    
    print("processed key", processed_key)
    id = processed_key[0:5]

    def create_string(filename): 
        template_str = Template('$ID/$filename')
        file_key = template_str.substitute(ID=id, filename=filename)
        return file_key

    # def get_file(bucket, file_key): 
    #     try: 
    #         raw_response = s3.get_object(Bucket=bucket, Key=file_key)
    #         raw_content = raw_response["Body"]
    #         processed_bucket_data = json.loads(raw_content.read())
    #         # print('JSON from raw s3 retrieved:', processed_bucket_data)
    #         return processed_bucket_data
    #     except Exception as e: 
    #         print(e)
    #         print("The ", file_key, " file does not exist.")

    sensor_file_key = create_string('accData.json')
    truth_file_key = create_string('agitationGroundTruth.json')
    model_file_key = create_string('trainedModel.pkl.json')
    quantizer_file_key = create_string('fittedQuantizer.json')
    derivative_file_key = create_string('fittedDerivative.json')
    ag_ground_truth_file_key = create_string('agitationGroundTruth.json')
    ag_displayed_file_key = create_string('predictedAgitation.json')
    alg_file_key = create_string('trainedModel.pkl')
    quantizer_file_key = create_string('fittedQuantizer.pkl')
   
    master_agitation_file_key = create_string('masterAgitation.json')
    sleep_file_key = create_string('sleepData.json')
    lifestyle_file_key = create_string('lifestyleData.json')
    heart_file_key = create_string('hrData.json')
    mobility_file_key = create_string('mobilityData.json')
    
    tips_input_data={
       'agitation': master_agitation_file_key,
       'sleep': sleep_file_key,
       'lifestyle': lifestyle_file_key,
       'heart': heart_file_key,
       'mobility': mobility_file_key
    }

    # try: 
        # data = dynamo.get_item(
        #     TableName=dynamo_geofences_table,
        #     Key={
        #         'id': {
        #         'S': '005'
        #         }
        #     }
        # )

        # item = dynamo_watch_data_table.get_item(Key={
        #     'id': id,
        # })

        # response = {
        #     'statusCode': 200,
        #     'body': json.dumps(data),
        #     'headers': {
        #         'Content-Type': 'application/json',
        #         'Access-Control-Allow-Origin': '*'
        #     },
        # }
        # print('dynamo call worked', item)
    # except:
    #     print('dynamo call failed')
  


    try: 
        raw_response = s3.get_object(Bucket=processed_bucket, Key=processed_key)
        raw_content = raw_response["Body"]
        raw_jsonobj = json.loads(raw_content.read())
        print('JSON from raw s3 retrieved:')

        # agitation_model = train_agitation_function(processed_bucket, trained_model_bucket, sensor_file_key, truth_file_key, model_file_key, quantizer_file_key, derivative_file_key)

    except Exception as e: 
        print(e)
        print('Agitation training unsuccessful.')
    
    try: 
        tips_results = tips_function(
            processed_bucket, mobile_bucket, 
            tips_input_data, 
            agitation_tips_function,
            hr_tips_function,
            lifestyle_tips_function,
            mobility_tips_function
        )
        print('tips results', tips_results)
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(processed_key, processed_bucket))
        raise e    




