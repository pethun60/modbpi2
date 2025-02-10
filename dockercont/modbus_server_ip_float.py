#!/usr/bin/env python3

import asyncio
import struct
from pymodbus.server.async_io import ModbusTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSequentialDataBlock
from pymodbus.device import ModbusDeviceIdentification
import logging
import argparse

# Configure logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.INFO)

# Global variable to track the floating-point register value
change_var = 100.0  # Now a float
parser = argparse.ArgumentParser(description='assign different IP address')
parser.add_argument('-ip', default='localhost', help='IP of the Modbus server in quotes"')
parser.add_argument('-p', default='5020', help='Port of Modbus server')
parser.add_argument('-t', type=int, default=1, help='Time interval for updates in seconds')
args = parser.parse_args()

# Helper function to convert float to two 16-bit registers
def float_to_registers(value):
    packed = struct.pack('>f', value)  # Pack the float as a big-endian 32-bit float
    return struct.unpack('>HH', packed)  # Unpack it into two 16-bit unsigned integers

# Modbus Data Store with initial values for holding registers as 32-bit floats
initial_float = float_to_registers(change_var)
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17] * 100),  # Discrete Inputs
    co=ModbusSequentialDataBlock(0, [17] * 100),  # Coils
    hr=ModbusSequentialDataBlock(0, list(initial_float) * 400),  # Holding Registers as floats
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

# Function to update holding registers with float values
async def update_holding_registers():
    global change_var
    while True:
        # Increment the float value
        change_var += 1.6
        if change_var > 100.0:
            change_var = 1.0
        
        # Convert float to two 16-bit registers and update the holding registers
        registers = float_to_registers(change_var)
        store.setValues(3, 0, list(registers) * 155)  # Update all holding registers with float
        log.info(f"Updated holding registers with float value: {change_var}")
        await asyncio.sleep(args.t)  # Wait for the specified time

# Start TCP Server asynchronously
async def run_server():
    log.info(f"Starting Modbus TCP server on {args.ip}:{args.p} update every {args.t} sec")
    
    # Start the server
    server = ModbusTcpServer(context=context, identity=identity, address=(args.ip, int(args.p)))

    # Start updating holding registers concurrently
    await asyncio.gather(server.serve_forever(), update_holding_registers())

if __name__ == "__main__":
    asyncio.run(run_server())
