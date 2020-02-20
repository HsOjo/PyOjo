import time


def wait_and_check(wait: float, step: float):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            for i in range(int(wait // step)):
                if not func(*args, **kwargs):
                    return False
                time.sleep(step)
            time.sleep(wait % step)
            return True

        return _wrapper

    return wrapper


def time_count(func):
    def wrapper(*args, **kwargs):
        t = time.time()
        result = func(*args, **kwargs)
        print('%s time usage: %f' % (func.__name__, time.time() - t))
        return result

    return wrapper


def try_exec(return_=False):
    def wrapper(func):
        def _wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if return_:
                    return result
                else:
                    return True
            except:
                return False

        return _wrapper

    return wrapper
