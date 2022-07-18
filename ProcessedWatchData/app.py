import json
from re import template
import urllib.parse
import boto3
from string import Template 
from helpers.train_agitation import train_agitation_function
# from helpers.sleep_algorithm import sleep_analysis_function
# from helpers.tips import tips_function
from helpers.create_agitation_master import create_agitation_master_file

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    processed_bucket = event['Records'][0]['s3']['bucket']['name']
    processed_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    print(processed_bucket) 
    print(processed_key) 
    mobile_bucket = "mobile-app-ready-data"
    trained_model_bucket = "adiona-trained-models"
    
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
    
    id = processed_key[0:5]
    sensor_template_str = Template('$ID/accData.json')
    sensor_file_key = sensor_template_str.substitute(ID=id)
    truth_template_str = Template('$ID/agitationGroundTruth.json')
    truth_file_key = truth_template_str.substitute(ID=id)
    model_template_str = Template('$ID/trainedModel.pkl')
    model_file_key = model_template_str.substitute(ID=id)
    quantizer_template_str = Template('$ID/fittedQuantizer.pkl')
    quantizer_file_key = quantizer_template_str.substitute(ID=id)
    derivative_template_str = Template('$ID/fittedDerivative.pkl')
    derivative_file_key = derivative_template_str.substitute(ID=id)
   
    try: 
        raw_response = s3.get_object(Bucket=processed_bucket, Key=processed_key)
        raw_content = raw_response["Body"]
        raw_jsonobj = json.loads(raw_content.read())
        # print('JSON from raw s3 retrieved:', raw_jsonobj)

        agitation_model = train_agitation_function(processed_bucket, trained_model_bucket, sensor_file_key, truth_file_key, model_file_key, quantizer_file_key, derivative_file_key)

        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(processed_key, processed_bucket))
        raise e    
