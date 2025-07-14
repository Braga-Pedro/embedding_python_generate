FROM python:3.11-slim

ARG SCRIPTS_PATH=./src/
ARG DOCKER_PATH=./docker/python/

WORKDIR /embedding

COPY ${DOCKER_PATH}requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN if [ -f ${SCRIPTS_PATH}.env.example ]; then cp ${SCRIPTS_PATH}.env.example .env; fi

COPY ${SCRIPTS_PATH} .

CMD ["python3", "main.py"]