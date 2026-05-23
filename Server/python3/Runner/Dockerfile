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

# =============================================================================
# PAQUETES CIENTÍFICOS BASE
# =============================================================================
RUN pip install --no-cache-dir \
    numpy==1.26.4 \
    scipy==1.13.1

# =============================================================================
# PAQUETES DE TRADING Y DATOS FINANCIEROS
# =============================================================================
RUN pip install --no-cache-dir \
    pandas==2.2.3 \
    backtrader==1.9.78.123 \
    websocket-client==1.8.0 \
    requests==2.32.3
    
# =============================================================================
# PAQUETES DE GRÁFICOS Y VISUALIZACIÓN
# =============================================================================
RUN pip install --no-cache-dir \
    matplotlib==3.10.0 \
    plotly==6.3.1 \
    seaborn==0.13.2

# =============================================================================
# PAQUETES DE REPORTES Y EXCEL
# =============================================================================
RUN pip install --no-cache-dir \
    openpyxl==3.1.2 \
    xlsxwriter==3.2.0

# =============================================================================
# MACHINE LEARNING Y ANÁLISIS
# =============================================================================
RUN pip install --no-cache-dir \
    scikit-learn==1.5.2

# =============================================================================
# PROCESAMIENTO DE TEXTO Y DOCUMENTOS
# =============================================================================
RUN pip install --no-cache-dir \
    beautifulsoup4==4.12.3 \
    lxml==5.2.1 \
    html5lib==1.1 \
    PyPDF2==3.0.1 \
    python-docx==1.1.0

# =============================================================================
# APIS Y COMUNICACIÓN
# =============================================================================
RUN pip install --no-cache-dir \
    fastapi==0.110.0 \
    uvicorn==0.29.0 \
    pydantic==2.6.4 \
    pydantic-core==2.16.3 \
    httpx==0.27.0 \
    aiohttp==3.9.5 \
    openai==1.68.0          # <-- OPENAI AGREGADO

    
# =============================================================================
# VERIFICACIÓN POR CATEGORÍAS
# =============================================================================
RUN python -c "\
print('🔬 VERIFICANDO PAQUETES CIENTÍFICOS...'); \
import numpy; print(f'  ✅ numpy: {numpy.__version__}'); \
import scipy; print(f'  ✅ scipy: {scipy.__version__}'); \
print(''); \
print('📈 VERIFICANDO PAQUETES DE TRADING...'); \
import pandas; print(f'  ✅ pandas: {pandas.__version__}'); \
import backtrader; print('  ✅ backtrader: OK'); \
import websocket; print('  ✅ websocket: OK'); \
import requests; print(f'  ✅ requests: {requests.__version__}'); \
print(''); \
print('📊 VERIFICANDO PAQUETES DE GRÁFICOS...'); \
import matplotlib; print(f'  ✅ matplotlib: {matplotlib.__version__}'); \
import plotly; print(f'  ✅ plotly: {plotly.__version__}'); \
import seaborn; print(f'  ✅ seaborn: {seaborn.__version__}'); \
print(''); \
print('📋 VERIFICANDO PAQUETES DE REPORTES...'); \
import openpyxl; print(f'  ✅ openpyxl: {openpyxl.__version__}'); \
import xlsxwriter; print(f'  ✅ xlsxwriter: {xlsxwriter.__version__}'); \
print(''); \
print('🤖 VERIFICANDO MACHINE LEARNING...'); \
import sklearn; print(f'  ✅ scikit-learn: {sklearn.__version__}'); \
print(''); \
print('🤖 OPENAI...'); \
import openai; print(f'  ✅ openai: {openai.__version__}'); \
print(''); \
print('🎉 TODOS LOS PAQUETES INSTALADOS CORRECTAMENTE');"

# Copiar archivos al contenedor
COPY Program/ /app/

# Establecer permisos
RUN chmod +x /app/scripts/*.py

# Directorio de trabajo
WORKDIR /app

# Exponer puerto si es necesario para APIs
EXPOSE 8000

# Iniciar contenedor
#CMD ["python3", "Start.py", "mediano_plazo"]
CMD ["python3"]

