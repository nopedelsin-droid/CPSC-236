def Even_Or_Odd(int):
    if int%2 == 0:
        print(f"{int} is even")
    elif int%2 != 0:
        print(f"{int} is odd")
    else:
        print("ERROR")

def To_Meter(ft):
    m = ft * 0.3048
    m = round(m, 2)
    return m

def To_Feet(m):
    ft = m / 0.3048
    ft = round(ft, 2)
    return ft

Sales_Tax = 0.06
def Add_Tax(cost, tax_rate):
    tax = cost * tax_rate
    cost += tax
    cost = round(cost, 2)
    tax = round(tax, 2)
    return cost, tax


def Prime_Check(num):
    factors = []
    for i in range(num):
        if (i + 1) == 1 or (i + 1) == num:
            continue
        if (num % (i + 1)) == 0:
            factors.append(i)
    Number_Of_Factors = len(factors)
    return Number_Of_Factors
