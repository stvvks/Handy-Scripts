import os
import boto3
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# AWS credentials
AWS_REGION = 'your-aws-region'
AWS_ACCESS_KEY_ID = 'your-access-key-id'
AWS_SECRET_ACCESS_KEY = 'your-secret-access-key'

# Slack credentials
SLACK_TOKEN = 'your-slack-token'
SLACK_CHANNEL = '#your-channel-name'

def lambda_handler(event, context):
    # Initialize AWS clients
    ec2_client = boto3.client('ec2', region_name=AWS_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    
    # Get current date
    current_date = datetime.now().date()
    
    # Calculate cutoff date (30 days ago)
    cutoff_date = current_date - timedelta(days=30)
    
    # Get stopped instances
    stopped_instances = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    
    # Initialize list to store stopped instances stopped for more than 30 days
    instances_stopped_for_long_time = []
    
    # Check stopped instances
    for reservation in stopped_instances['Reservations']:
        for instance in reservation['Instances']:
            instance_id = instance['InstanceId']
            stopped_time = instance['StateTransitionReason'].split(' ')[-1]  # Get time instance was stopped
            stopped_date = datetime.strptime(stopped_time, '%Y-%m-%dT%H:%M:%S.000000Z').date()  # Convert to date
            
            # Check if instance has been stopped for more than 30 days
            if stopped_date <= cutoff_date:
                instances_stopped_for_long_time.append(instance_id)
    
    # Send notification to Slack
    if instances_stopped_for_long_time:
        message = f"The following EC2 instances have been stopped for more than 30 days: {' '.join(instances_stopped_for_long_time)}"
        send_slack_message(message)

def send_slack_message(message):
    try:
        client = WebClient(token=SLACK_TOKEN)
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        print("Slack notification sent successfully:", response)
    except SlackApiError as e:
        print(f"Failed to send Slack notification: {e.response['error']}")

