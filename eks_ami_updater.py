import boto3,os

CLUSTER = os.environ['CLUSTER_NAME']
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']

eks_client = boto3.client('eks')

node_group = eks_client.list_nodegroups(clusterName=CLUSTER)
nodegroups = node_group["nodegroups"]

## Loop tough the nodegroups of the eks cluster and upgrade one at a time while outputting the status of the upgrade
for group in nodegroups:
    description = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)
    group_status = description["nodegroup"]
    status = group_status["status"]
    if status == "ACTIVE":
      update_vendor_registry = eks_client.update_nodegroup_version(clusterName=CLUSTER,nodegroupName=group,force=True)
    description = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)
    group_status = description["nodegroup"]
    status = group_status["status"]
    while status != "ACTIVE":
      # update_vendor_registry = eks_client.update_nodegroup_version(clusterName=CLUSTER,nodegroupName=group,force=True)
      description = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)
      group_status = description["nodegroup"]
      status = group_status["status"]
      print(group_status["nodegroupName"] + " is " + status)
      status = group_status["status"]

## Loop tough each node and output its status
for group in nodegroups:
    description = eks_client.describe_nodegroup(clusterName=CLUSTER,nodegroupName=group)
    group_status = description["nodegroup"]
    status = group_status["status"]
    print(group_status["nodegroupName"] + " is " + status)
