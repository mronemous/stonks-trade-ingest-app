#!/bin/bash

aws eks --region $AWS_DEFAULT_REGION --profile $AWS_PROFILE update-kubeconfig --name $KS_CLUSTER

for filename in ./kube_config/*.yml; do
  cat "$filename" | envsubst | kubectl apply -f -
done
