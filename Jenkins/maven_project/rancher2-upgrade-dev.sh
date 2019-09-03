##Jenkins Continuous Deployment on Rancher v2##
#!/bin/sh

IMAGE_TAG=${1:-"latest"}
IMAGE_NAME=${2:-"dev-docker-registry.tecnotree.com/ngb/ngbui"}

BEARER_TOKEN="token-8b9h6:46kpbwxnc2pdh44kwqpvhv4sddmwhxstcs7nxddksk75hksxtmzb62"       ##sandeep's token##
RANCHER_SERVER="https://rancher2.tecnotree.com/v3"
PROJECT="c-2cglh:p-46925"       ##dcbs-integration##
NAMESPACE="dcbs-apps"
DEPLOYMENT="dcbs-webui"
POD="dcbs-webui"

#Download Rancher v2 CLI
wget https://releases.rancher.com/cli2/v2.2.0/rancher-linux-amd64-v2.2.0.tar.gz  -O - | tar -zx  -C . --strip-components=2

./rancher login --token ${BEARER_TOKEN} --context ${PROJECT} ${RANCHER_SERVER}
./rancher kubectl --namespace=${NAMESPACE} set image deployment/${DEPLOYMENT} ${POD}=${IMAGE_NAME}:${IMAGE_TAG}

exit 0