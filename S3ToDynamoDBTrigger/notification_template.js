client.send_messages(
    ApplicationId='string',
    MessageRequest={
        'Addresses': {
            'string': {
                'BodyOverride': 'string',
                'ChannelType': 'APNS',
                'Context': {
                    'string': 'string'
                },
                'RawContent': 'string',
                'Substitutions': {
                    'string': [
                        'string',
                    ]
                },
                'TitleOverride': 'string'
            }
        },
        'Context': {
            'string': 'string'
        },
        'Endpoints': {
            'string': {
                'BodyOverride': 'string',
                'Context': {
                    'string': 'string'
                },
                'RawContent': 'string',
                'Substitutions': {
                    'string': [
                        'string',
                    ]
                },
                'TitleOverride': 'string'
            }
        },
        'MessageConfiguration': {
            'APNSMessage': {
                'APNSPushType': 'string',
                'Action': 'OPEN_APP'|'DEEP_LINK'|'URL',
                'Badge': 123,
                'Body': 'string',
                'Category': 'string',
                'CollapseId': 'string',
                'Data': {
                    'string': 'string'
                },
                'MediaUrl': 'string',
                'PreferredAuthenticationMethod': 'string',
                'Priority': 'string',
                'RawContent': 'string',
                'SilentPush': True|False,
                'Sound': 'string',
                'Substitutions': {
                    'string': [
                        'string',
                    ]
                },
                'ThreadId': 'string',
                'TimeToLive': 123,
                'Title': 'string',
                'Url': 'string'
            },
        },
        'TemplateConfiguration': {
            'PushTemplate': {
                'Name': 'string',
                'Version': 'string'
            },
        },
        'TraceId': 'string'
    }
)