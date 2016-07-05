__author__ = 'Mudit Srivastav'
'''
# Skip a test if dependent test fails
# Date : 6/6/2016
'''

def skipIfTrue(flag):
    def deco(f):
        def wrapper(self, *args, **kwargs):
            if getattr(self, flag):
                self.skipTest(f)
            else:
                f(self, *args, **kwargs)
        return wrapper

    return deco


