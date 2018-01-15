#!/usr/bin/env python

class Generic():

    power = 0

    def __init__(self, name):
        self.name = name

    def pow(self, number):
        return number**self.power

class Special1(Generic):
    power = 1

class Special2(Generic):
    power = 2    


print("Hello, classy world")
hi = Special1("hi")
print(hi.pow(3))

