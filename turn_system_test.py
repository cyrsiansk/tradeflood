from turn_system import turn, turn_execution, Turn, call__if_eq__, Call


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


@turn
def check1():
    call__if_eq__(checkSystem(), False, Call(logOutage, "check1"))
    log("check1")


@turn
def check2():
    call__if_eq__(checkSystem(), False, Call(logOutage, "check2"))
    log("check2")


@turn
def check3():
    call__if_eq__(checkSystem(), True, Call(logOutage, "check3"))
    log("check3")


def print__():
    print("________________________________")
    print()


if __name__ == "__main__":
    print("Start")
    print__()

    with Turn():
        check1()
        check2()
        check3()

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
