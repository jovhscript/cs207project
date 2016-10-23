# Lazy.py

class LazyOperation:
    
    def __init__(self, function, args_init, kwargs_init):
        self._function = function
        self._args = args_init
        self._kwargs = kwargs_init
        
    def eval(self):
        kwargs_final = []
        args_final = []
        
        for k,v in self._kwargs.items():
            if v.__class__.__name__ == "LazyOperation":
                args_final.append((k,v.eval()))
            else:
                args_final.append((k,v))
            
        for i in self._args:
            if i.__class__.__name__ == "LazyOperation":
                args_final.append(i.eval())
            else:
                args_final.append(i)
                
        return self._function(*tuple(args_final),**dict(kwargs_final))

def lazy(function):
    def decorator(*args, **kwargs):
        return LazyOperation(function, args_init = args, kwargs_init = kwargs)
    return decorator

def multiply(a, b):
    return a * b

def add(a, b):
    return a + b
    
lazy_add = lazy(add)
lazy_mul = lazy(multiply)

print(isinstance( lazy_add(1,2), LazyOperation ) == True )