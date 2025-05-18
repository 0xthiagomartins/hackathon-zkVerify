# Usar Ubuntu 22.04 LTS
FROM ubuntu:22.04

# Evitar prompts durante a instalação
ENV DEBIAN_FRONTEND=noninteractive

# Instalar Python e dependências
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-venv \
    curl \
    build-essential \
    git \
    pkg-config \
    libssl-dev \
    jq \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Configurar shell para noirup
SHELL ["/bin/bash", "-c"]

# Instalar Rust e Cargo
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Instalar Noir
RUN curl -L https://raw.githubusercontent.com/noir-lang/noirup/main/install | bash && \
    echo 'export PATH="/root/.noir/bin:$PATH"' >> ~/.bashrc && \
    . ~/.bashrc && \
    noirup

# Compilar Barretenberg do código fonte
RUN git clone https://github.com/AztecProtocol/barretenberg.git /tmp/barretenberg && \
    cd /tmp/barretenberg && \
    git checkout v0.82.2 && \
    ./bootstrap.sh && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make -j$(nproc) bb

# Mover o binário compilado para um local no PATH
RUN cp /tmp/barretenberg/build/bin/bb /usr/local/bin/ && \
    rm -rf /tmp/barretenberg

# Configurar diretório de trabalho
WORKDIR /app

# Copiar todo o código fonte
COPY . .

# Instalar dependências Python
RUN pip3 install --no-cache-dir -e ".[dev]" && \
    pip3 install --no-cache-dir "uvicorn[standard]>=0.27.1"

# Expor a porta da API
EXPOSE 8000

# Comando para iniciar a API
CMD ["python3", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 