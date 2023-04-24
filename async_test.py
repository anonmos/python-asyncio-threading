from time import sleep
from asyncio import set_event_loop, get_event_loop, new_event_loop, gather, sleep as async_sleep, AbstractEventLoop, run_coroutine_threadsafe, create_task, all_tasks
from threading import Thread

class RunAsyncThings():
    def __init__(self):
        self.result_dict = {}
        self.event_loop = new_event_loop()
        self.thread = None
        self.gathered_things = None

    def thread_loop_func(self, loop: AbstractEventLoop, gathered_things, result_dict) -> None:
        set_event_loop(loop)
        result = loop.run_until_complete(gathered_things)
        result_dict['result'] = result

    async def async_thing(self, x, wait_time):
        await async_sleep(wait_time)
        return x * wait_time

    def async_things(self, wait_time=1):
        self.gathered_things = gather(*[self.event_loop.create_task(self.async_thing(x, wait_time)) for x in range(10)])
        self.thread = Thread(target=self.thread_loop_func, args=(self.event_loop, self.gathered_things, self.result_dict), daemon=True)
        self.thread.start()
        print("Tasks scheduled")
    
    def things_done(self):
        if 'result' in self.result_dict:
            self.thread.join()
            self.event_loop.close()
            return self.result_dict['result']
        else:
            return False
    
    def cancel_things(self):
        if self.gathered_things is not None and self.gathered_things.cancelled() is not True and self.event_loop is not None and self.event_loop.is_closed() is not False and self.thread is not None and self.thread.is_alive() is True:
            self.gathered_things.cancel()
            self.event_loop.stop()
            self.event_loop.close()
            self.thread.join(1)

            if self.thread.is_alive():
                print("Thread still alive?  Zombie thread!")
            
            if not self.gathered_things.cancelled():
                print("Gathered things is still running.  Zombie task!")
            
            if not self.event_loop.is_closed():
                print("Event loop is still open.  Zombie event loop!")

            self.event_loop = None
            self.thread = None
            self.gathered_things = None

def main():
    async_things_runner = RunAsyncThings()
    second_async_things_runner = RunAsyncThings()
    async_things_runner.async_things()
    second_async_things_runner.async_things(20)

    print("Some")
    if not async_things_runner.things_done():
        print("Async 1 still running")
    if not second_async_things_runner.things_done():
        print("Async 2 still running")
    sleep(3)
    print("Things")
    if not async_things_runner.things_done():
        print("Async still running")
    if not second_async_things_runner.things_done():
        print("Async 2 still running")
    sleep(3)
    print("Being")
    if not async_things_runner.things_done():
        print("Async still running")
    if not second_async_things_runner.things_done():
        print("Async 2 still running")
    sleep(3)
    print("Done")
    if not async_things_runner.things_done():
        print("Async still running")
    if not second_async_things_runner.things_done():
        print("Async 2 still running")
    sleep(3)

    while(not async_things_runner.things_done()):
        print("Waiting")
        sleep(1)
    
    if not second_async_things_runner.things_done():
        print("Async 2 still running, cancelling it")
    else:
        print("Async 2 done, printing things")
        print(second_async_things_runner.things_done())
    
    print("Printing things: ")
    print(async_things_runner.things_done())


if __name__ == "__main__":
    main()
