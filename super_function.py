"""
In Python, super() has two major use cases:
    Allows us to avoid using the base class name explicitly
    Working with Multiple Inheritance
"""


class Mammal(object):
    def __init__(self, mammalName):
        print(mammalName, 'is a warm-blooded animal.')


class Dog(Mammal):
    def __init__(self):
        print('Dog has four legs.')
        super().__init__('Dog')


d1 = Dog()