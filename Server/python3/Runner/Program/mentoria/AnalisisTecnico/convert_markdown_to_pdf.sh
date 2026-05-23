#!/bin/bash
# convert_to_pdf.sh - Conversor Markdown a PDF
# Uso: ./convert_to_pdf.sh archivo_entrada.md [archivo_salida.pdf]

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar parámetros
if [ $# -lt 1 ]; then
    echo -e "${RED}Error:${NC} Debes especificar el archivo de entrada"
    echo -e "Uso: ${GREEN}./convert_to_pdf.sh archivo_entrada.md [archivo_salida.pdf]${NC}"
    echo -e "Ejemplo: ${YELLOW}./convert_to_pdf.sh analisis_tecnico.md${NC}"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${2:-documento_final.pdf}"
#INPUT_FILE="01_Markdown_AnalisisTecnicoPrincipiantes_youtube.md"
#OUTPUT_FILE="01_PDF_AnalisisTecnicoPrincipiantes_youtube.pdf"

# Verificar que el archivo de entrada existe
if [ ! -f "$INPUT_FILE" ]; then
    echo -e "${RED}Error:${NC} El archivo '$INPUT_FILE' no existe"
    exit 1
fi

# Función para verificar e instalar dependencias
install_dependencies() {
    echo -e "${YELLOW}Verificando dependencias...${NC}"
    
    # Verificar pandoc
    if ! command -v pandoc &> /dev/null; then
        echo -e "${YELLOW}Instalando pandoc...${NC}"
        sudo apt update && sudo apt install -y pandoc
    else
        echo -e "${GREEN}✓ Pandoc ya instalado${NC}"
    fi
    
    # Verificar latex
    if ! command -v xelatex &> /dev/null; then
        echo -e "${YELLOW}Instalando TexLive...${NC}"
        sudo apt install -y texlive-latex-base texlive-fonts-recommended \
                          texlive-latex-extra texlive-xetex
    else
        echo -e "${GREEN}✓ LaTeX ya instalado${NC}"
    fi
}

# Función principal de conversión
convert_to_pdf() {
    echo -e "${YELLOW}Convirtiendo '$INPUT_FILE' a '$OUTPUT_FILE'...${NC}"
    
    pandoc "$INPUT_FILE" -o "$OUTPUT_FILE" \
        --pdf-engine=xelatex \
        -V geometry:margin=2cm \
        -V fontsize=11pt \
        --toc \
        --toc-depth=3
    
    # Verificar si la conversión fue exitosa
    if [ $? -eq 0 ] && [ -f "$OUTPUT_FILE" ]; then
        echo -e "${GREEN}✓ Conversión exitosa!${NC}"
        echo -e "Archivo generado: ${GREEN}$OUTPUT_FILE${NC}"
        echo -e "Tamaño del archivo: ${YELLOW}$(du -h "$OUTPUT_FILE" | cut -f1)${NC}"
    else
        echo -e "${RED}✗ Error en la conversión${NC}"
        exit 1
    fi
}

# Archivo de estilo personalizado
create_style_file() {
    cat > custom.sty << 'EOF'
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{fancyhdr}

% Colores personalizados
\definecolor{azulprofundo}{RGB}{0,51,102}
\definecolor{verdeoscuro}{RGB}{0,102,51}
\definecolor{naranja}{RGB}{255,140,0}

% Formato de títulos
\titleformat{\section}
{\color{azulprofundo}\normalfont\Large\bfseries}
{\thesection}{1em}{}

\titleformat{\subsection}
{\color{verdeoscuro}\normalfont\large\bfseries}
{\thesubsection}{1em}{}

\titleformat{\subsubsection}
{\color{naranja}\normalfont\normalsize\bfseries}
{\thesubsubsection}{1em}{}

% Encabezado y pie de página
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\leftmark}
\fancyhead[R]{\thepage}
\fancyfoot[C]{Análisis Técnico - Guía Completa}

% Espaciado de párrafos
\setlength{\parindent}{0pt}
\setlength{\parskip}{8pt}

% Mejorar listas
\usepackage{enumitem}
\setlist{nosep}
EOF
}

# Archivo header para metadatos PDF
create_header_file() {
    cat > header.tex << 'EOF'
\usepackage{hyperref}
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    urlcolor=red,
    pdftitle={Guía Completa de Análisis Técnico},
    pdfauthor={Sistema de Análisis},
    pdfsubject={Trading y Análisis Técnico},
    pdfkeywords={trading, análisis técnico, forex, criptomonedas, ETFs}
}
EOF
}

# Mensaje de inicio
echo -e "${GREEN}=== CONVERSOR MARKDOWN A PDF ===${NC}"
echo -e "Archivo de entrada: ${YELLOW}$INPUT_FILE${NC}"
echo -e "Archivo de salida:  ${YELLOW}$OUTPUT_FILE${NC}"
echo ""

# Ejecutar proceso principal
install_dependencies
create_style_file
create_header_file
convert_to_pdf

echo -e "\n${GREEN}Proceso completado!${NC}"