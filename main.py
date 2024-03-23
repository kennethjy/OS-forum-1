import sys
import threading
import random
import time
from queue import Queue

BUFFER_SIZE = 100


# Stack class
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        if len(self.stack) >= BUFFER_SIZE:
            return False
        self.stack.append(item)
        return True

    def pop(self):
        item = self.stack.pop()
        return item

    def getTop(self):
        if len(self.stack) == 0:
            return "empty"
        return self.stack[-1]


# Function to generate random numbers and push them into the stack
def number_generator(stack):
    global gen_turn, gen_arr
    i = 0
    max_count = 10000
    lower_bound = 1
    upper_bound = 10000
    filename = "all.txt"
    f = open(filename, 'w')
    f.close()
    while i < max_count:
        while not gen_turn:
            if len(gen_arr) > 0:
                with open(filename, 'a') as f:
                    f.write(f"{gen_arr.pop()}\n")
            pass
        num = random.randint(lower_bound, upper_bound)
        while stack.push(num):
            i += 1
            gen_arr.append(num)
            num = random.randint(lower_bound, upper_bound)
            if i >= max_count:
                break
        gen_turn = False
    global finished_generating
    with open('all.txt', 'a') as f:
        for number in gen_arr:
            f.write(f"{number}\n")
        gen_arr = []
    finished_generating = True
    return


# Function for the thread that removes odd numbers from the stack
def odd_thread(stack):
    global finished_generating, odd_turn, gen_turn, odd_arr
    filename = "odd.txt"
    f = open(filename, 'w')
    f.close()
    while True:
        while (not odd_turn) or (gen_turn):
            if len(odd_arr) > 0:
                with open(filename, 'a') as f:
                    n = odd_arr.pop()
                    f.write(f"{n}\n")
            elif finished_generating and len(stack.stack) == 0:
                return
            pass
        num = stack.getTop()
        while (num != "empty") and (num % 2 != 0):
            num = stack.pop()
            odd_arr.append(num)
            num = stack.getTop()
        if num == "empty":
            gen_turn = True
        else:
            odd_turn = False
        if finished_generating and len(stack.stack) == 0:
            if len(odd_arr) > 0:
                with open(filename, 'a') as f:
                    for n in odd_arr:
                        f.write(f"{n}\n")
                    odd_arr = []
                    odd_turn = False
                    return

# Function for the thread that removes even numbers from the stack
def even_thread(stack):
    global finished_generating, odd_turn, gen_turn, even_arr, odd_arr, gen_arr
    filename = 'even.txt'
    f = open(filename, 'w')
    f.close()
    while True:
        while odd_turn or gen_turn:
            if len(even_arr) > 0:
                with open(filename, 'a') as f:
                    n = even_arr.pop()
                    f.write(f"{n}\n")
            elif finished_generating and len(stack.stack) == 0:
                return
            pass
        num = stack.getTop()
        while (num != "empty") and (num % 2 == 0):
            num = stack.pop()
            even_arr.append(num)
            num = stack.getTop()
        if num == "empty":
            gen_turn = True
        else:
            odd_turn = True

        if finished_generating and len(stack.stack) == 0:
            if len(even_arr) > 0:
                with open(filename, 'a') as f:
                    for n in even_arr:
                        f.write(f"{n}\n")
                even_arr = []
                odd_turn = True
                return


stack = Stack()
gen_turn = True
odd_turn = True
gen_arr = []
odd_arr = []
even_arr = []
finished_generating = False

gen_thread = threading.Thread(target=number_generator, args=(stack,))
odd_thread = threading.Thread(target=odd_thread, args=(stack,))
even_thread = threading.Thread(target=even_thread, args=(stack,))

gen_thread.start()
odd_thread.start()
even_thread.start()

gen_thread.join()
odd_thread.join()
even_thread.join()
