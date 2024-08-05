import asyncio

loop = asyncio.get_event_loop()

def perform_sync(task):
    return loop.run_until_complete(task)


def perform_async(task):
    return loop.create_task(task)