import json
import boto3

sns = boto3.client('sns')

def lambda_handler(event, context):

    print("Received event: " + json.dumps(event, indent=2))
    sns_arn = 'arn:aws:sns:us-west-2:99999999:analytics-demo' # Replace it with your SNS ARN
    sns_event = event
    sns_event["default"] = json.dumps(event)

    try:
        sns.publish(
            TargetArn=sns_arn,
            Message=json.dumps(sns_event),
            MessageStructure='json',
            Subject="Centrify Analytics Alert"
        )
    except Exception as e:
        print(e)
        raise e
