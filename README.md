# eks_managed_node_ami_update
Automatically update eks nodes ami to the latest version.

>If running locally, the script expects the following environment variables:
```
CLUSTER_NAME
  type: string
AWS_ACCESS_KEY_ID
  type: string
AWS_SECRET_ACCESS_KEY
  type: string
AWS_DEFAULT_REGION
  type: string
```


>The image is built and pushed as ttl.sh/airkewld/eks-ami-updater:48h

>If running as a container, pass the same variables
```
docker run --rm -i -e CLUSTER_NAME=eks-cluster1 -e AWS_ACCESS_KEY_ID=fsdlkjf654847 -e AWS_SECRET_ACCESS_KEY=65484sfdjkljfeij -e AWS_DEFAULT_REGION=us-west-1 ttl.sh/airkewld/eks-ami-updater:48h
```
