import asyncio
from time import sleep


async def put_log():
    print('startput')
    sleep(5)
    print('endput')


if __name__ == '__main__':
    print('start')
    log = put_log()
    asyncio.run(log)
    print('end')

