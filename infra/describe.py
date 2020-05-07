import os
import boto3
import json

def describe(event, context):
    if 'servers' in event:
        servers = event['servers']
    else:
        print(f"Could not find key 'servers' in dict: {event}")
        return

    ec2 = boto3.resource('ec2')
    rv = []
    for server in servers:      
        rv_message={'name':server['name'], 'id':server['id'] ,'state':'','message':''}
        try:
            instance = ec2.Instance(server['id'])
        except:
            rv_message['message'] = f"Could not find {server['name']}"
        
        rv_message['state'] = instance.state['Code'] 

        #https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_InstanceState.html
        if instance.state['Code'] == 0:
            rv_message['message'] = f"{server['name']} is pending"
        if instance.state['Code'] == 16:  
            rv_message['message'] = f"{server['name']} is running"
            extra_info = boto3.client('ec2').describe_instances(InstanceIds=[server['id']])
            public_ip = extra_info["Reservations"][0]["Instances"][0]["NetworkInterfaces"][0]["Association"]["PublicIp"]
            rv_message['public_ip'] = public_ip
        if instance.state['Code'] == 32:
            rv_message['message'] = f"{server['name']} is shutting-down"
        if instance.state['Code'] == 48:
            rv_message['message'] = f"{server['name']} is terminated"
        if instance.state['Code'] == 64:
            rv_message['message'] = f"{server['name']} is stopping"
        if instance.state['Code'] == 80:
            rv_message['message'] = f"{server['name']} is stopped"


        print(rv_message)
        rv.append(rv_message)       
    
    return {
        "messages": rv,
    }
