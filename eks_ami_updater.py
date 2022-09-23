import boto3,os,logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT,level=logging.INFO)

homeDir = os.getenv("HOME")

if os.path.exists(homeDir + "/.aws/credentials") == True:
  logging.info("Using local credentials file...")
elif os.path.exists(homeDir + "/.aws/credentials") != True:
  logging.info("Credentials file not found.")
  try:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
  except KeyError:
    logging.error("Missing container environment variable AWS_ACCESS_KEY_ID.")
    exit(1)
  try:
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
  except KeyError:
    logging.error("Missing container environment variable AWS_SECRET_ACCESS_KEY.")
    exit(1)
  try:
    AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']
  except KeyError:
    logging.error("Missing container environment variable AWS_DEFAULT_REGION." )
    exit(1)

try:
  CLUSTER = os.environ['CLUSTER_NAME']
  eks_client = boto3.client('eks')

  node_group = eks_client.list_nodegroups(clusterName=CLUSTER)
  nodegroups = node_group["nodegroups"]

  ## Loop tough the nodegroups of the eks cluster and upgrade one at a time while outputting the status of the upgrade
  for group in nodegroups:
      description = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)
      group_status = description["nodegroup"]
      status = group_status["status"]
      if status == "ACTIVE":
        logging.info(group_status["nodegroupName"] + " is " + status)
        update_vendor_registry = eks_client.update_nodegroup_version(clusterName=CLUSTER,nodegroupName=group,force=True)
      description = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)
      group_status = description["nodegroup"]
      status = group_status["status"]
      while status != "ACTIVE":
        # update_vendor_registry = eks_client.update_nodegroup_version(clusterName=CLUSTER,nodegroupName=group,force=True)
        description = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)
        group_status = description["nodegroup"]
        status = group_status["status"]
        logging.info(group_status["nodegroupName"] + " is " + status)
        status = group_status["status"]

  ## Loop tough each node and output its status
  for group in nodegroups:
      description = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)
      group_status = description["nodegroup"]
      status = group_status["status"]
      logging.info(group_status["nodegroupName"] + " is " + status)
except KeyError:
    logging.error("Missing required CLUSTER_NAME environment variable")
    exit(1)
except:
    logging.error("Cluster name did not match environment credentials.")
