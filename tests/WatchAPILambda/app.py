import json
# import res quests

print('Loading function')

def handler(event, context):

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'hello world',
        })
    }