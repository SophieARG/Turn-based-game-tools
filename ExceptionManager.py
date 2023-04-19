import time, threading, traceback

MAXTIME = 1e-4

class Timeout(Exception):
    pass

class Call:
    def __init__(self, func):
        self.func = func
        self.result = None
        self.state = Timeout()
        
    def call(self, *args, **kwargs):
        try:
            begin = time.perf_counter()
            self.result = self.func(*args, **kwargs)
            end = time.perf_counter()
            self.state = end - begin
        except Exception as exception:
            self.state = exception

class Player:
    def __init__(self, name, instance):
        self.name = name
        self.instance = instance
        self.time = 0
        self.error = None

    def call(self, funcname, *args, **kwargs):
        if self.error is not None: return
        try:
            result = Call(getattr(self.instance, funcname))
            thread = threading.Thread(target = result.call, args = (*args, ), kwargs = {**kwargs})
            thread.daemon = True
            thread.start()
            thread.join(MAXTIME - self.time)
            if isinstance(result.state, Exception): raise result.state
            self.time += result.state
            if self.time >= MAXTIME: raise Timeout()
        except:
            self.error = traceback.format_exc()
