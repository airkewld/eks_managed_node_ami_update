# eks_managed_node_ami_updater
Automatically update eks nodes ami to the latest version.

>If running locally, make sure that you have already ran `aws configure`.
>Set `AWS_PROFILE` to the desired profile, `CLUSTER_NAME` to the desired cluster.
```
export AWS_PROFILE=profile_name
export CLUSTER_NAME=eks_cluster_name
python3 eks_ami_updater.py
```

>The image is built and pushed as ttl.sh/airkewld/eks-ami-updater:48h

>If running as a container, you must provide the env variables in order to authn/authz
```
docker run --rm -i -e CLUSTER_NAME=cluster_name -e AWS_ACCESS_KEY_ID=access_key_id -e AWS_SECRET_ACCESS_KEY=secret -e AWS_DEFAULT_REGION=aws_region ttl.sh/airkewld/eks-ami-updater:48h
```
