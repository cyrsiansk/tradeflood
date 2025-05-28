from turn_system import turn, turn_execution, Turn, call__if_eq__, Call
import linktester


@turn_execution
def logOutage(*args):
    print("logOutage", *args)


@turn_execution
def checkSystem():
    print("checkSystem")
    return False


@turn_execution
def log(text):
    print(text)


@turn_execution
def log_result(call: Call):
    result = call()
    print(f"result: {result}")


@turn
def check1():
    call__if_eq__(checkSystem(), False,
                  Call(logOutage, "check1"))
    log("check1")


@turn
def check2():
    call__if_eq__(checkSystem(), False,
                  Call(logOutage, "check2"))
    log("check2")


@turn
def check3():
    call__if_eq__(checkSystem(), True,
                  Call(logOutage, "check3"))
    log("check3")


@turn
def check4():
    log_result(checkSystem())


@turn_execution
def print_execution(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")
    is_first = True
    for arg in args:
        if not is_first:
            print(sep, end="")

        if isinstance(arg, Call):
            print(arg(), end="")
        else:
            print(arg, end="")
        is_first = False
        print(end=end)


def print__():
    print("________________________________")
    print()


if __name__ == "__main__":
    print("Start")
    print__()

    source = linktester.BinanceHistoryFetcher()
    interface = linktester.InterfaceSearcher(source, linktester.Candle)

    with Turn():
        data = interface.get_data(0, 10, "BTCUSDT")
        print_execution(data)

    print__()

    with Turn():
        check1()
        check2()
        check3()
        check4()

    print__()

    with Turn():
        check1()
    with Turn():
        check2()

    print__()

    with Turn():
        logOutage("check separated")

    logOutage("check separated")
    check1()

    print__()
    print("End")
