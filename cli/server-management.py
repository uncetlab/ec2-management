import os
import boto3
import json
import argparse
from enum import Enum


class Org(Enum):
    RC=1
    KFNEXT=2
    REESELAB=3

CREDENTIALFOLDER='.creds'
ORGS = [Org.KFNEXT, Org.RC, Org.REESELAB]


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
        credentialLocation = os.path.join(credentialLocation, "reese.json")
    
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
    for org in ORGS:
        rv = loadCredentials(org)
        if not rv:
            print(f"You do not have creds for {org}")
        else:
            print(rv)


def stop(args):
    rv = loadCredentials(Org.KFNEXT)
    lambda_client = boto3.client(
        "lambda",
        aws_access_key_id=rv['access_key'],
        aws_secret_access_key=rv['secret_key'],
        region_name=rv['region']
    )

    with open(os.path.join("./","demo","demo.json")) as fh:
        data = json.load(fh)

    rv2 = lambda_client.invoke(
        FunctionName="stop-ec2",
        Payload=json.dumps(data)
    )

    print(json.load(rv2['Payload']))


def main():
    parser = argparse.ArgumentParser(description="Manage the Reese Inovation and KF Next EC2 Instances")
    parser.add_argument('command', type=str, choices=['ls', 'start', 'stop', 'check'],  help='List servers, start server, stop sever, check server')
    parser.add_argument('--server', type=str, help="name of the server")

    args = parser.parse_args()
    #print(args)
    #print(args.command)
    if args.command == "ls":
        ls(args)
    elif args.command == 'stop':
        stop(args)


if __name__=='__main__':
    
    main()