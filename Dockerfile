FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Installs lib to do pings from the server
RUN apt-get update && apt-get install -y \
  inetutils-ping \
  && rm -rf /var/lib/apt/lists/*

CMD [ "/start-reload.sh" ]
