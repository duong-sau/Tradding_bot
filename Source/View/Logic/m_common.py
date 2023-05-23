from Source.View.Logic.common import math_fibonacci, NORMAL, normal, uaFIBONACCI, daFIBONACCI


def m_fibonacci(n):
    if n == 0 or n == 1:
        return [1]
    if n == 2:
        return [1, 2]
    else:
        return math_fibonacci(n + 1)[1:]


def make_normal(min_val, max_val, counter):
    normal_list = normal(counter)
    result = m_distribution(normal_list, min_val, max_val)
    return result


def make_m_u_fibonacci(min_val, max_val, counter):
    fibonacci_list = m_fibonacci(counter)
    result = m_distribution(fibonacci_list, min_val, max_val)
    return result


def make_m_d_fibonacci(min_val, max_val, counter):
    fibonacci_list = m_fibonacci(counter)
    fibonacci_list.reverse()
    result = m_distribution(fibonacci_list, min_val, max_val)
    return result


def m_distribution(list_p, min_val, max_val):
    sum_product = max_val - min_val
    total = sum(list_p)
    divided_values = [sum_product * x / total for x in list_p]

    real_values = [x + min_val for x in divided_values]
    return real_values


m_math_dict = {
    uaFIBONACCI: make_m_u_fibonacci,
    daFIBONACCI: make_m_d_fibonacci,
    NORMAL: make_normal,
}
