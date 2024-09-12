#!/bin/sh
# Token e Registro
registration_token="GR1348941VNgDGwZX4KeyehVbmw3h"
url="http://gitlab"

docker exec -it gitlab-runner \
gitlab-runner register \
    --non-interactive \
    --registration-token ${registration_token} \
    --locked=false \
    --description docker-stable \
    --url ${url} \
    --executor docker \
    --docker-image docker:stable \
    --docker-volumes "/var/run/docker.sock:/var/run/docker.sock" \
    --docker-network-mode gitlab