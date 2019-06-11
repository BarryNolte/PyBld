"""Decorators for makefiles's."""
from time import perf_counter

# store the target descriptions here, this is a little
# convoluted, but it seems to work
descriptions = {}
def buildTarget(func):
    """Build a Target.

    Function decorator to signify that the function
    is a build target.
    """
    # Save the descriptions, see note above
    descriptions[func.__name__] = func.__doc__
    
    def decorator_func(*args, **kwargs):
        start_time = perf_counter()

        # Call Decorated Function
        returnValue = func(*args, **kwargs)

        end_time = perf_counter()
        run_time = end_time - start_time

        if returnValue is None or returnValue is False:
            return False, run_time

        return True, run_time

    return decorator_func
