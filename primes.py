#!/usr/bin/env python3

from math import sqrt, ceil

import unittest

DEFAULT_NUM_OF_PRIMES = 10


def get_n_primes(n=DEFAULT_NUM_OF_PRIMES):
    def is_prime(num):
        if num == 1 or num == 2:
            return True
        for i in range(2, ceil(sqrt(num))+1):
            if num % i == 0:
                return False
        return True

    result = []
    candidate = 2
    while len(result) < n:
        if is_prime(candidate):
            result.append(candidate)
        candidate += 1
    return result


def print_multiplication_table(top, side):
    # how wide is the largest number in the table
    digits = len(str(top[-1] * side[-1]))
    # how wide should the side (left) column be?
    side_width = len(str(side[-1]))
    # build and print the table header
    head_str = " " * (side_width+1)
    for n in top:
        head_str += str(n).rjust(digits+1)
    print(head_str)
    print(" " * side_width + "_" * len(head_str))
    # now build and print every row
    for i in range(0, len(side)):  # i is the row index
        # takes care of the side 'prefix'
        row_string = ("%d" % (side[i],)).rjust(side_width) + "|"
        for j in range(0, len(top)):
            row_string += str(top[j]*side[i]).rjust(digits+1)
        print(row_string)


class InterviewProblemsTest(unittest.TestCase):

    def test_get_n_primes(self):
        assert([2, 3, 5, 7, 11, 13, 17, 19, 23, 29] == get_n_primes())

    # not really proper tests, other than making sure we handle the edge case and don't crush
    def test_print_table_single(self):
        col = row = get_n_primes(1)
        print_multiplication_table(row, col)

    def test_print_table(self):
        col = [1,2,3,4,5]
        row = [6,7,8]
        print_multiplication_table(row, col)


if __name__ == '__main__':
    unittest.main()
