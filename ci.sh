#Simulation of what Jenkins or Travis would do.

set -o allexport
source .env
set +o allexport

#TODO: add unit testing, code checks to ci

./scripts/build.sh && ./scripts/publish.sh && ./scripts/deploy.sh