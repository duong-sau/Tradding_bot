from Common.common import math_fibonacci, uFIBONACCI, dFIBONACCI, DISTANCE, distance

probability_list_n = [uFIBONACCI, dFIBONACCI, DISTANCE]


def make_distance(min_val, max_val, counter):
    distance_list = distance(counter)
    result = n_u_distribution(distance_list, min_val, max_val)
    return result


def make_n_u_fibonacci(min_val, max_val, counter):
    fibonacci_list = n_fibonacci(counter)
    result = n_u_distribution(fibonacci_list, min_val, max_val)
    return result


def make_n_d_fibonacci(min_val, max_val, counter):
    fibonacci_list = n_fibonacci(counter)
    fibonacci_list.reverse()
    result = n_d_distribution(fibonacci_list, min_val, max_val)
    return result


def n_u_distribution(list_p, min_val, max_val):
    if len(list_p) == 0:
        return []
    best = max(list_p)

    round_values = []
    for i in range(len(list_p)):
        value = min_val + (max_val - min_val) * list_p[i] / best
        round_values.append(value)
    return round_values


def n_d_distribution(list_p, min_val, max_val):
    if len(list_p) == 0:
        return []
    best = max(list_p)

    round_values = []
    for i in range(len(list_p)):
        value = max_val - (max_val - min_val) * list_p[i] / best
        round_values.append(value)
    return round_values


def n_fibonacci(n):
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
    uFIBONACCI: make_n_u_fibonacci,
    dFIBONACCI: make_n_d_fibonacci,
    DISTANCE: make_distance
}
