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

# Descargar y compilar TA-Lib correctamente
#RUN curl -L https://sourceforge.net/projects/ta-lib/files/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz/download -o ta-lib-0.4.0-src.tar.gz \
#    && tar -xzf ta-lib-0.4.0-src.tar.gz \
#    && ls -la \
##    && cd ta-lib \
#    && ./configure --prefix=/usr/local \
#    && make \
#    && make install \
#    && cd .. \
#    && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz



# Verificar que la librería fue instalada en `/usr/local/lib`
#RUN ls -la /usr/local/lib/ | grep libta_lib.so

# Verificar que la librería fue instalada en `/usr/local/lib`
#RUN ls -la /usr/local/lib/ | grep ta

# Actualizar caché de bibliotecas
#ENV LIB_TA_PATH="/usr/local/lib"
#ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${LIB_TA_PATH}"
#ENV CFLAGS="${CFLAGS} -I/usr/local/include"
#ENV LDFLAGS="${LDFLAGS} -L/usr/local/lib -lta_lib"



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
    backtrader


# Actualizar caché de bibliotecas
#https://files.pythonhosted.org/packages/35/dc/e7fab66315fdd2e2eeb2e3dbb9d23ea615bafc1e9174a8965d310e40a3c2/ta_lib-0.6.3.tar.gz
#RUN ln -s /usr/local/lib/libta_lib.so.0.0.0 /usr/local/lib/libta-lib.so
#ENV LDFLAGS="${LDFLAGS} -L/usr/local/lib  -Llta-lib"
#ENV LDFLAGS="${LDFLAGS} -L/usr/local/lib  -L/usr/local/lib/lta-lib -L/usr/local/lib/lta_lib.so -L/usr/local/lib/lta_lib.so.0"

# Instalar TA-Lib con pip (ahora debería encontrar la librería)
#RUN pip install --no-cache-dir TA-Lib

# Verifica que la librería esté accesible
# RUN ldd /MotorBolsaIA/lib/python3.10/site-packages/talib/_ta_lib.cpython-310-x86_64-linux-gnu.so

# Verificar instalación,
RUN python -c "import numpy, pandas, matplotlib, plotly, sklearn, websocket, backtrader; print('Instalación exitosa')"
#RUN python -c "import numpy, pandas, matplotlib, plotly, sklearn, websocket; print('Instalación exitosa')"

CMD ["python3"]
