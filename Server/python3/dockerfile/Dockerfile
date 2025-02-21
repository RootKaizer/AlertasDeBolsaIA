# Usar Ubuntu Minimal como base
FROM ubuntu:20.04

# Establecer el directorio de trabajo
WORKDIR /app

# Evitar la interacción al instalar paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Actualizar e instalar dependencias necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    curl \
    wget \
    make \
    gcc \
    nano \
    vim

# Actualizar pip
RUN pip3 install --upgrade pip setuptools wheel

# Instalar dependencias de Python excepto TA-Lib
RUN pip3 install --no-cache-dir \
    pandas \
    numpy \
    matplotlib \
    plotly \
    scikit-learn \
    websockets

RUN apt install -y python3.8-venv

# Crear usuario python3 con UUID 9000 y contraseña pythonuser1
RUN useradd -m -u 9000 -s /bin/bash python3 && \
    echo "python3:pythonuser1" | chpasswd

# Copiar el script de arranque al home del usuario
COPY --chown=python3:python3 ./bin/startServicePython.sh /app/startServicePython.sh

# Dar permisos de ejecución al script
RUN chmod +x /app/startServicePython.sh

# Exponer un puerto si es necesario
EXPOSE 8080

# Comando de arranque del contenedor
CMD ["/bin/sh"]
#CMD ["/home/python3/startServicePython.sh"]
#CMD ["python3"]

