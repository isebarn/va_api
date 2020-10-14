FROM python:3.8

# current working directory in the docker container filesystem
WORKDIR /app

# run 'git clone <your repo> api'
COPY api .

# install project dependencies
RUN pip3 install -r requirements.txt

ENV DATABASE=mongodb://root:example@192.168.1.35:27017/ # may need edit
ENV PASSWORD=example # may need edit
ENV USERNAME=root # may need edit

EXPOSE 1024 # may need edit

ENTRYPOINT [ "gunicorn", "API:app", "--bind", "0.0.0.0:1024", "--timeout", "120", "--log-level", "debug"]