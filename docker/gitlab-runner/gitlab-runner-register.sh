#!/bin/sh
# Token e Registro
registration_token="<Insira o token criado no Passo 1.2.e>"
url="http://192.168.98.10"

sudo docker exec -it gitlab-runner1 \
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