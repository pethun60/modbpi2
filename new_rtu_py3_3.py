#!/usr/bin/env python3
"""
Pymodbus AsyncIO Server Example
--------------------------------------------------------------------------
This script demonstrates how to create an asyncio-based Modbus server
using Pymodbus with StartAsyncSerialServer.
"""
import asyncio
import logging
from pymodbus.server.async_io import StartAsyncSerialServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer
from pymodbus import __version__ as version

# Configure logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

# Global variables
change_var = 120
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17] * 100),
    co=ModbusSequentialDataBlock(0, [17] * 100),
    hr=ModbusSequentialDataBlock(0x00, [change_var] * 6000),
    ir=ModbusSequentialDataBlock(0, [17] * 100),
)
context = ModbusServerContext(slaves=store, single=True)

# Async function to update Modbus registers periodically
async def update_registers_periodically():
    global context, change_var
    while True:
        change_var += 10
        context[0].setValues(3, 10, [change_var] * 90)  # Update HR 10–99
        context[0].setValues(3, 522, [change_var] * 96)  # Update HR 522–617
        context[0].setValues(3, 1034, [change_var] * 88)  # Update HR 1034–1121
        context[0].setValues(3, 1546, [change_var] * 88)  # Update HR 1546–1633
        context[0].setValues(3, 2570, [change_var] * 149)  # Update HR 2570–2718
        if change_var > 1000:
            change_var = 0
        await asyncio.sleep(2)

# Async function to run the Modbus server
async def run_server():
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = version

    # Start the Modbus RTU server with proper arguments
    await StartAsyncSerialServer(
        context=context,
        framer=ModbusRtuFramer,
        identity=identity,
        port='/dev/ttyUSB0',
        baudrate=9600,
        parity='E',
        bytesize=8,
        stopbits=1,
        ignore_missing_slaves=True,
    )

# Main function to handle environments with running event loops
def main():
    loop = asyncio.get_event_loop()
    loop.create_task(update_registers_periodically())
    loop.create_task(run_server())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        log.info("Server stopped by user")

if __name__ == "__main__":
    main()

