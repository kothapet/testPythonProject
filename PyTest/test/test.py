'''
Created on Jul 17, 2017

@author: anand
'''

#===============================================================================
# the_world_is_flat=True
# print(the_world_is_flat)
# ##print(n)
# if the_world_is_flat:
#     print("Be careful dont fall off")
# 
# def fib_n(n):
#     a, b = 0, 1
#     while b < n:
#         print(b, end="->")
#         a, b = b, a+b
#     print()
# 
# fib_n(100)
# 
# print(range(10))
# 
# print(list(range(10)))
# 
# def prime_n(n):
#     for z in range(2, n):
#         for x in range(2, z):
#            if z % x == 0:
#                 print(z, 'equals', x, '*', z//x)
#                 break
#         else:
#             # loop fell through without finding a factor
#             print(z, 'is a prime number')
#     
# prime_n(20)         
#===============================================================================


#===============================================================================
# def towers_of_honoi(numDisks, poleS, poleD, poleT, counter=0):
#     
#     if numDisks > 1:
#         counter = towers_of_honoi(numDisks-1, poleS, poleT, poleD, counter)
#         counter=counter+1
#         print('Step ', counter, 'Move ', numDisks, ' Disk from pole ', poleS, ' to pole ', poleD)
#         counter = towers_of_honoi(numDisks-1, poleT, poleD, poleS, counter)
#     else:
#         counter=counter+1
#         print('Step ', counter, 'Move ', numDisks, ' Disk from pole ', poleS, ' to pole ', poleD)
#     
#     return counter    
# 
# towers_of_honoi(10, 'A', 'B', 'C') 
#===============================================================================
     
'''     
matrix = [
     [1, 2, 3, 4],
     [5, 6, 7, 8],
     [9, 10, 11, 12],
 ]

transposed = [[row[i] for row in matrix] for i in range(4)]

print(matrix) 
print(transposed)           
        

def ask_ok(prompt, retries=4, reminder='Please try again!'):
    while True:
        ok = input(prompt)
        if ok in ('y', 'ye', 'yes'):
            return True
        if ok in ('n', 'no', 'nop', 'nope'):
            return False
        retries = retries - 1
        if retries < 0:
            raise ValueError('invalid user response')
        print(reminder)

#y=ask_ok('Do you really want to quit?')
#y=ask_ok('OK to overwrite the file?', 2)
y=ask_ok('OK to overwrite the file?', 2, 'Come on, only yes or no!')

print(y)


def f(a, L=[]):
    L.append(a)
    return L

def f(a, L=None):
    if L is None:
        L = []
    L.append(a)
    return L

print(f(1))
print(f(2))
print(f(3))

L=[]
L=f(1)
print(L)
L=f(2,L)
print(L)
L=f(3,L)
print(L)

def parrot(voltage, state='a stiff', action='voom', type='Norwegian Blue'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.")
    print("-- Lovely plumage, the", type)
    print("-- It's", state, "!")


parrot()                     # required argument missing
parrot(voltage=5.0, 'dead')  # non-keyword argument after a keyword argument
parrot(110, voltage=220)     # duplicate value for the same argument
parrot(actor='John Cleese')  # unknown keyword argument
    
parrot(1000)                                          # 1 positional argument
parrot(voltage=1000)                                  # 1 keyword argument
parrot(voltage=1000000, action='VOOOOOM')             # 2 keyword arguments
parrot(action='VOOOOOM', voltage=1000000)             # 2 keyword arguments
parrot('a million', 'bereft of life', 'jump')         # 3 positional arguments
parrot('a thousand', state='pushing up the daisies')  # 1 positional, 1 keyword

def cheeseshop(kind, *arguments, **keywords):
    print("-- Do you have any", kind, "?")
    print("-- I'm sorry, we're all out of", kind)
    print("-" * 40)
    for arg in arguments:
        print(arg)
    print("-" * 40)
    for kw in keywords:
        print(kw, ":", keywords[kw])
        
cheeseshop("Limburger", "It's very runny, sir.",
           "It's really very, VERY runny, sir.",
           shopkeeper="Michael Palin",
           client="John Cleese",
           sketch="Cheese Shop Sketch")

def concat(*args, sep="/"):
    return sep.join(args)

print(concat("earth", "mars", "venus"))

print(concat("earth", "mars", "venus", sep="."))

print(list(range(3, 6)))
 
args = [3, 6]
print(*args)
print(list(range(*args)))       

def parrot(voltage, state='a stiff', action='voom'):
    print("-- This parrot wouldn't", action, end=' ')
    print("if you put", voltage, "volts through it.", end=' ')
    print("E's", state, "!")

d = {"voltage": "four million", "state": "bleedin' demised", "action": "VOOM"}
parrot(**d)

def make_incrementor(n):
    return lambda x: x + n

print(make_incrementor(10))

f = make_incrementor(42)

f = lambda x: x + 42

print(f(0))

print(f(1))

print(f(10))


pairs = [(1, 'one'), (2, 'two'), (3, 'three'), (4, 'four')]
pairs.sort(key=lambda pair: pair[1])
print(pairs)

def my_function():
    """
    Do nothing, but document it.

    No, really, it doesn't do anything.
    """
    pass

print(my_function.__doc__)

def f(ham: str, eggs: str = 'eggs') -> str:
    print("Annotations:", f.__annotations__)
    print("Arguments:", ham, eggs)
    return ham + ' and ' + eggs

print(f('spam'))
'''
list1 = []
list1.insert(1,'1')
list1.insert(2,'2')
print(list1[1])

list1 = [1,2,3,4,5]
for i in range(5):
    print(i, list1[i])
    
            

