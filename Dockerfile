# Use a imagem base oficial do Python
FROM python:3.9-slim

# Instala as dependências necessárias
RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pandas==2.1.4 openpyxl==3.1.2

# Copia o script wait-for-it e dá permissão de execução
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta que a aplicação irá rodar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["/wait-for-it.sh", "db:5432", "--", "flask", "run", "--host=0.0.0.0"]
