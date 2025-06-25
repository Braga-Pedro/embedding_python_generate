FROM python:3.11-slim

ARG SCRIPTS_PATH=./src/scripts/
ARG DOCKER_PATH=./docker/python/

WORKDIR /app

COPY ${DOCKER_PATH}requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN if [ -f ${SCRIPTS_PATH}.env.example ]; then cp ${SCRIPTS_PATH}.env.example .env; fi

COPY ${SCRIPTS_PATH} .

RUN echo 'Aguardando instalação do modelo LLM...' && sleep 60

# CMD ["python3", "main.py"]
CMD ["python3", "dev.py"]
