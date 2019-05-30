from time import perf_counter


def target(func):
    """
    This is a decorator function
    :param func: (function)
    :return:
    """
    def decorator_func(*args, **kwargs):
        start_time = perf_counter()

        returnValue = func(*args, **kwargs)

        end_time = perf_counter()
        run_time = end_time - start_time
        # print(f"Finished {func.__name__!r} in {run_time:.4f} secs")

        if returnValue is None or returnValue is False:
            return False, run_time
        else:
            return True, run_time

    return decorator_func
