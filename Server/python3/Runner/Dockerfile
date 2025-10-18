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
    openblas-dev \
    openblas \
    gfortran \
    alpine-sdk \
    bash \
    tar \
    curl \
    wget \
    git \
    cmake \
    meson \
    ninja \
    gfortran \
    pkgconfig

  

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

# Configurar variables de entorno para compilación
ENV LDFLAGS="-L/usr/lib"
ENV CFLAGS="-I/usr/include"
ENV OPENBLAS_NUM_THREADS=1

# Actualizar pip
RUN pip install --upgrade pip setuptools wheel cython

# Instalar numpy primero (base para otras librerías científicas)
RUN pip install --no-cache-dir numpy==1.26.4

# Instalar scipy con dependencias de build
RUN pip install --no-cache-dir scipy==1.13.1

# Instalar el resto de dependencias
RUN pip install --no-cache-dir \
    pandas==2.2.3 \
    matplotlib==3.10.0 \
    plotly==6.3.1 \
    scikit-learn==1.5.2 \
    websocket-client==1.8.0 \
    backtrader==1.9.78.123 \
    requests==2.32.3

# Verificar instalación,
RUN python -c "import numpy, pandas, matplotlib, plotly, sklearn, websocket, backtrader; print('Instalación exitosa')"

# Copiar archivos al contenedor
COPY Program/ /app/

# Directorio de trabajo
WORKDIR /app

# Iniciar contenedor
CMD ["python3"]
