#Ricky said I need this

'''
This made both Priscilla and I chuckle

The reason you need this is so that you can import this code as a python package.
Some people even do imports and some basic initialization in this file.
You can also just create a python package that has nothing but an __init__ file
with the objects or functions that you intend to utilize from it
(I have an image uploader that is built in this exact way).

Anything you build that we want to run as a docker container will be imported as a python package,
so init is necessary there.  You can also add variables to this that would get in the way elsewhere....

See below:

'''
__version__ = '1.0.0'

__release_notes__ = '''
1.0.0: 
    This is my first version; Bitch!
'''