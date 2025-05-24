from contextvars import ContextVar

execution_list = ContextVar("execution_list")
executions_list = ContextVar("executions_list")
execution_results = ContextVar("execution_results")
execution_list_block = ContextVar("execution_list_block", default=False)


class Call:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __eq__(self, other):
        if not isinstance(other, Call):
            return NotImplemented
        return (self.func == other.func and
                self.args == other.args and
                frozenset(self.kwargs.items()) == frozenset(other.kwargs.items()))

    def __hash__(self):
        return hash((
            self.func,
            self.args,
            frozenset(self.kwargs.items())
        ))

    def _sorted_kwargs(self):
        return dict(sorted(self.kwargs.items()))

    def __call__(self):
        call_results = execution_results.get()
        if self in call_results:
            return call_results[self]
        res = self.func(*self.args, **self.kwargs)
        call_results[self] = res
        return res

    def __repr__(self):
        return f"Call({self.func.__name__}, {self.args}, {self.kwargs})"


class Turn:
    _depth = ContextVar("turn_depth", default=0)

    def __enter__(self):
        depth = self._depth.get()
        self._depth.set(depth + 1)

        if depth == 0:
            executions_list.set([])
            execution_results.set({})

        execution_list.set(None)
        execution_list_block.set(False)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        depth = self._depth.get() - 1
        self._depth.set(depth)

        if depth == 0:
            execution_list_block.set(True)
            for ex_list in executions_list.get():
                for call in ex_list:
                    call()
            execution_list_block.set(False)

            executions_list.set([])
            execution_list.set(None)
            execution_results.set({})

        return False


from functools import wraps

def turn(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ex_list = execution_list.get()
        i_am_owner = True
        if ex_list is None:
            ex_list = []
            execution_list.set(ex_list)
        else:
            i_am_owner = False

        res = func(*args, **kwargs)

        if i_am_owner:
            exs_list = executions_list.get()
            exs_list.append(ex_list)
            execution_list.set(None)

        return res

    return wrapper


def _turn_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ex_list = execution_list.get()
        call = Call(func, *args, **kwargs)
        block = execution_list_block.get()
        if not block:
            ex_list.append(call)
        return call

    return wrapper


def turn_execution(func):
    return turn(_turn_execution(func))


def _turn_execution_blocker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ex_list = execution_list.get()
        execution_list_block.set(True)
        call = Call(func, *args, **kwargs)
        ex_list.append(call)
        execution_list_block.set(False)
        return call

    return wrapper


def turn_execution_blocker(func):
    return turn(_turn_execution_blocker(func))



@turn_execution_blocker
def call__if_eq__(call: Call, eq_other, call_activation: Call):
    res = call()
    if res == eq_other:
        call_activation()()
