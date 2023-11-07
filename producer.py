import asyncio
from typing import List
from tqdm import tqdm
import sys

async def produce_work(
        batch: List[dict], datalen, work_queue: asyncio.Queue, producer_completed: asyncio.Event
) -> None:

    for data in tqdm(batch, file=sys.stdout, total=datalen):
        await work_queue.put(data)

    producer_completed.set()
