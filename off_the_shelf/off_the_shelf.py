from cPickle import PicklingError
from functools import wraps
import shelve
import datetime
from hashlib import sha1

__author__ = 'rogueleaderr'

shelf_fname = "my_shelf.shelf"


def off_the_shelf(verbose=False):
    def shelve_it(f):
        @wraps(f)
        def shelf_wrap(*args, **kwargs):
            shelf = shelve.open(shelf_fname)
            key = sha1(str(f.__module__) + str(f.__name__) + str(args) + str(kwargs)).hexdigest()
            try:
                if shelf.has_key(key):
                    if verbose: print "got from the shelf"
                    return shelf[key]
                else:
                    if verbose: print "put on the shelf"
                    res = f(*args, **kwargs)
                    try:
                        shelf[key] = res
                    except PicklingError:
                        if verbose: print "result cannot be pickled"
                    return res
            finally:
                shelf.close()
        return shelf_wrap
    return shelve_it


@off_the_shelf(verbose=True)
def test_function(arg):
    print "arbitrary argument: {}".format(arg)
    return datetime.datetime.now()


def main():
    print test_function(3)

if __name__ == "__main__":
    main()