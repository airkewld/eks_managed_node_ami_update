import boto3
import botocore
import os
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT,level=logging.INFO)

## Ensure that credentials are set.
try:
  AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']
except KeyError:
  logging.error("Missing AWS_DEFAULT_REGION environment variable")
  exit(1)
try:
  AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
except KeyError:
  logging.error("Partial credentials found in env, missing: AWS_ACCESS_KEY_ID")
  exit(1)
try:
  AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
except KeyError:
  logging.error("Partial credentials found in env, missing: AWS_SECRET_ACCESS_KEY")
  exit(1)
try:
  CLUSTER = os.environ['CLUSTER_NAME']
except KeyError:
    logging.error("Missing required CLUSTER_NAME environment variable.")
    exit(1)

## set client variable
eks_client = boto3.client('eks')

try:
  nodegroups = eks_client.list_nodegroups(clusterName=CLUSTER)["nodegroups"]

  ## Loop tough the nodegroups of the eks cluster and upgrade one at a time while outputting the status of the upgrade
  for group in nodegroups:
      status = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)["nodegroup"]["status"]
      if status == "ACTIVE":
        logging.info(group + " is " + status)
        # update_vendor_registry = eks_client.update_nodegroup_version(clusterName=CLUSTER,nodegroupName=group,force=True)
      status = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)["nodegroup"]["status"]
      while status != "ACTIVE":
        status = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)["nodegroup"]["status"]
        logging.info(group + " is " + status)
        status = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)["nodegroup"]["status"]

  ## Loop tough each node and output its status
  for group in nodegroups:
      status = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)["nodegroup"]["status"]
      logging.info(group + " is " + status)

except botocore.exceptions.NoCredentialsError:
    logging.error("Please provide credentials via environment variables.")
    exit(1)
except eks_client.exceptions.ResourceNotFoundException:
    logging.error(CLUSTER + " eks cluster not found.")
    exit(1)
except eks_client.exceptions.ClientError:
    logging.error("Bad credentials provided. Try again.")
    exit(1)
except botocore.exceptions.EndpointConnectionError:
    print(AWS_DEFAULT_REGION)
    logging.error("Could not connect to the endpoint URL: https://eks." + AWS_DEFAULT_REGION + ".amazonaws.com/clusters/" + CLUSTER + "/node-groups")
