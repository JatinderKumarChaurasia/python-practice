__author__ = 'akarpov'


class SomeDecoratorClass(object):
    def __init__(self, f):
        print("in SomeDecoratorClass.__init__, about to call the decoratee as a proof of concept")
        f()  # just as a proof that function is indeed completed at this point
        self.f = f

    def __call__(self, *args, **kwargs):
        print("in SomeDecoratorClass.__call__, *args= %s, kwargs= %s; about to call the decoratee %s" % (args, kwargs, self.f))
        self.f()


@SomeDecoratorClass
def a_function():
    print("a_function called!")


@SomeDecoratorClass
def b_function():
    print("b_function called!")

print("a_function and b_function are now decorated by SomeDecoratorClass")

a_function()
b_function()


def decorator_function(f):  # also takes a function in
    def new_f():
        print("inside decorator_function, calling the decoratee:")
        f()
        print("there you go, wasn't so bad?")
    return new_f

@decorator_function
def c_function():
    print("ima c_function, I let no class decorate me!")

print("c_function is now decorated by %s and about to get called..." % decorator_function)

c_function()
