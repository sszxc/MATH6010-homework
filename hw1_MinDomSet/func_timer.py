# Author: Xuechao Zhang
# Date: March 26th, 2022
# Description: Implementing function timing with function decorators

import functools
import datetime

def timeit(func):
    '''
    用函数装饰器实现函数计时
    '''
    @functools.wraps(func)
    def wrapper(*args, **kw):
        starttime = datetime.datetime.now()
        f = func(*args, **kw)
        endtime = datetime.datetime.now()
        print('Called %s(), ' % func.__name__, end='')
        print('Execution time ', end='')
        print(endtime - starttime)
        return f
    return wrapper