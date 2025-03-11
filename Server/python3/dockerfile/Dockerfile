FROM python:3.10-alpine3.20

# Instalar dependencias necesarias
RUN apk add --no-cache \
    gcc \
    g++ \
    make \
    musl-dev \
    libstdc++ \
    libgcc \
    libffi-dev \
    openssl-dev \
    python3-dev \
    py3-pip \
    lapack-dev \
    gfortran \
    alpine-sdk \
    bash \
    tar \
    curl \
    wget \
    git \
    meson \
    ninja \
    gfortran

  

# validar version de gcc 
RUN gcc --version

    # validación de musl
RUN apk info musl
RUN ldd --version || true



# Directorio de trabajo
WORKDIR /tmp



# Crear entorno virtual
RUN python -m venv /MotorBolsaIA
ENV PATH="/MotorBolsaIA/bin:$PATH"

# Actualizar pip
RUN pip install --upgrade pip setuptools wheel

# Instalar dependencias de Python
RUN pip install --no-cache-dir \
    numpy \
    pandas \
    matplotlib \
    plotly \
    scikit-learn \
    websocket-client \
    backtrader \
    requests

# Verificar instalación,
RUN python -c "import numpy, pandas, matplotlib, plotly, sklearn, websocket, backtrader; print('Instalación exitosa')"


# Directorio de trabajo
WORKDIR /app


# Iniciar contenedor
CMD ["python3"]
