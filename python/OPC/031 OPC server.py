import asyncio
import logging

from asyncua import Server, ua
from asyncua.common.methods import uamethod

import time

@uamethod
def func(parent, value):
    return value * 2


async def main():
    _logger = logging.getLogger(__name__)
    # setup our server
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://10.10.10.217:4840")

    # set up our own namespace, not really necessary but should as spec
    uri = "OPC_SIMULATION_SERVER"
    idx = await server.register_namespace(uri)

    # populating our address space
    # server.nodes, contains links to very common nodes like objects and root
    myobj = await server.nodes.objects.add_object(idx, "EstacionDeGas")
    
    myvar = await myobj.add_variable(idx, "MyVariable", 0.0)
    # Set MyVariable to be writable by clients
    await myvar.set_writable()
    await server.nodes.objects.add_method(
        ua.NodeId("ServerMethod", idx),
        ua.QualifiedName("ServerMethod", idx),
        func,
        [ua.VariantType.Int64],
        [ua.VariantType.Int64],
    )
    _logger.info("Starting server!")
    async with server:
        while True:
            await asyncio.sleep(1) #tiempo de espera en segundos
            new_val = await myvar.get_value() + 0.1
            _logger.info("Set value of %s to %.1f", myvar, new_val)
            await myvar.write_value(new_val)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=False)
