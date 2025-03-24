# /bin/bash

# Definir el nombre del archivo docker-compose
COMPOSE_FILE="MotorBolsaIA.yml"
CONTAINER_IMAGE=rottdocker/alertasdebolsaia:python3

# Detener y eliminar los contenedores, redes y volúmenes definidos en el archivo docker-compose
echo "Deteniendo y eliminando contenedores y redes..."
docker-compose -f ${COMPOSE_FILE} down

# Eliminar la imagen '${CONTAINER_IMAGE}'
echo "Eliminando la imagen '${CONTAINER_IMAGE}'..."
docker rmi -f ${CONTAINER_IMAGE}
docker ps

# Verificar si la imagen se ha eliminado correctamente
if ! docker image inspect ${CONTAINER_IMAGE} > /dev/null 2>&1; then
    echo "La imagen '${CONTAINER_IMAGE}' ha sido eliminada exitosamente."
else
    echo "Hubo un problema al eliminar la imagen."
fi

# Iniciar  contenedor magis-tv
docker-compose -f $COMPOSE_FILE up -d


# validar servicios arriba
sleep 5
echo "------------------------------------------------------------"
echo "validar servicios arriba"
echo "------------------------------------------------------------"
docker ps -a | grep ${CONTAINER_IMAGE}


# Log de arranque
#docker logs -f magis-tv
