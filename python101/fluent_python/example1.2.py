#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 22:15:32 2020

@author: xlew
"""

from math  import hypot

class Vector:
    
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return 'Vector({!r}, {!r})'.format(self.x, self.y)
    
    def __abs__(self):
        return hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))
    
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return Vector(x ,y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

v1 = Vector(2,4)
v2 = Vector(2,1)
print(v1 + v2)

v = Vector(3,4)
print(abs(v))

print(v * 3)

print(abs(v * 3))

'''
If we did not implement __repr__ , 
vector instances would be shown in the console like 
<Vector object at 0x10e100070> .
'''