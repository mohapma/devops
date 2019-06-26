export imageTag=${1:-"develop-latest"}
export imageName=${2:-"digital-clm/dclm-customer-management"}

export RANCHER_PROJECT_NAME=${3:-"dclm-customer-management"}

export RANCHER_URL="https://rancher.tecnotree.com/v1"
export RANCHER_ENVIRONMENT="1a45760"
export RANCHER_ACCESS_KEY="B68A6D267CBB814308D5"
export RANCHER_SECRET_KEY="YRoE6gkCoCMyhSygNF9RhZbL8bVp7wZ28jzQ717p"

wget https://nexus.tecnotree.com/repository/raw-3rd-party/rancher/cli/v0.6.13/rancher-linux-amd64-v0.6.13.tar.gz -O - | tar -zx  -C . --strip-components=2

rm -rf ${RANCHER_PROJECT_NAME}
./rancher export ${RANCHER_PROJECT_NAME}
cd ${RANCHER_PROJECT_NAME}
sed -i "s|${imageName}.*|${imageName}:${imageTag}|g" ./docker-compose.yml
../rancher up --upgrade -c -d

exit 0
