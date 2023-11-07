import asyncio
from time import perf_counter
from scrapli.driver.core import AsyncIOSXEDriver, AsyncEOSDriver
from typing import Callable
import sys
from conn_params import get_conn_details



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


async def do_work(work_queue: asyncio.Queue, callback: Callable[[dict], None]) -> None:
    while True:
        task_data = await work_queue.get()

        task_id = task_data['task_id']
        ip = task_data['ipaddr'].strip()
        model = task_data['model']
        commands = task_data['commands']
        status = task_data['status']

        start = perf_counter()

        if sys.read_only:
            task_ = task_retriever
        else:
            task_ = task

        if "OK" in str(status): #მოსაფიქრებელია უკეთესად, უნდა გამოირიცხოს OK კონფიგში
            result = status
        else:
            connector, conn_details = get_conn_details(model)
            try:
                result = await asyncio.wait_for(task_(ip, connector, conn_details, commands), timeout=60)
            except asyncio.TimeoutError:
                print("task timed out")
                result = "Task Timed Out"

        end = perf_counter()

        result = {
                "task_id": task_id,
                "result": result,
                "time_secs": end - start
            }
        callback(result)

        work_queue.task_done()

