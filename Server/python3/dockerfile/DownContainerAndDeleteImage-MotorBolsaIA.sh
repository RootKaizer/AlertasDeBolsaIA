#!/bin/bash

# Definir el nombre del archivo docker-compose
COMPOSE_FILE="MotorBolsaIA.yml"
CONTAINER_IMAGE=rottdocker/alertasdebolsaia:python3

# Detener y eliminar los contenedores, redes y volúmenes definidos en el archivo docker-compose
echo "Deteniendo y eliminando contenedores y redes..."
docker-compose -f ${COMPOSE_FILE} down
docker container prune -f

# Eliminar la imagen '${CONTAINER_IMAGE}'
echo "Eliminando la imagen '${CONTAINER_IMAGE}'..."
docker rmi -f ${CONTAINER_IMAGE}

# Verificar si la imagen se ha eliminado correctamente
if ! docker image inspect ${CONTAINER_IMAGE} > /dev/null 2>&1; then
    echo "La imagen '${CONTAINER_IMAGE}' ha sido eliminada exitosamente."
else
    echo "Hubo un problema al eliminar la imagen."
fi
