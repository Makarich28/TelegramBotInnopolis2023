from time import time

def time_measure(func):
    def wrapper(*args, **kwargs):
        before = time()
        a = func(*args, **kwargs)
        after = time()
        t = after - before
        print(f'Функция {func.__name__}  выполнялась {after-before}')
        return t
    return wrapper

def timer(func,*args,**kwargs):
        before = time()
        a = func(*args, **kwargs)
        after = time()
        t = after - before
        return t
