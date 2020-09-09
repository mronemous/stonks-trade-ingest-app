#!/bin/bash

aws ecr get-login-password --region $AWS_DEFAULT_REGION --profile=$AWS_PROFILE | docker login --username AWS --password-stdin $ECR_HOST
docker build -t "${ECR_REPO}:${VERSION}" .
docker tag "${ECR_REPO}:${VERSION}" "${ECR_HOST}/${ECR_REPO}:${VERSION}"