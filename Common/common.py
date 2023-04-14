ulFIBONACCI = "ulFibonacci"
dlFIBONACCI = "dlFibonacci"
usFIBONACCI = "usFibonacci"
dsFIBONACCI = "dsFibonacci"
dDISTANCE = 'dDistance'
DISTANCE = 'Distance'

uaFIBONACCI = "uaFibonacci"
daFIBONACCI = "daFibonacci"
NORMAL = "Normal"

MCN = "M+ N"
MCNT = "M+ N-"
MNT = "M N-"

probability_list = [MCN, MCNT, MNT]


def distance(n):
    return [i for i in range(n)]


def normal(n):
    return [1 for i in range(n)]


def math_fibonacci(n):
    fib = [0, 1, 2]
    for i in range(3, n):
        fib.append(fib[i - 1] + fib[i - 2])
    return fib


def string_to_float_list(string_list):
    int_list = []
    for string_value in string_list:
        try:
            int_value = float(string_value)
        except (ValueError, TypeError):
            int_value = 0
        int_list.append(int_value)
    return int_list
