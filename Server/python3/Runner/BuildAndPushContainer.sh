#!/bin/bash

# borrar imagen
#docker rmi -f rottdocker/alertasdebolsaia:python3

# depurar imagenes
#docker image prune


# construir contenedor
sudo docker build -t rottdocker/alertasdebolsaia:python3 .


# Subir al repositorio el contenedor
docker push rottdocker/alertasdebolsaia:python3
