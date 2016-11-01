# Lazy.py

class LazyOperation:
    '''
    A class for lazy-computed Time Series.
    
    Attributes
    ----------
    function : function
        LazyOperation performs this function
    args: float, int
        function args
    kwargs: float, int
        function kwargs
    '''
    
    def __init__(self, function, args_init, kwargs_init):
        '''
        Initialization
        
        Params
        ------
        function : function
            LazyOperation performs this function
        
        Examples
        --------
        >>> @lazy
            def lazy_add(a, b):
                return a + b
        >>> isinstance(lazy_add(1,2), LazyOperation)
        True
        '''
        self._function = function
        self._args = args_init
        self._kwargs = kwargs_init
        
    # need an equivalence method
    def __eq__(self,other):
        return_value = (self._kwargs == other._kwargs) and (self._args == other._args)
        return_value = return_value and (id(other._function) == id(self._function))
        return return_value
    
    # test out
        
    def eval(self):
        '''
        Returns the evaluated value of a given instance of LazyOperation.
        
        Examples
        --------
        >>> @lazy
            def lazy_add(a, b):
                return a + b
        >>> lazy_add(1,3).eval()
        4
        '''
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