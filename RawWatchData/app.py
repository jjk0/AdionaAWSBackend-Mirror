import json
import urllib.parse
import boto3
from string import Template 
from agitation_func import agitation_function
from sleep_func import sleep_function
from sensor_func import sensor_function 
from lifestyle_func import lifestyle_function 
from acc_func import acc_function 



print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    raw_bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    processed_bucket = "processed-adiona-watch-app-data"
    
    id = raw_key[0:4]
    acc_template_str = Template('$ID/accData.json')
    acc_file_key = acc_template_str.substitute(ID=id)
    ag_displayed_str = Template('$ID/agitationGroundTruth.json')
    ag_ground_truth_file_key = ag_displayed_str.substitute(ID=id)
    ag_displayed_str = Template('$ID/agitationDisplayed.json')
    ag_displayed_file_key = ag_displayed_str.substitute(ID=id)
    sleep_template_str = Template('$ID/sleepData.json')
    sleep_file_key = sleep_template_str.substitute(ID=id)
    life_template_str = Template('$ID/lifestyleData.json')
    life_file_key = life_template_str.substitute(ID=id)
    sensor_template_str = Template('$ID/sensorData.json')
    sensor_file_key = sensor_template_str.substitute(ID=id)
    alg_template_str = Template('$ID/trainedModel.pkl')
    alg_file_key = alg_template_str.substitute(ID=id)

    
    # this is dummy data you can substitute with raw_jsonobj to test how the function operates
    data = {
        "id": "11111",
        "type": "refund",
        "amount": 1.22,
        "date": "2022-06-09T06:19:04Z"
    }
   
    try: 
        raw_response = s3.get_object(Bucket=raw_bucket, Key=raw_key)
        raw_content = raw_response["Body"]
        raw_jsonobj = json.loads(raw_content.read())
        print('JSON from raw s3 retrieved:', raw_jsonobj)

        agitation_results = agitation_function(processed_bucket, alg_file_key, ag_ground_truth_file_key, ag_displayed_file_key, raw_jsonobj)
        print('AGITATION RESULTS:', agitation_results)

        # sleep_results = sleep_function(processed_bucket, sleep_file_key, data)
        # print('SLEEP DATA RESULTS:', sleep_results)

        # sensor_results = sensor_function(processed_bucket, sensor_file_key, data)
        # print('OTHER SENSOR RESULTS:', sensor_results)

        # lifestyle_results = lifestyle_function(processed_bucket, life_file_key, data)
        # print('LIFESTYLE RESULTS:', lifestyle_results)

        # acc_results = acc_function(processed_bucket, acc_file_key, data)
        # print('ACC RESULTS:', acc_results)

        print('RAW WATCH DATA FUNCTION RAN.')
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(raw_key, raw_bucket))
        raise e    
