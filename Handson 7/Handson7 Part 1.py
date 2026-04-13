
print("Tip Calculator")
while True:
    try:
        cost = float(input("Cost of meal: "))
    except ValueError:
        print("Must be a valid decimal number. Please try again")
    else:
        if cost <= 0:
            print("Must be greater than 0. Please try again")
        else:
            break
while True:
    try:
        tip = int(input("Tip Percent: "))
    except ValueError:
        print("Must be a valid integer. Please try again")
    else:
        if cost <= 0:
            print("Must be greater than 0. Please try again")
        else:
            break

tip_amount = cost * (tip/100)
total = round(tip_amount + cost, 2)
tip_amount = round(tip_amount, 2)
cost = round(cost, 2)
print("\nOUTPUT")
print("Cost of meal:".ljust(15), cost,"$")
print(f"{"Tip Percent:".ljust(15)} {tip}%")
print("Tip Amount:".ljust(15), tip_amount,"$")
print("Total amount:".ljust(15), total,"$")