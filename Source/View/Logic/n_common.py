from Source.View.Logic.common import math_fibonacci, ulFIBONACCI, dlFIBONACCI, DISTANCE, distance, usFIBONACCI, dsFIBONACCI, \
    dDISTANCE


def make_d_distance(min_val, max_val, counter):
    if counter == 1:
        return [min_val]
    distance_list = distance(counter)
    result = long_distribution(distance_list, min_val, max_val)
    return result


def make_distance(min_val, max_val, counter):
    if counter == 1:
        return [min_val]
    distance_list = distance(counter)
    result = short_distribution(distance_list, min_val, max_val)
    return result


def make_d_long_fibonacci(min_val, max_val, counter):
    fibonacci_list = u_fibonacci(counter)
    fibonacci_list.reverse()
    result = short_distribution(fibonacci_list, min_val, max_val)
    return result


def make_u_long_fibonacci(min_val, max_val, counter):
    fibonacci_list = u_fibonacci(counter)
    result = long_distribution(fibonacci_list, min_val, max_val)
    return result


def long_distribution(list_p, min_val, max_val):
    if len(list_p) == 0:
        return [0]
    if len(list_p) == 1:
        return [1]
    best = max(list_p)

    round_values = []
    for i in range(len(list_p)):
        value = max_val - (max_val - min_val) * list_p[i] / best
        round_values.append(value)
    return round_values


def make_d_short_fibonacci(min_val, max_val, counter):
    fibonacci_list = u_fibonacci(counter)
    fibonacci_list.reverse()
    result = long_distribution(fibonacci_list, min_val, max_val)
    return result


def make_u_short_fibonacci(min_val, max_val, counter):
    fibonacci_list = u_fibonacci(counter)
    result = short_distribution(fibonacci_list, min_val, max_val)
    return result


def short_distribution(list_p, min_val, max_val):
    if len(list_p) == 0:
        return [0]
    if len(list_p) == 1:
        return [1]
    best = max(list_p)

    round_values = []
    for i in range(len(list_p)):
        value = min_val + (max_val - min_val) * list_p[i] / best
        round_values.append(value)
    return round_values


def u_fibonacci(n):
    if n == 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]
    if n == 3:
        return [0, 1, 2]
    else:
        return math_fibonacci(n)


n_math_dict = {
    ulFIBONACCI: make_u_long_fibonacci,
    dlFIBONACCI: make_d_long_fibonacci,
    usFIBONACCI: make_u_short_fibonacci,
    dsFIBONACCI: make_d_short_fibonacci,
    dDISTANCE: make_d_distance,
    DISTANCE: make_distance
}
