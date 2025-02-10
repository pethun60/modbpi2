#!/usr/bin/env python3

import asyncio
from pymodbus.server.async_io import ModbusTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import logging
import argparse

# Configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Global variable to track the holding register value
change_var = 100
parser = argparse.ArgumentParser(description='assign differnt ip address')
parser.add_argument('-ip', default='localhost', help='ip of the modbusserver in quotes"')
parser.add_argument('-p', default='5020', help='port of modbusserver')
parser.add_argument('-t', type=int, default=1, help='port of modbusserver')
args = parser.parse_args()

# Modbus Data Store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17] * 100),  # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [17] * 100),  # Coils
    hr=ModbusSequentialDataBlock(0, [change_var] * 100),  # Holding Registers
    ir=ModbusSequentialDataBlock(0, [17] * 100)   # Input Registers
)
context = ModbusServerContext(slaves=store, single=True)

# Device Identification
identity = ModbusDeviceIdentification()
identity.VendorName = 'Pymodbus'
identity.ProductCode = 'PM'
identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
identity.ProductName = 'Pymodbus Server'
identity.ModelName = 'Pymodbus Server'
identity.MajorMinorRevision = '2.5.3'

# Function to update holding registers
async def update_holding_registers():
    global change_var
    while True:
        # Update the values in holding registers (function code 3)
        change_var += 10
        if change_var > 1000:
            change_var = 100
        store.setValues(3, 0, [change_var] * 100)  # Update all holding registers
        log.info(f"Updated holding registers with value: {change_var}")
        await asyncio.sleep(args.t)  # Wait for 1 second

# Start TCP Server asynchronously
async def run_server():
    log.info("Starting Modbus TCP server on "+ args.ip  + ":" + args.p + " update every " + str(args.t) + " sec")
    
    # Start the server
    server = ModbusTcpServer(context=context, identity=identity, address=(args.ip, args.p))

    # Start updating holding registers concurrently
    await asyncio.gather(server.serve_forever(), update_holding_registers())

if __name__ == "__main__":
    asyncio.run(run_server())
