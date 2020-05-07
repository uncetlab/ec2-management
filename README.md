# Perforce Management

This repo contains all the files that help manage the Lab's EC2 Instances. It contains some lambda functions that will turn on/off EC2 instances. These functions can be called from the CLI utility.  

# Bootstrapping local environment
Python 3.7+
```
pip install -r requirements.txt
```
You need aws [Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) (SAM) to deploy the lambda functions 

You will need access to the lab's secret perforce server to get access to the configuration files and aws credentials for this to tool to work.

# Overview
This repo contains the Infrastructure as Code (SAM) for deploying lambda functions to manage EC2 instances and a CLI to interact with them. I choose to use the lambda functions instead of writing the EC2 management code in the cli to create seperation of concerns for security reasons. This way the credentials stored on the local machine only have access to the lambda service and not directly to our EC2 instances. 


# Build and deploy the lambda functions
Make sure your current AWS credentials are set to the account you want to deploy to. You then need to rename the .toml file for the environment you want to deploy to samconfig.toml. Setting the aws credentials for the RC environment is a pain so do it first then start a competely new terminal to switch to other credentials.
```
mv <org.toml> samconfig.toml

sam build --use-container
sam deploy

mv samconfig.toml <org.toml>
```

# CLI Tool
Commands:
Stop a running server
```
python cli/server-mangement.py stop --server <project>
```
Start a stopped server 
```
python cli/server-mangement.py start --server <project>
```
List all the servers you have access to
```
python cli/server-mangement.py ls 
```