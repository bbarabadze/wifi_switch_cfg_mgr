import asyncio
from scrapli.driver.core import AsyncIOSXEDriver, AsyncEOSDriver
from time import perf_counter
from conn_params import get_conn_details
from configs import get_model_cfg


async def task(host, connector, conn_details, commands):
    exc = "OK"

    try:
        async with connector(host, **conn_details) as conn:

            results = await conn.send_configs(commands, stop_on_failed=True)

            for i, cmd_res in enumerate(results):
                if cmd_res.failed:
                    exc = f'"{commands[i]}" Command Failed'

    except Exception as ex:
        exc = str(ex)
    finally:
        return exc

async def task_retriever(host, connector, conn_details, commands):

    exc = "OK"
    result = None

    try:
        async with connector(host, **conn_details) as conn:
            results = [await conn.send_command(command) for command in commands]
            result = results[-1].result
    except Exception as ex:
        exc = str(ex)
    finally:
        return exc, result


async def task_prep():
    
    with open("ip_model") as f:
        for line in f:
            ip, model = line.strip().split()
            connector, conn_details = get_conn_details(model)
            commands = get_model_cfg(model)
            print(ip, await task_retriever(ip, connector, conn_details, commands))



if __name__ == '__main__':
    t = perf_counter()
    asyncio.run(task_prep())
    print(perf_counter()-t)