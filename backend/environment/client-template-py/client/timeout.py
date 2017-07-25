from threading import Thread
import functools


def timeout(time_limit):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [Exception('function [%s] timeout [%s seconds] exceeded!' % (func.__name__, time_limit))]

            def new_func():
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as e:
                    res[0] = e
            t = Thread(target=new_func)
            t.daemon = True
            try:
                t.start()
                t.join(time_limit)
            except Exception as je:
                print("error starting thread")
                raise je
            ret = res[0]
            if isinstance(ret, BaseException):
                raise ret
            return ret
        return wrapper
    return deco


@timeout(2)
def myFunc():
    while True:
        print("s")

if __name__ == '__main__':
    func = timeout(time_limit=2)(myFunc)
    try:
        func()
    except Exception as ex:
        print(ex)
