# def mut(a,b):
#     return a*b
# def sub(a,b):
#     return a-b
#
# def function_father(x):
#     def inside_function(repeat):
#         print(x*repeat)
#     return inside_function
#
# first = function_father("hello")
# second = function_father(2)
# # first(1)
# # second(3)
# # first(3)
#
# def double(func):
#     def wrapper(*args):
#         return func(*args) * 2
#     return wrapper
#
# def undouble(func):
#     def wrapper(a, b):
#         return func(a, b) / 2
#     return wrapper
#
# summ = double(summ)
# print(summ(2, 2))
# summ = undouble(summ)
# print(summ(2, 2))
#
# @double
# def summ(a, b):
#     return a+b
#
# @double
# def mut(a, b):
#     return a*b
#
# @double
# def sub(a, b):
#     return a-b
from time import time, sleep

def time_measure(func):
    def wrapper(*args, **kwargs):
        before = time()
        a = func(*args, **kwargs)
        after = time()
        t = after - before
        print(f'Функция {func.__name__}  выполнялась примерно {after-before}')
        return t
    return wrapper

def sleeper(t):
    sleep(t)

# first = time_measure(sleeper)
# first(5)

def timer(func,*args,**kwargs):
        before = time()
        a = func(*args, **kwargs)
        after = time()
        t = after - before
        return t
