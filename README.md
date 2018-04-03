# Create Analytics SMS Notification by Using AWS Lambda  

This is an example of developing an AWS Lambda function which will send an SMS or email when there is Centrify Analytics Alert. By extending the AWS Lambda function from this simple example, you can archive more sophisticated remediation tasks such as kill the session or ban the IP address etc. ![lambda.png](https://yanlin286934087.files.wordpress.com/2018/04/lambda1.png)

### Create SNS Topic

Create A SNS topic “analytics-demo”:

![SNS](https://yanlin286934087.files.wordpress.com/2018/04/sns.png) Create an SMS subscription, choose SMS in protocol and input your mobile number: ![SNS Topic Sub](https://yanlin286934087.files.wordpress.com/2018/04/sns-topic-sub.png)

### Create the AWS Lambda function

Login to your AWS Console via your favorite browser, select “Lambda**”** from “Services**”.**

  1. In “Functions**”**, Click “Create function**”** button
  2. In “**Create function”** wizard, choose “Author from scratch”, input “name”, choose Python 3.6 in “Runtime”, choose “Create new role from template(s)” from “Role” drop-down, input “Role name”, choose “SNS publish policy” from “Policy templates” drop-down.
  3. Click “Create function”
  4. In the “Function code”, choose “Edit code inline” in “Code entry type” drop-down.
  5. Copy and paste following code, remember to replace sns_arn variable with your SNS ARN.
  6. Review the code, settings and click the “Save” button.
[code language='python'] import json import boto3 sns = boto3.client('sns') def lambda_handler(event, context): print("Received event: " + json.dumps(event, indent=2)) # Replace following with your SNS ARN sns_arn = 'arn:aws:sns:us-west-2:99999999:analytics-demo' sns_event = event sns_event["default"] = json.dumps(event) try: sns.publish( TargetArn=sns_arn, Message=json.dumps(sns_event), MessageStructure='json', Subject="Centrify Analytics Alert" ) except Exception as e: print(e) raise e [/code] This simple example code is using boto3 to publish the webhook payload from Centrify Analytics to the SNS topic, which has your mobile SMS number subscribed to. 

### Setup AWS API Gateway

To make the Lambda function accessible via an HTTP POST, you need to create AWS API Gateway and associate the Lambda function with an API endpoint. Login to your AWS Console via your favorite browser, select “**API Gateway”** from “**Services”.**

  1. Click “Create API” button  --> input “Analytics Demo API” as “API name”
  2. Click the “Create API” button
  3. Choose “Create Resource” in “Actions” drop-down  -->  input “analyticsdemo” as “Resource Name” and “analyticsdemo” as “Resource Path”
  4. Click “Create Resouce” button
  5. Select the newly created “analyticsdemo” node in “Resources” tree --> choose “Create Method” in “Actions” drop-down --> choose “POST” method for “analyticsdemo” resource.
  6. In the POST method configuration panel  -->  choose “Lambda Function” as “Integration type”  --> choose the proper “Lambda Region”  -->  input your lambda ARN in “Lambda Function”.
  7. Click “Save” button.
If all went well, you should end up with execution workflow diagram like this: ![api gateway post](https://yanlin286934087.files.wordpress.com/2018/04/api-gateway-post.png)

### Setup API Stage

The stage represents the label of API lifecycle stages, e.g. development, test, production etc. In API console choose your API and the root resource of the API  --> choose “Deploy API” in the “Actions” drop-down: ![api stage](https://yanlin286934087.files.wordpress.com/2018/04/api-stage.png) In this example, I use “demo” as the stage name. 

### Setup Usage Plan

“Usage Plans” allow you to put control and constraint into your API, e.g. “Rate”, “Burst”, “Quota” etc. If you have setup API usage plan before, you just need to add the newly created API to the usage plan, otherwise, you will need to follow the steps below. Also if you have never used “Usage Plans” and don't see the option in the API console, you will need to enable it in your account. In API console, choose “Usage Plans” and click “Create” button. Follow the wizard and make sure to associate your API and stage with the usage plan in the wizard: ![api usage plan](https://yanlin286934087.files.wordpress.com/2018/04/api-usage-plan.png)

### Setup API Key

In API console, choose “API Keys”, then choose “Create API key” in “Actions”. Once the API key is created, you can click the newly create API key and click the “Add to Usage Plan” button to link your API key to the usage plan: ![api key](https://yanlin286934087.files.wordpress.com/2018/04/api-key.png) Click “Show” link, copy and save your API key. This API key will be used in the webhooks configuration in Centrify Analytics Portal. 

### Deploy

In API console choose your API and the root resource of the API, then choose “Deploy API” in the “Actions” drop-down.  You should use the “demo” stage to deploy the API. After deploy, your API is now ready to use and you can find "invoke URL" from the stage editor: ![deploy stage](https://yanlin286934087.files.wordpress.com/2018/04/deploy-stage1.png)

### Setup Centrify Analytics Webhook

Log in Centrify Analytics portal and navigate to Settings -> Webhooks. Click “New” button: ![analytics webhook](https://yanlin286934087.files.wordpress.com/2018/04/analytics-webhook.png) The webhook can be also imported from “Anomaly Detection Notification.json“ which is located in this Github [repository](https://github.com/centrify/Analytics-Notification-Lambda). 

### End to end Testing
