# Perforce Management

This repo contains all the files that help manage the Lab's EC2 Instances. It contains some lambda functions that will turn on/off EC2 instances. These functions can be called from the CLI utility.  

# Bootstrapping local environment
Python 3.7+
```
pip install -r requirements.txt
```
You need aws [Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html) (SAM) to deploy the lambda functions 

# Overview
This repo contains the Infrastructure as Code (SAM) for deploying lambda functions to manage EC2 instances and a CLI to interact with them. I choose to use the lambda functions instead of writing the EC2 management code in the cli to create seperation of concerns for security reasons. This way the credentials stored on the local machine only have access to the lambda service and not directly to our EC2 instances. 


# Build and deploy the lambda functions
Make sure your current AWS credentials are set to the account you want to deploy to.
```
sam build --use-container
sam deploy
```