from functools import partial
from random import seed
from uuid import uuid4
from controller import run_job
from pprint import pprint
import sys
from data_reader import get_wbook
import argparse


sys.read_only = False
result = {}
data = []
wb = None
st = ""



def main(job_id: str) -> None:
    global FILE_NAME
    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument("file_name", help='Name of a Properly Formatted .xlsx File', type=str)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', '--read', action='store_true',
                       help='enable read mode')
    group.add_argument('-w', '--write', action='store_true',
                       help='enable write mode')

    args = parser.parse_args()
    sys.read_only = args.read
    FILE_NAME = args.file_name

    print(f'Starting job {job_id}')

    task_callback = partial(task_completed_callback_handler, job_id)
    job_callback = partial(job_completed_callback_handler, job_id)
    global wb
    global st
    wb, st, datalen, task_data = get_wbook(FILE_NAME)

    #
    # task_data = [
    #     {"task_id": i, "ipaddr": ip.strip(), "commands": ['no alias cwmp qwe qwe', 'do wr']}
    #     for i, (code, ip) in enumerate(data)
    # ]

    run_job(task_data, datalen, task_callback, job_callback)


def task_completed_callback_handler(job_id: str, callback_message: dict) -> None:
    #print(f'Task Completed in {job_id=}: {callback_message=}')
    global wb
    global st
    i = callback_message["task_id"]
    cell_id = st + str(i + 2)
    sheet = wb['cfgdata']
    sheet[cell_id].value = str(callback_message["result"])



def job_completed_callback_handler(job_id: str, callback_message: dict) -> None:

    print(f'Job {job_id} completed: {callback_message=}')
    close_xls(FILE_NAME)


def close_xls(file_name):
    global wb
    while True:
        try:
            wb.save(file_name)
            break
        except Exception as ex:
            print(str(ex))
            input("Close The File And Press Enter:")



if __name__ == '__main__':
    sys.stderr = open("errors.txt", "w")
    seed(0)
    main(str(uuid4()))
































































