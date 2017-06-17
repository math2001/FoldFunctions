# -*- encoding: utf-8 -*-

# repr is used instead of print in this example as this file is ran by sublime text, and
# we don't want to pollute the console on start up.

def hello_world(arg1, arg2):
    for i in range(10):
        if i % 2 == 0:
            repr(i)

    repr('-end')

repr('hello world')
repr('test')
def long_arg(argument_number_one, argument_number_two,
             argument_number_three):
    if True:
        if True or False:
            if False or True:
                repr('Hello')

    repr('world!')

