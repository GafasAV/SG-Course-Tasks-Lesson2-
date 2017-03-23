__author__ = 'Andrew Gafiychuk'


class AdditionalMethods(object):
    """
    This class contains three methods that addition
    the metaclass result class.

    - pretty_func() Static method, just print some text
    - do_things() Method that print private arr 'var'
    -print_all_attr() Print all class public attributes

    """
    @staticmethod
    def pretty_func():
        print('Some useful message')

    def do_things(self):
        print(self.var)

    def print_all_attr(self):
        """
        Method print all class public attributes
        (Takes all object params list
        filter all public attributes
        and print them)

        """
        args_list = []

        for arg in dir(self):
            if not arg.startswith('_') and not callable(getattr(self, arg)):
                args_list.append(arg)

        for arg in args_list:
            print(getattr(self, arg))


class PublicMeta(type):
    """
    Metaclass that builds new class by adding
    three additional methods to them and replacing
    all private attributes with public ones

    """
    def __new__(cls, name, bases, dict):

        new_bases = (AdditionalMethods,) + bases

        signature = "_" + name + "__"

        new_dict = {}

        for name, value in dict.items():
            if name.startswith(signature) and not callable(value):
                name = name.replace(signature, "")

            new_dict[name] = value

        return super(PublicMeta, cls).__new__(cls, name, new_bases, new_dict)


class A(metaclass=PublicMeta):

    __var = 10

    def __init__(self, x):
        self.x = x


class B(metaclass=PublicMeta):

    __x = 100
    __y = 200
    __z = 300

    def __init__(self, x):
        self.x = x


if __name__ == "__main__":
    # A sample print
    a = A(10)

    print(a.var)

    a.pretty_func()
    a.do_things()

    # B print ALL public attributes use print_all_attr()
    b = B(100)

    print(b.x)
    print(b.y)
    print(b.z)

    b.pretty_func()
    b.print_all_attr()