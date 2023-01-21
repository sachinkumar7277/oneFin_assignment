import os
import json
import dotenv


def retry(times, exceptions):
    """
    Retry Decorator
    It takes two arguments times (number of times you want to retry) and list of exceptions
    and it wrapp a function/method
    :param times: The number of times to repeat the wrapped function/method
    :type times: Int
    :param Exceptions: Lists of exceptions that trigger a retry attempt
    :type Exceptions: Tuple of Exceptions
    """
    def decorator(func):
        def fn(*args, **kwargs):
            retry_times = 0
            while retry_times < times:
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    print(exceptions)
                    print(
                        'Exception thrown when attempting to run %s, retry_times '
                        '%d of %d' % (func, retry_times, times)
                    )
                    retry_times += 1
            return func(*args, **kwargs)
        return fn
    return decorator
