#!/bin/bash

aws ecr get-login-password --region $AWS_DEFAULT_REGION --profile=$AWS_PROFILE | docker login --username AWS --password-stdin $ECR_HOST
docker push "${ECR_HOST}/${ECR_REPO}:${VERSION}"