#!/usr/bin/env python

from __future__ import division, print_function
import itertools
import sys


def f(k, b):
    """
    INPUT: integer between 0 and n
    Canonical translation from k -> (r,s)
    Finds (r, s) such that s < self.a and r * self.b + s = k
    """
    return k // b, k % b


def finv(r, s, b):
    """
    INPUT: r,s as above
    OUTPUT: k as above
    Canonical translation (r,s) -> k
    """
    return r * b + s


def combine_pairings(pa, pb, b):
    """
    INPUT:  Two lists of tuples representing pairings on sub problems
            of size a and b
    OUTPUT: One list of tuples representing a pairing on a problem
            of size n = a * b
    """
    result = []
    itr = itertools.product(pa, pb)
    for pair1, pair2 in itr:
        comb = (finv(pair1[0], pair2[0], b), finv(pair1[1], pair2[1], b))
        result.append(comb)

    return result


def get_pairing_power_of_2(s, b):
    """
    INPUT: s - day number between 0 and b-1, b number of
    OUTPUT: List of tuples representing the days partnerships

    This function creates a pairing on day s for b students.
    """
    if bin(b).count("1") != 1:
        raise ValueError('b = {0}; it must be a power of 2.'.format(b))

    result = []
    for i in range(b):
        result.append((i, i ^ s))
    return result


def get_pairing_double_odd(r, a):
    if a % 2 == 1 or a % 4 == 0:
        raise ValueError("a = 0; in must be 2 times an odd number.".format(a))
    if r < 0 or r >= a:
        raise ValueError("r = {0}; it must be between 0 and {1}".format(r, a))

    # There are a-1 pairings.  For each r from 1 to a-1 we should get a
    # different pairing.
    # For each odd q such that 1 <= q < a, q != a/2, we get a pairing
    # by pairing every even i with i + q % a
    # This is a/2-1 pairings.  These will be numbered 1 to a/2-1.
    # For each q from 0 to a/2-1 we get a pairing by matching q
    # with q + a/2 and q-i with q+i for i in range(1, a/2-1)
    # This is a/2 pairings.  These will be numbered a/2 to a - 1
    # pairing number 0 is the identity (non)pairing.

    result = []
    if r == 0:
        for i in range(a):
            result.append((i, i))
        return result
    elif r < a//2:
        q = 2 * r - 1
        # skip the case where q = a/2
        if q >= a//2:
            q += 2
        for i in range(0, a-1, 2):
            result.append((i, (i+q) % a))
        return result
    else:
        assert(r < a)
        q = r - a//2
        result.append((q, (q+a//2) % a))
        for i in range(1, a//2):
            result.append(((q - i + a) % a, (q + i) % a))
        return result


def prettify(pairing):
    s = set()
    for pair in pairing:
        if pair[0] < pair[1]:
            s.add(pair)
        else:
            s.add((pair[1], pair[0]))
    return sorted(list(s))


class Pairer(object):

    def __init__(self, n):
        """
        INPUT: n, an even natural number
        Constructs a Pairer object for a given even number of students, n.
        """
        self.n = n

        if n % 2 == 1 or n <= 0:
            raise ValueError("N={0}; it must be positive and even.".format(n))
        a = n
        b = 1
        while a % 4 == 0:
            a //= 2
            b *= 2
        # a is an even number not divisible by 4
        self.a = a
        # b is a power of 2
        self.b = b

    def get_pairing(self, day):
        r, s = f(day, self.b)
        p1 = get_pairing_power_of_2(s, self.b)
        p2 = get_pairing_double_odd(r, self.a)
        return combine_pairings(p1, p2, self.a)


def usage():
    print("Usage:   python pairer.py <cohortfile> <day>")
    print("Example: python pairer.py cohort4 1")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        usage()
        sys.exit()
    try:
        with open(sys.argv[1]) as studentfile:
            student = [line.strip() for line in studentfile.readlines()]
    except:
        usage()
        sys.exit()

    try:
        p = Pairer(len(student))
    except ValueError:
        print("The number of students must be even. Add a dummy student")
        print("(e.g., 'Your choice') at the end of the input file to allow")
        print("one student work alone or join any group")
        print("they wish.")
        sys.exit()
    try:
        day = int(sys.argv[2])
    except:
        print("<day> must be an integer between 1 and {0}"
              .format(len(student)-1))
        usage()
        sys.exit()

    pairing = prettify(p.get_pairing(day))
    print("Recommended partnerships - Seed {0} of {1}:"
          .format(day, len(student)-1))
    for tup in pairing:
        print(", ".join([student[a] for a in tup]))
