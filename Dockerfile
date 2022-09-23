FROM python:3.11.0rc2-alpine3.16
WORKDIR /app
RUN pip install boto3 && \
    addgroup -S eks-ami-updater && adduser -S eks-ami-updater -G eks-ami-updater -u 2055
COPY ./eks_ami_updater.py /app
USER 2055
ENTRYPOINT python /app/eks_ami_updater.py
