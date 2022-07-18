from curses import raw
import json
import urllib.parse
import boto3
from string import Template 
from helpers.acc_func import acc_function 
from helpers.hr_func import hr_function 
from helpers.res_func import res_function 
from helpers.lifestyle_func import lifestyle_function 
from helpers.agitation_func import agitation_function
# import pandas as pd 
# import numpy as np
# from sklearn import datasets
# from timesmash import SymbolicDerivative
# from sklearn.ensemble import RandomForestClassifier


print('Loading function')

s3 = boto3.client('s3')

def lambda_handler(event, context):
    raw_bucket = event['Records'][0]['s3']['bucket']['name']
    raw_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    processed_bucket = "processed-adiona-watch-app-data"
    mobile_bucket = "mobile-app-ready-data"
    
    id = raw_key[0:5]

    def create_string(filename): 
        template_str = Template('$ID/$filename')
        file_key = template_str.substitute(ID=id, filename=filename)
        return file_key

    acc_file_key = create_string('accData.json')
    hr_file_key = create_string('hrData.json')
    life_file_key = create_string('lifestyleData.json')
    ag_ground_truth_file_key = create_string('agitationGroundTruth.json')
    ag_displayed_file_key = create_string('predictedAgitation.json')
    alg_file_key = create_string('trainedModel.pkl')
    quantizer_file_key = create_string('fittedQuantizer.pkl')
   
    try: 
        raw_response = s3.get_object(Bucket=raw_bucket, Key=raw_key)
        raw_content = raw_response["Body"]
        raw_jsonobj = json.loads(raw_content.read())
        print('JSON from raw s3 retrieved')
        print("aloha")

        # acc_results = acc_function(processed_bucket, acc_file_key, raw_jsonobj)
        # print('ACC RESULTS:', acc_results)

        # hr_results = hr_function(processed_bucket, hr_file_key, raw_jsonobj)
        # print('HEART RATE RESULTS:', hr_results)

        # try: 
        #     res_results = res_function(processed_bucket, res_file_key, raw_jsonobj)
        #     print('RESPIRATORY RESULTS:', res_results)
        # except: 
        #     print('No respiratory sensor data available') 

        # lifestyle_results = lifestyle_function(processed_bucket, life_file_key, raw_jsonobj)
        # print('LIFESTYLE RESULTS:', lifestyle_results)

        agitation_results = agitation_function(processed_bucket, alg_file_key, quantizer_file_key, ag_ground_truth_file_key, ag_displayed_file_key, raw_jsonobj)
        # print('AGITATION RESULTS:', agitation_results)

        # print('RAW WATCH DATA FUNCTION RAN.')

        # s = pd.Series([1, 3, 5, np.nan, 6, 8])
        # print('pandas and numpy worked!', s)
        # print('now try scikit learn')
        # iris_X, iris_y = datasets.load_iris(return_X_y=True)
        # val = np.unique(iris_y)
        # print('sci kit learn worked too!', val)
        # print('Let us test Timesmash. See below.')
        # train = [[1, 0, 1, 0, 1, 0], [1, 1, 0, 1, 1, 0]]
        # train_label = [[0], [1]]
        # test = [[0, 1, 1, 0, 1, 1]]
        # train_features, test_features = SymbolicDerivative().fit_transform(
        #     train=train, test=test, label=train_label
        # )
        # clf = RandomForestClassifier().fit(train_features, train_label)
        # label = clf.predict(test_features)
        # print("Predicted label: ", label)
        # print('Great! If you see the predicted label, then it worked.')


        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(raw_key, raw_bucket))
        raise e    
