# Stage 1: Builder
FROM python:3.15-slim AS builder

WORKDIR /app

# Instala o poetry e o plugin de exportação (necessário nas versões mais recentes)
RUN pip install --no-cache-dir poetry poetry-plugin-export

COPY pyproject.toml poetry.lock ./

# Extrai os pacotes de produção para um requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --only main

# Stage 2: Final
FROM python:3.15-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copia apenas o arquivo requirements.txt do stage anterior
COPY --from=builder /app/requirements.txt .

# Instala as dependências diretamente no Python do sistema
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

EXPOSE 8000

CMD ["uvicorn", "it_mdb_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
