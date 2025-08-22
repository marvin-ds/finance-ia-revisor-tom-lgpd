# Finance-IA Revisor de Tom & LGPD - Dockerfile
# Sistema HTTP para revisão automatizada de conteúdo com IA

# Usar Python 3.11 slim como base
FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Criar usuário não-root para segurança
RUN groupadd -r financeai && useradd -r -g financeai financeai

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primeiro (para cache de layers)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Remover arquivos desnecessários
RUN rm -rf .git .gitignore .venv __pycache__ *.pyc *.pyo

# Alterar propriedade dos arquivos
RUN chown -R financeai:financeai /app

# Mudar para usuário não-root
USER financeai

# Expor porta
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/healthz', timeout=5)"

# Comando padrão (produção com Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]