from curses import raw
import json
import urllib.parse
import boto3
from string import Template 
from acc_func import acc_function 
from hr_func import hr_function 
from res_func import res_function 
from lifestyle_func import lifestyle_function 
from agitation_func import agitation_function
from sleep_func import sleep_function

print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    raw_bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    processed_bucket = "processed-adiona-watch-app-data"
    
    id = raw_key[0:5]
    acc_template_str = Template('$ID/accData.json')
    acc_file_key = acc_template_str.substitute(ID=id)
    hr_template_str = Template('$ID/hrData.json')
    hr_file_key = hr_template_str.substitute(ID=id)
    res_template_str = Template('$ID/respiratoryData.json')
    res_file_key = res_template_str.substitute(ID=id)
    life_template_str = Template('$ID/lifestyleData.json')
    life_file_key = life_template_str.substitute(ID=id)

    ag_displayed_str = Template('$ID/agitationGroundTruth.json')
    ag_ground_truth_file_key = ag_displayed_str.substitute(ID=id)
    ag_displayed_str = Template('$ID/predictedAgitation.json')
    ag_displayed_file_key = ag_displayed_str.substitute(ID=id)
    sleep_template_str = Template('$ID/sleepData.json')
    sleep_file_key = sleep_template_str.substitute(ID=id)
    alg_template_str = Template('$ID/trainedModel.pkl')
    alg_file_key = alg_template_str.substitute(ID=id)
   
    try: 
        raw_response = s3.get_object(Bucket=raw_bucket, Key=raw_key)
        raw_content = raw_response["Body"]
        raw_jsonobj = json.loads(raw_content.read())
        print('JSON from raw s3 retrieved:', raw_jsonobj)

        acc_results = acc_function(processed_bucket, acc_file_key, raw_jsonobj)
        print('ACC RESULTS:', acc_results)

        hr_results = hr_function(processed_bucket, hr_file_key, raw_jsonobj)
        print('HEART RATE RESULTS:', hr_results)

        try: 
            res_results = res_function(processed_bucket, res_file_key, raw_jsonobj)
            print('RESPIRATORY RESULTS:', res_results)
        except: 
            print('No respiratory sensor data available') 

        lifestyle_results = lifestyle_function(processed_bucket, life_file_key, raw_jsonobj)
        print('LIFESTYLE RESULTS:', lifestyle_results)

        agitation_results = agitation_function(processed_bucket, alg_file_key, ag_ground_truth_file_key, ag_displayed_file_key, raw_jsonobj)
        print('AGITATION RESULTS:', agitation_results)

        sleep_results = sleep_function(processed_bucket, sleep_file_key, raw_jsonobj)
        print('SLEEP DATA RESULTS:', sleep_results)

        print('RAW WATCH DATA FUNCTION RAN.')
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(raw_key, raw_bucket))
        raise e    
