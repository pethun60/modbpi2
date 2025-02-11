FROM python:3.12-slim-bookworm

LABEL Maintainer="peterT"
COPY requirements.txt /app/src/app/requirements.txt
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY modbus_server_ip_float_v2.py .

CMD [ "python", "./modbus_server_ip_float_v2.py","-ip","192.168.0.11 ","-p", "5020", "-t", "1"]

