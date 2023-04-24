from time import sleep
from asyncio import set_event_loop, get_event_loop, new_event_loop, gather, sleep as async_sleep, AbstractEventLoop, run_coroutine_threadsafe, create_task, all_tasks
from threading import Thread

class RunAsyncThings():
    def __init__(self):
        self.result_dict = {}
        self.event_loop = new_event_loop()
        self.thread = None

    def thread_loop_func(self, loop: AbstractEventLoop, gathered_things, result_dict) -> None:
        set_event_loop(loop)
        result = loop.run_until_complete(gathered_things)
        result_dict['result'] = result

    async def async_thing(self, x):
        await async_sleep(1)
        return x

    def async_things(self):
        gathered_things = gather(*[self.event_loop.create_task(self.async_thing(x)) for x in range(10)])
        self.thread = Thread(target=self.thread_loop_func, args=(self.event_loop, gathered_things, self.result_dict), daemon=True)
        self.thread.start()
        print("Tasks scheduled")
    
    def things_done(self):
        if 'result' in self.result_dict:
            self.thread.join()
            self.event_loop.close()
            return self.result_dict['result']
        else:
            return False

def main():
    async_things_runner = RunAsyncThings()
    second_async_things_runner = RunAsyncThings()
    async_things_runner.async_things()
    second_async_things_runner.async_things()

    print("Some")
    if not async_things_runner.things_done():
        print("Async still running")
    sleep(3)
    print("Things")
    if not async_things_runner.things_done():
        print("Async still running")
    sleep(3)
    print("Being")
    if not async_things_runner.things_done():
        print("Async still running")
    sleep(3)
    print("Done")
    if not async_things_runner.things_done():
        print("Async still running")
    sleep(3)

    while(not async_things_runner.things_done()):
        print("Waiting")
        sleep(1)
    
    print("Printing things: ")
    print(async_things_runner.things_done())
    print(second_async_things_runner.things_done())


if __name__ == "__main__":
    main()
