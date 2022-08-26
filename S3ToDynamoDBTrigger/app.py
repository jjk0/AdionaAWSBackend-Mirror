import boto3
import json

MASTER_AGITATION = 'masterAgitation.json'
TIPS_DATA = 'tipsData.json'
RESPIRATORY_DATA = 'respiratoryData.json'
HR_DATA = 'hrData.json'
LIFESTYLE_DATA = 'lifestyleData.json'

s3 = boto3.resource('s3')
pinpoint_client = boto3.client('pinpoint')


# PATIENT_HEALTH_DATA_TABLE_NAME = 'PatientWatchData-o76lfmasxnec5ftzmzuynnxuhi-dev'
# PATIENT_HEALTH_DATA_TABLE_NAME = 'PatientWatchData-dgii6riv3jhpvnp5nzl4age5pq-dev'
PATIENT_HEALTH_DATA_TABLE_NAME = 'PatientWatchData-5o6t4k2w7jgxvj2hpntqlyk5wi-dev'
# PATIENT_AGITATION_TABLE_NAME = 'PatientAgitation-o76lfmasxnec5ftzmzuynnxuhi-dev'
# PATIENT_AGITATION_TABLE_NAME = 'PatientAgitation-dgii6riv3jhpvnp5nzl4age5pq-dev'
PATIENT_AGITATION_TABLE_NAME = 'PatientAgitation-5o6t4k2w7jgxvj2hpntqlyk5wi-dev'
# PATIENT_TIPS_TABLE_NAME = 'PatientTips-o76lfmasxnec5ftzmzuynnxuhi-dev'
# PATIENT_TIPS_TABLE_NAME = 'PatientTips-dgii6riv3jhpvnp5nzl4age5pq-dev'
PATIENT_TIPS_TABLE_NAME = 'PatientTips-5o6t4k2w7jgxvj2hpntqlyk5wi-dev'


dynamodb = boto3.resource('dynamodb')
patientHealthDataTable = dynamodb.Table(PATIENT_HEALTH_DATA_TABLE_NAME)
patientTipsTable = dynamodb.Table(PATIENT_TIPS_TABLE_NAME)
patientAgitationTable = dynamodb.Table(PATIENT_AGITATION_TABLE_NAME)


def lambda_handler(event, context):
  print(event)
  bucket = event['Records'][0]['s3']['bucket']['name']
  key = event['Records'][0]['s3']['object']['key']

  keyInfo = key.split("/")
  print('this is keyInfo', keyInfo)

  if len(keyInfo) == 2 and keyInfo[0].isnumeric():
    patientId = keyInfo[0]

    # Processed masterAgitation file
    if key.endswith(MASTER_AGITATION):
      content = get_file_content(bucket, key)
      episodes = content.get('episodes')

      for time in episodes:
        insert__patient_agitation_data_in_table(patientId, time)


    # Processed tipsData file
    elif key.endswith(TIPS_DATA):
      content = get_file_content(bucket, key)
      lifestyle_tips = content.get('lifestyle_tips')
      sleep_tips = content.get('sleep_tips')
      hr_tips = content.get('hr_tips')
      respiratory_tips = content.get('respiratory_tips')
      general_tips = content.get('general_tips')

      insert__patient_tips_data_in_table(patientId, lifestyle_tips, 'lifestyleTip')
      insert__patient_tips_data_in_table(patientId, sleep_tips, 'sleepTip')
      insert__patient_tips_data_in_table(patientId, hr_tips, 'hrTip')
      insert__patient_tips_data_in_table(patientId, respiratory_tips, 'respiratoryTip')
      insert__patient_tips_data_in_table(patientId, general_tips, 'generalTip')


    # Processed respiratoryData file
    elif key.endswith(RESPIRATORY_DATA):
      content = get_file_content(bucket, key)

      respiratory_rate = content.get('respiratory_rate')
      oxygen_saturation = content.get('oxygen_saturation')
      
      for idx, val in enumerate(respiratory_rate.get('value')):
        timestamp = int(respiratory_rate['timestamps'][idx])
        insert__patient_health_data_in_table(patientId, str(timestamp), val, 'respiratoryRate')

      for idx, val in enumerate(oxygen_saturation.get('value')):
        timestamp = int(oxygen_saturation['timestamps'][idx])
        insert__patient_health_data_in_table(patientId, str(timestamp), val, 'oxygenSaturation')


    # Processed hrData file
    elif key.endswith(HR_DATA):
      content = get_file_content(bucket, key)

      heart_rate = content.get('heart_rate')
      
      for idx, val in enumerate(heart_rate.get('value')):
        timestamp = int(heart_rate['timestamps'][idx])
        insert__patient_health_data_in_table(patientId, str(timestamp), val, 'heartRate')
        
        
    # Processed lifestyleData file
    elif key.endswith(LIFESTYLE_DATA):
      content = get_file_content(bucket, key)

      step_count = content.get('step_count')
      calories = content.get('calories')
      print('here are steps:', step_count, 'here are calories:', calories)
      
      for idx, val in enumerate(step_count.get('value')):
        timestamp = int(step_count['timestamps'][idx])
        insert__patient_health_data_in_table(patientId, str(timestamp), val, 'steps')

      for idx, val in enumerate(calories.get('value')):
        timestamp = int(calories['timestamps'][idx])
        insert__patient_health_data_in_table(patientId, str(timestamp), val, 'calories')


    # Skip if unknown file
    else:
      print("Skipping file")

  # endpoints = pinpoint_client.get_user_endpoints(
  #   ApplicationId='530ffa0302914c9aad10fd138d436f45',
  #   UserId='90567bb6-1d30-4c40-a14f-d00696c33c82'
  # )
  # print("Pinpoint endpoints: ", endpoints)



def get_file_content(bucket, key):
    obj = s3.Object(bucket, key)
    data = obj.get()['Body'].read().decode('utf-8') 
    print('this runs')
    return json.loads(data)

# if tips==True: 

#   pinpoint_client.send_messages(
#       ApplicationId='530ffa0302914c9aad10fd138d436f45',
#       MessageRequest={
#           'Addresses': {
#               'string': {
#                   'BodyOverride': 'string',
#                   'ChannelType': 'APNS',
#                   'Context': {
#                       'string': 'string'
#                   },
#                   'RawContent': 'string',
#                   'Substitutions': {
#                       'string': [
#                           'string',
#                       ]
#                   },
#                   'TitleOverride': 'string'
#               }
#           },
#           'Context': {
#               'string': 'string'
#           },
#           'Endpoints': {
#               'string': {
#                   'BodyOverride': 'string',
#                   'Context': {
#                       'string': 'string'
#                   },
#                   'RawContent': 'string',
#                   'Substitutions': {
#                       'string': [
#                           'string',
#                       ]
#                   },
#                   'TitleOverride': 'string'
#               }
#           },
#           'MessageConfiguration': {
#               'APNSMessage': {
#                   'APNSPushType': 'string',
#                   'Action': 'OPEN_APP'|'DEEP_LINK'|'URL',
#                   'Badge': 123,
#                   'Body': 'hello world',
#                   'Category': 'string',
#                   'CollapseId': 'string',
#                   'Data': {
#                       'string': 'string'
#                   },
#                   'MediaUrl': 'string',
#                   'PreferredAuthenticationMethod': 'string',
#                   'Priority': 'string',
#                   'RawContent': 'string',
#                   'SilentPush': True|False,
#                   'Sound': 'string',
#                   'Substitutions': {
#                       'string': [
#                           'string',
#                       ]
#                   },
#                   'ThreadId': 'string',
#                   'TimeToLive': 123,
#                   'Title': 'string',
#                   'Url': 'string'
#               },
#           },
#           'TemplateConfiguration': {
#               'PushTemplate': {
#                   'Name': 'string',
#                   'Version': 'string'
#               },
#           },
#           'TraceId': 'string'
#       }
  # )

def insert__patient_health_data_in_table(patientId, time, val, key):
  # old_item = get__patient_health_data(patientId, time)

  # if old_item:
  #   old_item[key] = val

  #   patientHealthDataTable.put_item(Item=old_item)

  # else:
  patientHealthDataTable.put_item(Item= {'id': patientId, 'time': time, key: val})


def insert__patient_agitation_data_in_table(patientId, time):
  patientAgitationTable.put_item(Item = {'id': patientId, 'time': time})


def insert__patient_tips_data_in_table(patientId, tipData, tipKey):
  old_tips_data = get__patient_tips_data(patientId)
  new_tips = {}

  if old_tips_data and old_tips_data.get('tips'):
    new_tips = old_tips_data.get('tips')
  
  new_tips[tipKey] = tipData
  patientTipsTable.put_item(Item = {'id': patientId, 'tips': new_tips})


def get__patient_health_data(patientId, time):
  old_item = patientHealthDataTable.get_item(Key={
      'id': patientId,
      'time': time
  })
  return old_item.get('Item')

def get__patient_tips_data(patientId):
  old_item = patientTipsTable.get_item(Key={
      'id': patientId,
  })
  return old_item.get('Item')
