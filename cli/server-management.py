import os
import boto3
import json
import argparse
from server import Org, SERVERS
from rich.table import Column, Table
from rich.console import Console

CREDENTIALFOLDER='.creds'
console = Console()

def getCredentialLocation(org):
    if not isinstance(org,Org):
        print("org is not a Org enum")
        return False
    
    credentialLocation=os.path.join("./", CREDENTIALFOLDER)

    if org == Org.RC:
        credentialLocation = os.path.join(credentialLocation, "rc.json")
    elif org == Org.KFNEXT:
        credentialLocation = os.path.join(credentialLocation, "kf.json")
    elif org == Org.REESELAB:
        credentialLocation = os.path.join(credentialLocation, "rl.json")
    
    return credentialLocation


def checkforCredential(org):
    if not isinstance(org,Org):
        print("org is not a Org enum")
        return False
    
    location = getCredentialLocation(org)

    if not os.path.isfile(location):
        return False
    else:
        return True


def loadCredentials(org):
    if not isinstance(org,Org):
        print("org is not a Org enum")
        return

    if not checkforCredential(org):
        print(f"Do not have the credentials for org: {org}")
        return False
    
    credentialLocation = getCredentialLocation(org) 
    
    with open(credentialLocation) as fh:
        credentials = json.load(fh)

    return credentials


def ls(args):
    servers = SERVERS

    if args.server:
        if not args.server in SERVERS:
            print(f"No servers named {args.server}")
            return
        else:
            #make the servers variable only contain a single server
            servers = {}
            servers[args.server] = SERVERS[args.server]


    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Project")
    table.add_column("Server")
    table.add_column("Status")
    table.add_column("Public IP")
    
    for name in servers:
        data = {}
        data['servers'] = servers[name]['servers'] 
        
        creds = loadCredentials(servers[name]['org'])
        
        lambda_client = boto3.client(
            "lambda",
            aws_access_key_id=creds['access_key'],
            aws_secret_access_key=creds['secret_key'],
            region_name=creds['region']
        )

        rv = lambda_client.invoke(
            FunctionName="describe-ec2",
            Payload=json.dumps(data)
        )

        outcome = json.load(rv['Payload'])
        
        for server_result in outcome['messages']:
            ip = ""
            if not 'public_ip' in server_result:
                ip ="*"
            else:
                ip = server_result['public_ip']

            table.add_row(name, server_result['name'], server_result['message'], ip)

    console.print(table)    


def updateServer(args):
    if args.server is None:
        print("Need to provide the server to stop")
        return

    if not args.server in SERVERS:
        print(f"{args.server} is not one of our managed servers")
        return

    data = {}
    data['servers'] = SERVERS[args.server]['servers'] 
    creds = loadCredentials(SERVERS[args.server]['org'])
    
    if not creds:
        #Problem when loading credentials let it handle error message
        return

    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=creds['access_key'],
        aws_secret_access_key=creds['secret_key'],
        region_name=creds['region']
    )

    if args.command == "stop":
        func="stop-ec2"
        verb="stop"
    elif args.command == "start":
        func="start-ec2"
        verb="start"
    else:
        print("command was not 'start' or 'stop'")
        return

    rv = lambda_client.invoke(
        FunctionName=func,
        Payload=json.dumps(data)
    )

    outcome = json.load(rv['Payload'])

    for server_result in outcome['messages']:
        if server_result['success']:
            print(f"{verb.capitalize()}{verb[-1]}ing server {server_result['name']}. This will take time to complete. Use the 'ls' command to check on the status of the server")
        else:
            print(f"Could not {verb} {server_result['name']} because {server_result['message']}")

def main():
    parser = argparse.ArgumentParser(description="Manage the Reese Inovation and KF Next EC2 Instances")
    parser.add_argument('command', type=str, choices=['ls', 'start', 'stop', 'check'],  help='List servers, start server, stop sever, check server')
    parser.add_argument('--server', type=str, help="name of the server")

    args = parser.parse_args()

    if args.command == "ls":
        ls(args)
    elif args.command == 'stop' or args.command == 'start':
        updateServer(args)


if __name__=='__main__':
    main()
