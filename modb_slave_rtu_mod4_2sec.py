#!/usr/bin/env python
"""
Pymodbus Asynchronous Server Example
--------------------------------------------------------------------------

The asynchronous server is a high performance implementation using the
twisted library as its backend.  This allows it to scale to many thousands
of nodes which can be helpful for testing monitoring software.
"""
# --------------------------------------------------------------------------- # 
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.version import version
from pymodbus.server.asynchronous import StartTcpServer
from pymodbus.server.asynchronous import StartUdpServer
from pymodbus.server.asynchronous import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import (ModbusRtuFramer,
                                  ModbusAsciiFramer,
                                  ModbusBinaryFramer)
from custom_message import CustomModbusRequest

# --------------------------------------------------------------------------- # 
# configure the service logging
# --------------------------------------------------------------------------- # 
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

import time
from threading import Thread

change_var = 120
interval_time =10
store = ModbusSlaveContext(
    di=ModbusSequentialDataBlock(0, [17]*100),
    co=ModbusSequentialDataBlock(0, [17]*100),
    hr=ModbusSequentialDataBlock(0x00, [change_var]*6000),
    ir=ModbusSequentialDataBlock(0, [17]*100))
store.register(CustomModbusRequest.function_code, 'cm',
               ModbusSequentialDataBlock(0, [0]*100))
context = ModbusServerContext(slaves=store, single=True)

# Function to update Modbus registers 0-100
def run_async_server():
    global store
    global context

    # ----------------------------------------------------------------------- # 
    # initialize your data store
    # ----------------------------------------------------------------------- # 
    # The datastores only respond to the addresses that they are initialized to
    # Therefore, if you initialize a DataBlock to addresses from 0x00 to 0xFF,
    # a request to 0x100 will respond with an invalid address exception.
    # This is because many devices exhibit this kind of behavior (but not all)
    #
    #      block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    #
    # Continuing, you can choose to use a sequential or a sparse DataBlock in
    # your data context.  The difference is that the sequential has no gaps in
    # the data while the sparse can. Once again, there are devices that exhibit
    # both forms of behavior::
    #
    #     block = ModbusSparseDataBlock({0x00: 0, 0x05: 1})
    #     block = ModbusSequentialDataBlock(0x00, [0]*5)
    #
    # Alternately, you can use the factory methods to initialize the DataBlocks
    # or simply do not pass them to have them initialized to 0x00 on the full
    # address range::
    #
    #     store = ModbusSlaveContext(di = ModbusSequentialDataBlock.create())
    #     store = ModbusSlaveContext()
    #
    # Finally, you are allowed to use the same DataBlock reference for every
    # table or you you may use a seperate DataBlock for each table.
    # This depends if you would like functions to be able to access and modify
    # the same data or not::
    #
    #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
    #     store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
    #
    # The server then makes use of a server context that allows the server to
    # respond with different slave contexts for different unit ids. By default
    # it will return the same context for every unit id supplied (broadcast
    # mode).
    # However, this can be overloaded by setting the single flag to False
    # and then supplying a dictionary of unit id to context mapping::
    #
    #     slaves  = {
    #         0x01: ModbusSlaveContext(...),
    #         0x02: ModbusSlaveContext(...),
    #         0x03: ModbusSlaveContext(...),
    #     }
    #     context = ModbusServerContext(slaves=slaves, single=False)
    #
    # The slave context can also be initialized in zero_mode which means that a
    # request to address(0-7) will map to the address (0-7). The default is
    # False which is based on section 4.4 of the specification, so address(0-7)
    # will map to (1-8)::
    #
    #     store = ModbusSlaveContext(..., zero_mode=True)
    # ----------------------------------------------------------------------- # 
    #store = ModbusSlaveContext(
    #    di=ModbusSequentialDataBlock(0, [17]*100),
    #    co=ModbusSequentialDataBlock(0, [17]*100),
    #    hr=ModbusSequentialDataBlock(0x00, [change_var]*6000),
    #    ir=ModbusSequentialDataBlock(0, [17]*100))
    #store.register(CustomModbusRequest.function_code, 'cm',
    #               ModbusSequentialDataBlock(0, [0]*100))
    #context = ModbusServerContext(slaves=store, single=True)
    
    # ----------------------------------------------------------------------- # 
    # initialize the server information
    # ----------------------------------------------------------------------- # 
    # If you don't set this or any fields, they are defaulted to empty strings.
    # ----------------------------------------------------------------------- # 
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = version.short()
    
    # ----------------------------------------------------------------------- # 
    # run the server you want
    # ----------------------------------------------------------------------- # 

    # TCP Server

    #StartTcpServer(context, identity=identity, address=("localhost", 5020),
    #               custom_functions=[CustomModbusRequest])

    # TCP Server with deferred reactor run

    # from twisted.internet import reactor
    # StartTcpServer(context, identity=identity, address=("localhost", 5020),
    #                defer_reactor_run=True)
    # reactor.run()

    # Server with RTU framer
    # StartTcpServer(context, identity=identity, address=("localhost", 5020),
    #                framer=ModbusRtuFramer)

    # UDP Server
    # StartUdpServer(context, identity=identity, address=("127.0.0.1", 5020))

    # RTU Server
    StartSerialServer(context, identity=identity,
                       port='/dev/ttyUSB0', framer=ModbusRtuFramer,
                       baudrate=9600,
                       parity='E',
                       bytesize=8,
                       stopbits=1,
                       ignore_missing_slaves=True)

    # ASCII Server
    #StartSerialServer(context, identity=identity, 
    #                   port='/dev/ttyUSB0', framer=ModbusAsciiFramer,
    #                   baudrate=9600,
    #                   parity='N',
    #                   bytesize=8,
    #                   stopbits=1,
    #                   ignore_missing_slaves=True)

    # Binary Server
    # StartSerialServer(context, identity=identity,
    #                   port='/dev/ttyp0', framer=ModbusBinaryFramer)
    # Function to update Modbus registers 0-100


def update_all_modbus_registers(start_address, end_address, value):
    global context  # Declare global context
    if context is not None:
        # Update the values for all registers in the range start_address to end_address
        context[0].setValues(3, start_address, [value] * (end_address - start_address + 1))
        print ("Updated registers ", start_address, end_address, value)




if __name__ == "__main__":
    #run_async_server()
    server_thread = Thread(target=run_async_server, args=())
    server_thread.daemon = True
    server_thread.start()
    while True :
        change_var +=10
    # Update registers 0-3000 with new values incremented by 10
        update_all_modbus_registers(10, 99, change_var)
        update_all_modbus_registers(522, 617, change_var)
        update_all_modbus_registers(1034, 1121, change_var)
        update_all_modbus_registers(1546, 1633, change_var)
        update_all_modbus_registers(2570, 2718, change_var)
        if change_var > 1000 :
            change_var = 0
        time.sleep(2) 


