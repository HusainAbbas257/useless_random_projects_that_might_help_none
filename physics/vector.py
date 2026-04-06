import math

class Vector:
    def __init__(self,x=0,y=0):
        self.x=x
        self.y=y
    def scaler(self):
        return (self.x**2+self.y**2)**0.5
    def dot(self,other):
        return self.x*other.x+self.y*other.y
    def angle(self,other):
        return math.acos(self.dot(other)/(self.scaler()*other.scaler()))
    def __add__(self,other):
        return Vector(self.x+other.x,self.y+other.y)
    def __sub__(self,other):
        return Vector(self.x-other.x,self.y-other.y)
    def __mul__(self,scalar: float):
        # vector multiplication by scalar
        return Vector(self.x*scalar,self.y*scalar)
    def __truediv__(self,scalar: float):
        # vector division by scalar
        return Vector(self.x/scalar,self.y/scalar)
    def tangent(self):
        return Vector(-self.y,self.x)
    def unit(self):
        # returs unit vector
        scaler=self.scaler()
        if scaler==0:
            return Vector(0,0)
        return Vector(self.x/scaler,self.y/scaler)
    def roundoff(self,n=2):
        
        self.x=round(self.x,n)
        self.y=round(self.y,n)
    
class position(Vector):
    def __init__(self,x=0,y=0):
        super().__init__(x,y)
class velocity(Vector):
    def __init__(self,x=0,y=0):
        super().__init__(x,y)
class acceleration(Vector):
    def __init__(self,x=0,y=0):
        super().__init__(x,y)
        

    