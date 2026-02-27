
import Functions







#------------------------------------------------------------------------------------------------
def converter():
    print("Feet and Meters Converter")
    print()
    done = False
    while done != True:
        print("Conversion Menu:")
        print("a.     Feet to Meters")
        print("b.     Meters to Feet")
        choice = input("Select a conversion (a/b: ")
        if choice == 'a':
            feet = int(input("Enter Feet: "))
            meter = Functions.To_Meter(feet)
            print(meter, "meters")
        elif choice == 'b':
            meter = int(input("Enter Meters: "))
            feet = Functions.To_Feet(meter)
            print(feet, "feet")
        else:
            print("Invalid Input")

        print()
        again = input("Would you like to do another converstion? (y/n):")
        if again == 'n':
            done = True

#------------------------------------------------------------------------------------------------

def Tax_Calculator():

    print("Sales Tax Calculator")
    print()
    done = False
    while done != True:

        print("ENTER ITEMS (ENTER 0 TO END)")
        item = -1
        total = 0
        while item != 0:
            item = float(input("Cost of item: "))
            total += item

        Taxed_Total, Tax_amount = Functions.Add_Tax(total, Functions.Sales_Tax)
        print(f"Total:  {total}$")
        print(f"Sales tax: {Tax_amount}$")
        print(f"Total after tax:  {Taxed_Total}$")
        print()
        again = input("Again? (y/n): ")
        if again == 'n':
            done = True


#------------------------------------------------------------------------------------------------

def Prime_Number_Checker():
    print("Prime Number Checker")
    print()
    done = False
    while done != True:
        number = -1
        while number < 1 or number > 5000:
            number = int(input("Please enter an integer between 1 and 5000: "))
            if number >= 1 or number >= 5000:
                break
            print("Invalid integer. Please try again")
        primes = Functions.Prime_Check(number)
        if primes == 0:
            print(number, "is a prime number")
        else:
            print(number, "is NOT a prime number")
            print(f"It has {primes} factors.")

        print()
        again = input("Try again? (y/n): ")
        if again == 'n':
            done = True



def main():
    for i in range(10):
        Functions.Even_Or_Odd(i)

    converter()
    Tax_Calculator()
    Prime_Number_Checker()

if __name__ == "__main__":
    main()