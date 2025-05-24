from turn_system import Turn, turn_execution, turn, call__if_eq__, Call, turn_execution_blocker


def run_test(name, fn):
    print(f"\n=== Running test: {name} ===")
    try:
        fn()
        print(f"[PASS] {name}")
    except AssertionError as e:
        print(f"[FAIL] {name}: {e}")


def test_lazy_execution():
    executed = []

    @turn_execution
    def foo():
        executed.append("foo")

    with Turn():
        foo()
        assert not executed, "Function should not be executed immediately"

    assert executed == ["foo"], "Function should be executed on Turn exit"


def test_deduplication():
    executed = []

    @turn_execution
    def foo():
        executed.append("foo")

    with Turn():
        f1 = foo()
        f2 = foo()
        assert f1 == f2, "Should return same Call object"
        assert not executed

    assert executed == ["foo"], "Function should be executed only once"


def test_arguments_uniqueness():
    executed = []

    @turn_execution
    def foo(x):
        executed.append(x)

    with Turn():
        foo(1)
        foo(2)

    assert executed == [1, 2], "Both calls with different args should execute"


def test_call_if_eq_true():
    executed = []

    @turn_execution
    def check():
        return 1

    @turn_execution
    def on_true():
        executed.append("yes")

    @turn
    def run():
        call__if_eq__(check(), 1, Call(on_true))

    with Turn():
        run()

    assert executed == ["yes"], "on_true should be executed"


def test_call_if_eq_false():
    executed = []

    @turn_execution
    def check():
        return 0

    @turn_execution
    def on_true():
        executed.append("yes")

    @turn
    def run():
        call__if_eq__(check(), 1, Call(on_true))

    with Turn():
        run()

    assert not executed, "on_true should not be executed"


def test_multiple_turns():
    order = []

    @turn_execution
    def a():
        order.append("a")

    @turn_execution
    def b():
        order.append("b")

    @turn
    def turn1():
        a()

    @turn
    def turn2():
        b()

    with Turn():
        turn1()
        turn2()

    assert order == ["a", "b"], "Both turns should execute in order"


def test_nested_call_graph():
    result = []

    @turn_execution
    def step1():
        result.append("1")

    @turn_execution
    def step2():
        result.append("2")

    @turn
    def pipeline():
        step1()
        step2()

    with Turn():
        pipeline()

    assert result == ["1", "2"], "Pipeline should be executed in order"


def test_manual_call_returns_cached():
    @turn_execution
    def f():
        return 42

    with Turn():
        c = f()
        res1 = c()
        res2 = c()
        assert res1 == 42 and res2 == 42


def test_call_executes_before_exit():
    executed = []

    @turn_execution
    def f():
        executed.append("run")
        return 99

    with Turn():
        c = f()
        assert c() == 99
        assert executed == ["run"]


def test_call_eq_and_hash():
    def dummy(): pass

    c1 = Call(dummy, 1, 2, x=3)
    c2 = Call(dummy, 1, 2, x=3)
    c3 = Call(dummy, 1, 2, x=4)

    assert c1 == c2
    assert hash(c1) == hash(c2)
    assert c1 != c3


def test_call_eq_different_func():
    def a(): pass

    def b(): pass

    assert Call(a) != Call(b)


def test_nested_turns():
    called = []

    @turn_execution
    def f(x):
        called.append(x)

    with Turn():
        f(1)
        with Turn():
            f(2)
        f(3)

    assert called == [1, 2, 3]


def test_blocker_forces_call():
    called = []

    @turn_execution
    def f(): called.append("normal")

    @turn_execution_blocker
    def g(): called.append("blocked")

    with Turn():
        f()
        g()

    assert called in [["blocked", "normal"], ["normal", "blocked"]]


def test_conditional_call_skips():
    called = []

    @turn_execution
    def check(): return 1

    def should_not_run(): called.append("fail")

    c = Call(should_not_run)

    @turn
    def run():
        call__if_eq__(check(), 2, c)

    with Turn():
        run()

    assert not called


def test_parallel_turns():
    result = []

    @turn_execution
    def a(): result.append("a")

    @turn_execution
    def b(): result.append("b")

    @turn
    def t1(): a()

    @turn
    def t2(): b()

    with Turn():
        t1()
        t2()

    assert set(result) == {"a", "b"}


def test_call_kwargs_affect_identity():
    def f(x=0): return x

    c1 = Call(f, x=1)
    c2 = Call(f, x=2)
    assert c1 != c2


def test_call_manual_outside_turn():
    called = []

    def f():
        called.append(1)
        return 3

    c = Call(f)
    result = c()
    assert result == 3
    assert called == [1]
