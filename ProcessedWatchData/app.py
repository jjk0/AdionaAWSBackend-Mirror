import json
import urllib.parse
import boto3
from string import Template 
from train_agitation import train_agitation_function


print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    processed_bucket = event['Records'][0]['s3']['bucket']['name']
    processed_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    trained_model_bucket = "adiona-trained-models"
    
    id = processed_key[0:4]
    sensor_template_str = Template('$ID/accData.json')
    sensor_file_key = sensor_template_str.substitute(ID=id)
    truth_template_str = Template('$ID/agitationGroundTruth.json')
    truth_file_key = truth_template_str.substitute(ID=id)
    model_template_str = Template('$ID/trainedModel.pkl')
    model_file_key = model_template_str.substitute(ID=id)

   
    try: 
        raw_response = s3.get_object(Bucket=processed_bucket, Key=processed_key)
        raw_content = raw_response["Body"]
        raw_jsonobj = json.loads(raw_content.read())
        print('JSON from raw s3 retrieved:', raw_jsonobj)

        agitation_model = train_agitation_function(processed_bucket, trained_model_bucket, sensor_file_key, truth_file_key, model_file_key)

        print('FUNCTION EXECUTED SUCCESSFULLY:', agitation_model)
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(processed_key, processed_bucket))
        raise e    
