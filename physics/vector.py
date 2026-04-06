import math

class Vector:
    '''a simple 2D vector class with some basic operations'''
    
    def __init__(self,x=0,y=0):
        '''initializes the vector with x and y components'''
        self.x=x
        self.y=y
        
    def scaler(self):
        '''returns the magnitude of the vector'''
        return (self.x**2+self.y**2)**0.5
    
    def dot(self,other):
        '''returns the dot product of self and other'''
        return self.x*other.x+self.y*other.y
    
    def angle(self,other):
        '''returns the angle between self and other in radians'''
        return math.acos(self.dot(other)/(self.scaler()*other.scaler()))
    
    def __add__(self,other):
        '''returns the sum of self and other'''
        return Vector(self.x+other.x,self.y+other.y)
    
    def __sub__(self,other):
        '''returns the difference of self and other'''
        return Vector(self.x-other.x,self.y-other.y)
    
    def __mul__(self,scalar: float):
        '''returns the product of self and scalar'''
        return Vector(self.x*scalar,self.y*scalar)
    
    def __truediv__(self,scalar: float):
        '''returns the quotient of self and scalar'''
        return Vector(self.x/scalar,self.y/scalar)
    
    def tangent(self):
        '''returns the tangent vector of self'''
        return Vector(-self.y,self.x)
    
    def unit(self):
        '''returns the unit vector of self'''
        scaler=self.scaler()
        if scaler==0:
            return Vector(0,0)
        return Vector(self.x/scaler,self.y/scaler)
    
    def roundoff(self,n=2):
        '''rounds off the components of the vector to n decimal places and also sets very small values to 0 to avoid jitter'''
        self.x=round(self.x,n)
        if(abs(self.x)<0.05):
            self.x=0
        self.y=round(self.y,n)
        if(abs(self.y)<0.05):
            self.y=0
    
class position(Vector):
    '''a simple position class that inherits from vector'''
    
    def __init__(self,x=0,y=0):
        '''initializes the position with x and y components'''
        super().__init__(x,y)
        
class velocity(Vector):
    '''a simple velocity class that inherits from vector'''
    
    def __init__(self,x=0,y=0):
        '''initializes the velocity with x and y components'''
        super().__init__(x,y)
class acceleration(Vector):
    '''a simple acceleration class that inherits from vector'''
    
    def __init__(self,x=0,y=0):
        '''initializes the acceleration with x and y components'''
        super().__init__(x,y)
        

    