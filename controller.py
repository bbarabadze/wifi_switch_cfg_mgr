import asyncio
from time import perf_counter
from typing import Callable, List

import consumer
import producer


NUM_WORKERS = 100
WORK_QUEUE_MAX_SIZE = 200

NUM_RESULT_HANDLERS = 50
RESULT_QUEUE_MAX_SIZE = 200


async def _controller(
        batch: List[dict],
        datalen,
        task_completed_callback: Callable[[dict], None],
        job_completed_callback: Callable[[dict], None]
) -> None:
    start = perf_counter()

    work_queue = asyncio.Queue(maxsize=WORK_QUEUE_MAX_SIZE)
    #result_queue = asyncio.Queue(maxsize=RESULT_QUEUE_MAX_SIZE)

    tasks = []

    producer_completed = asyncio.Event()
    producer_completed.clear()

    tasks.append(
        asyncio.create_task(producer.produce_work(batch, datalen, work_queue, producer_completed))
    )

    for _ in range(NUM_WORKERS):
        tasks.append(
            asyncio.create_task(consumer.do_work(work_queue, task_completed_callback))
        )

    # for _ in range(NUM_RESULT_HANDLERS):
    #     tasks.append(
    #         asyncio.create_task(resulthandler.handle_task_result(result_queue, task_completed_callback))
    #     )

    await producer_completed.wait()
    print("CP 1")
    await work_queue.join()
    #await result_queue.join()
    print("CP 2")
    for task in tasks:
        task.cancel()

    end = perf_counter()
    print("CP 3")
    job_completed_callback({"Elapsed_secs": end - start})
    print("CP 4")
    #await asyncio.sleep(10)


def run_job(
        batch: List[dict], datalen,
        task_completed_callback: Callable[[dict], None],
        job_completed_callback: Callable[[dict], None]
) -> None:
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(_controller(batch, task_completed_callback, job_completed_callback))

    asyncio.get_event_loop().run_until_complete(_controller(batch, datalen, task_completed_callback, job_completed_callback))
    print("CP 5")