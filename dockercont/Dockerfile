FROM python:3.12-slim-bookworm

LABEL Maintainer="peterT"
COPY requirements.txt /app/src/app/requirements.txt
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY modbus_server_ip_float_v4.py .

CMD [ "python", "./modbus_server_ip_float_v4.py","-ip","192.168.0.71","-p", "502", "-t", "1", "-startreg", "600"]


