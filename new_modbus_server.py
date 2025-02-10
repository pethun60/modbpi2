#!/usr/bin/env python3

import asyncio
from pymodbus.server.async_io import ModbusTcpServer  # Updated import for TCP Server
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Modbus Data Store
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17] * 100),  # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [17] * 100),  # Coils
    hr=ModbusSequentialDataBlock(0, [100] * 100),  # Holding Registers
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

# Start TCP Server asynchronously
async def run_server():
    log.info("Starting Modbus TCP server on localhost:5020")
    server = ModbusTcpServer(context=context, identity=identity, address=("localhost", 5020))
    await server.serve_forever()  # Start the server

if __name__ == "__main__":
    asyncio.run(run_server())
