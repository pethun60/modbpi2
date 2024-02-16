
#!/usr/bin/env python3
"""Pymodbus synchronous client example.

An example of a single threaded synchronous client.

usage: simple_client_async.py

All options must be adapted in the code
The corresponding server must be started before e.g. as:
    python3 server_sync.py
"""

# --------------------------------------------------------------------------- #
# import the various client implementations
# --------------------------------------------------------------------------- #

# 

import pymodbus.client as ModbusClient
from pymodbus import (
    ExceptionResponse,
    Framer,
    ModbusException,
    pymodbus_apply_logging_config,
)
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

maxaddr=int(100)
minaddr=int=(0)

def decode_float(register):
    decoder = BinaryPayloadDecoder.fromRegisters(register.registers, byteorder=Endian.BIG, wordorder=Endian.LITTLE)
    return decoder.decode_32bit_float()

def run_sync_simple_client(comm, host, port, framer=Framer.SOCKET, minaddr=int):
    """Run sync client."""
    # activate debugging
    pymodbus_apply_logging_config("INFO")  # enable with "DEBUG" disable "INFO"


    print("get client")
    if comm == "tcp":
        client = ModbusClient.ModbusTcpClient(
            host,
            port=port,
            framer=framer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,y
            # close_comm_on_error=False,
            # strict=True,
            # source_address=("localhost", 0),
        )
    elif comm == "udp":
        client = ModbusClient.ModbusUdpClient(
            host,
            port=port,
            framer=framer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
            # source_address=None,
        )
    elif comm == "serial":
        client = ModbusClient.ModbusSerialClient(
            port,
            framer=framer,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,.
            # strict=True,
            baudrate=9600,
            bytesize=8,
            parity="N",
            stopbits=1,
            # handle_local_echo=False,
        )
    elif comm == "tls":
        client = ModbusClient.ModbusTlsClient(
            host,
            port=port,
            framer=Framer.TLS,
            # timeout=10,
            # retries=3,
            # retry_on_empty=False,
            # close_comm_on_error=False,
            # strict=True,
            # sslctx=None,
            certfile="../examples/certificates/pymodbus.crt",
            keyfile="../examples/certificates/pymodbus.key",
            # password=None,
            server_hostname="localhost",
        )
    else:
        print(f"Unknown client {comm} selected")
        return

    print("connect to server")
    client.connect()

    print("get and verify data")
    try:
        for i in range(minaddr,maxaddr,2):
    #       rr = client.read_coils(1, 1, slave=1)
            rr = client.read_holding_registers(address=i, count=maxaddr, slave=0)
            print("output")
            # print (rr.getRegister(0)) # This returns value of only one register
            # print (rr.registers[0:]) # This returns the response for whole length of registers
            
        
            float_value = decode_float(rr)
        
            print ("Register: %0.2f" % float_value)
            print ( 'loop ' + str(i)) 
    
    except ModbusException as exc:
        print(f"Received ModbusException({exc}) from library")
        client.close()
        return
    if rr.isError():
        print(f"Received Modbus library error({rr})")
        client.close()
        return
    if isinstance(rr, ExceptionResponse):
        print(f"Received Modbus library exception ({rr})")
        # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        client.close()
       
    print("close connection")
    client.close()



if __name__ == "__main__":
    run_sync_simple_client("tcp", "16.171.249.231", "5020" )