import unittest


# merging sorted lists
def merge_lists(alist, blist):
    if len(alist) == 0:
        return blist
    if len(blist) == 0:
        return alist
    if alist[0] < blist[0]:
        return [alist[0]] + merge_lists(alist[1:], blist)
    else:
        return [blist[0]] + merge_lists(alist, blist[1:])


# several functions for Fibonacci numbers, including memoized version
def compute_nth_fib(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return compute_nth_fib(n-1) + compute_nth_fib(n-2)


class Memoizer(object):
    """A generic class for memoization.

    Memoizer implements two methods, __init__ and __call__.
    __init__ sets the function being memoized and initiates the memory dict.

    __call__ makes sure the decorated function is only called if we don't
    have the value computed already from a previous call.

    """
    def __init__(self, f):
        self.func = f
        self.memory = {}

    def __call__(self, *args):
        if args not in self.memory:
            self.memory[args] = self.func(*args)
        return self.memory[args]


def memoize_with_closure(f):
    """A functional memoization technique.

    The result is achieved through a memoization_closure, which closes over a
    'memory' dict, and operates in an intuitive way, making sure the function is
    only called if the same call's results are not yet in the memory.

    :param f: function being decorated and memoized
    """
    memory = {}

    def memoization_closure(*args):
        if args not in memory:
            memory[args] = f(*args)
        return memory[args]
    return memoization_closure


@memoize_with_closure
def compute_nth_fib_memo(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return compute_nth_fib_memo(n - 1) + compute_nth_fib_memo(n - 2)


def gather_first_n_fibonacci(n):
    result = []
    for i in range(0, n):
        result.append(compute_nth_fib_memo(i))
    return result


def all_fib_below_n(n):
    result = []
    count = next_fib = 0

    while next_fib < n:
        result.append(next_fib)
        count += 1
        next_fib = compute_nth_fib_memo(count)
    return result


# stock prices problem
def maximize_profit(stocks):
    best_buy_day = candidate_buy_day = 0
    best_sell_day = 0
    best_profit = 0
    for (day, price) in enumerate(stocks):
        # consider selling on this day
        candidate_profit = price - stocks[candidate_buy_day]
        if candidate_profit > best_profit:
            # regardless of when we bought, selling today is better
            best_sell_day = day
            # ... commit to the buying day, too, since this is a best deal
            best_buy_day = candidate_buy_day
            best_profit = candidate_profit
        # consider buying on this day -- but no commitment yet
        if stocks[candidate_buy_day] > price:
            candidate_buy_day = day
    return best_buy_day, best_sell_day, best_profit


def is_palindrome(a_string):
    length = len(a_string)
    middle = length//2

    if not middle:
        return True

    left_idx = middle - 1
    right_idx = middle + 1 if length % 2 else middle

    while left_idx >= 0:
        if a_string[left_idx] != a_string[right_idx]:
            return False
        left_idx -= 1
        right_idx += 1
    return True


@memoize_with_closure
def all_string_permutations(a_string):
    if a_string == "":
        return[""]

    result = []
    for idx, a_char in enumerate(a_string):
        remaining_string = a_string[0:idx] + a_string[idx+1:]
        rec_result = all_string_permutations(remaining_string)
        for new_string in rec_result:
            new_string_with_char = a_char + new_string
            if not result.count(new_string_with_char):
                result.append(new_string_with_char)
    return result


def sum_of_two(a_list, target):
    a_set = {x for x in a_list}
    for x in a_list:
        if target-x in a_set:
            return x, target-x
    return ()


def sum_of_three(a_list, target):
    for x in a_list:
        twos = sum_of_two(a_list, target-x)
        if (len(twos) != 0):
            return (x,) + twos
    return ()


class InterviewProblemsTest(unittest.TestCase):

    # tests for merge_lists
    def test_first_list_empty(self):
        alist = []
        blist = [1,2,3]
        assert merge_lists(alist, blist) == blist

    def test_second_list_empty(self):
        alist = [1, 2, 3]
        blist = []
        assert merge_lists(alist, blist) == alist

    def test_both_lists_empty(self):
        alist = []
        blist = []
        assert merge_lists(alist, blist) == []

    def test_merge_start_first(self):
        alist = [1,3,5]
        blist = [2,4,6]
        assert merge_lists(alist, blist) == [1,2,3,4,5,6]

    def test_merge_start_second(self):
        alist = [3, 5]
        blist = [2, 4, 6]
        assert merge_lists(alist, blist) == [2, 3, 4, 5, 6]

    # tests for Fibonacci
    def test_compute_nth_fib(self):
        assert compute_nth_fib(0) == 0
        assert compute_nth_fib(1) == 1
        assert compute_nth_fib(2) == 1
        assert compute_nth_fib(3) == 2
        assert compute_nth_fib(4) == 3
        assert compute_nth_fib(5) == 5
        assert compute_nth_fib(6) == 8
        #import time
        #start_time = time.time()
        #fib40 = compute_nth_fib(40)
        #end_time = time.time()
        #print("40th fib is %d and took %d to compute" % (fib40, end_time - start_time,))
        assert compute_nth_fib_memo(100) == 354224848179261915075

    def test_gather_first_n_fib(self):
        assert gather_first_n_fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_all_fib_below_n(self):
        assert all_fib_below_n(100) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

    # testing maximize_profit
    def test_increasing(self):
        expected = (0, 5, 5)
        assert expected == maximize_profit([1, 2, 3, 4, 5, 6])

    def test_decreasing(self):
        expected = (0, 0, 0)
        assert expected == maximize_profit([10, 9, 8, 7, 6, 5])

    def test_one_peak(self):
        expected = (0, 3, 4)
        assert expected == maximize_profit([6, 7, 8, 10, 9, 8, 7])

    def test_new_buy_wins(self):
        expected = (4, 7, 5)
        assert expected == maximize_profit([6, 7, 8, 10, 1, 2, 3, 6])

    def test_new_buy_fails(self):
        expected = (0, 3, 4)
        assert expected == maximize_profit([6, 7, 8, 10, 1, 2, 3, 4])

    def test_palindrome_empty(self):
        assert is_palindrome("")

    def test_palindrome_single(self):
        assert is_palindrome("q")

    def test_palindrome_even(self):
        assert is_palindrome("qwwq")

    def test_palindrome_odd(self):
        assert is_palindrome("qwewq")

    def test_palindrome_false(self):
        assert not is_palindrome("qwerewa")

    def test_all_permutations_empty(self):
        assert all_string_permutations("") == [""]

    def test_all_permutations_single(self):
        assert all_string_permutations("a") == ["a"]

    def test_all_permutations_two(self):
        result = all_string_permutations("ab")
        assert result == ["ab", "ba"]

    def test_all_permutations_single(self):
        result = all_string_permutations("abc")
        assert result == ["abc", "acb", "bac", "bca", "cab", "cba"]

    def test_all_permutations_duplicates(self):
        result = all_string_permutations('abba')
        result.sort()
        expected = ["aabb", "abab", "abba", "baab", "baba", "bbaa"]

        assert result == expected

    def test_sum_of_two_found(self):
        expected = (3, -3)
        result = sum_of_two([1, 2, 3, 4, -3, -5, -10], 0)
        assert result == expected

    def test_sum_of_two_found_nonzero(self):
        expected = (2, 10)
        result = sum_of_two([1, 2, 3, 10], 12)
        assert result == expected

    def test_sum_of_two_found_negative(self):
        expected = (3, -7)
        result = sum_of_two([1, 2, 3, 10, -2, -7], -4)
        assert result == expected

    def test_sum_of_two_not_found(self):
        expected = ()
        result = sum_of_two([1, 2, 3, 4, -5, -10], 0)
        assert result == expected

    def test_sum_of_three_found(self):
        expected = (1, 2, -3)
        result = sum_of_three([1, 2, 3, 4, -1, -3], 0)
        print("result =")
        print(result)
        print("expected =")
        print(expected)

        assert result == expected

    def test_sum_of_three_nonzero(self):
        expected = (1, 4, -20)
        result = sum_of_three([1, 2, 3, 4, -1, -3, -20], -15)

        assert result == expected


if __name__ == '__main__':
    unittest.main()



