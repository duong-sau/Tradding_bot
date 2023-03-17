uFIBONACCI = "+Fibonacci"
dFIBONACCI = "-Fibonacci"
NORMAL = "Normal"
DISTANCE = 'Distance'

probability_list_m = [uFIBONACCI, dFIBONACCI, NORMAL]
probability_list_n = [uFIBONACCI, dFIBONACCI, DISTANCE]


def make_distance(min_val, max_val, counter):
    distance_list = distance(counter)
    result = distribution(distance_list, min_val, max_val)
    return result


def make_normal(min_val, max_val, counter):
    normal_list = normal(counter)
    result = distribution(normal_list, min_val, max_val)
    return result


def make_u_fibonacci(min_val, max_val, counter):
    fibonacci_list = fibonacci(counter)
    fibonacci_list.reverse()
    result = distribution(fibonacci_list, min_val, max_val)
    return result


def make_d_fibonacci(min_val, max_val, counter):
    fibonacci_list = fibonacci(counter)
    result = distribution(fibonacci_list, min_val, max_val)
    return result


def distribution(list_p, min_val, max_val):
    sum_product = max_val - min_val
    total = sum(list_p)
    divided_values = [sum_product * x / total for x in list_p]

    real_values = [x + min_val for x in divided_values]
    round_values = [round(x, 4) for x in real_values]
    return round_values


def distance(n):
    return [i for i in range(n)]


def normal(n):
    return [1 for i in range(n)]


def fibonacci(n):
    if n == 1:
        return [1]
    else:
        return math_fibonacci(n + 2)[2:]


def math_fibonacci(n):
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib


math_dict = {
    uFIBONACCI: make_u_fibonacci,
    dFIBONACCI: make_d_fibonacci,
    NORMAL: make_normal,
    DISTANCE: make_distance
}


def string_to_float_list(string_list):
    int_list = []
    for string_value in string_list:
        try:
            int_value = float(string_value)
        except (ValueError, TypeError):
            int_value = 0
        int_list.append(int_value)
    return int_list


def auto_complete(function_type, pre_list, min_value, max_value, counter):
    if not pre_list:
        return math_dict[function_type](min_value, max_value, counter)
    if len(pre_list) >= counter:
        return pre_list[0:counter]
    return pre_list + math_dict[function_type](pre_list[-1], max_value, counter - len(pre_list))
