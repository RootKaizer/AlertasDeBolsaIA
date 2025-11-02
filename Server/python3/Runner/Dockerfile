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
    pkgconfig \
    rust \
    cargo \
    libxml2-dev \
    libxslt-dev

  

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
    requests==2.32.3 \
    openpyxl>=3.1.0 \
    xlsxwriter==3.2.0 \
    seaborn==0.13.2

# Instalar comunicación con IA >> LangChain y sus dependencias principales
RUN pip install --no-cache-dir \
    langchain==0.1.20 \
    langchain-community==0.0.38 \
    langchain-core==0.1.61 \
    langchain-text-splitters==0.0.1 \
    langchain-openai==0.1.6 \
    openai==1.30.1 \
    tiktoken==0.6.0 \
    chromadb==0.4.24 \
    sentence-transformers==2.7.0 \
    faiss-cpu==1.7.4

# Instalar dependencias adicionales para procesamiento de texto
RUN pip install --no-cache-dir \
    beautifulsoup4==4.12.3 \
    lxml==5.2.1 \
    html5lib==1.1 \
    PyPDF2==3.0.1 \
    python-docx==1.1.0 \
    unstructured==0.14.3

# Instalar dependencias para APIs y web
RUN pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn==0.29.0 \
    pydantic==2.6.4 \
    pydantic-core==2.16.3 \
    httpx==0.27.0 \
    aiohttp==3.9.5

# Verificar instalación de paquetes críticos
RUN python -c "\
import numpy, pandas, matplotlib, scipy, sklearn; \
print('✅ Paquetes científicos instalados correctamente'); \
import openpyxl, xlsxwriter; \
print('✅ Paquetes Excel instalados correctamente'); \
import langchain, langchain_community, openai; \
print('✅ LangChain y OpenAI instalados correctamente'); \
print('Todas las dependencias instaladas exitosamente')"

# Copiar archivos al contenedor
COPY Program/ /app/

# Establecer permisos
RUN chmod +x /app/scripts/*.py

# Directorio de trabajo
WORKDIR /app

# Exponer puerto si es necesario para APIs
EXPOSE 8000

# Iniciar contenedor
#CMD ["python3"]
CMD ["python3", "Start.py", "mediano_plazo"]
