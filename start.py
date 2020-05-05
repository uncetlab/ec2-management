import os
import boto3
import json

def start(event, context):
    if 'servers' in event:
        servers = event['servers']
    else:
        print(f"Could not find key 'servers' in dict: {event}")
        return

    ec2 = boto3.resource('ec2')
    rv = []
    for server in servers:      
        rv_message={'name':server['name'], 'id':server['id'],'success': False ,'state':'','message':''}
        try:
            instance = ec2.Instance(server['id'])
        except:
            rv_message['message'] = f"Could not find {server['name']}"
        
        rv_message['state'] = instance.state['Code'] 

        #https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_InstanceState.html
        if instance.state['Code'] == 0:
            rv_message['message'] = f"Instance {server['name']} is pending"
        if instance.state['Code'] == 16:  
            rv_message['message'] = f"Instance {server['name']} is running"
        if instance.state['Code'] == 32:
            rv_message['message'] = f"Instance {server['name']} is shutting-down"
        if instance.state['Code'] == 48:
            rv_message['message'] = f"Instance {server['name']} is terminated"
        if instance.state['Code'] == 64:
            rv_message['message'] = f"Instance {server['name']} is stopping"
        if instance.state['Code'] == 80:
            try:
                instance.start()
                rv_message['message'] = f"Starting instance {server['name']}"
                rv_message['success'] = True
            except:
                rv_message['message'] = f"Could not start instance {server['name']}"


        print(rv_message)
        rv.append(rv_message)       
    
    return {
        "messages": rv,
    }

