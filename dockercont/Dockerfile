FROM python:alpine3.21

LABEL Maintainer="peterT"
COPY requirements.txt /app/src/app/requirements.txt
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY modbus_server_ip_float.py .

CMD [ "python", "./modbus_server_ip_float.py","-ip","192.168.0.11 ","-p", "502", "-t", "1"]

