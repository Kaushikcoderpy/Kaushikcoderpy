import math
import statistics as st
from statistics import StatisticsError

# Addition
def add(*args):
    total = 0
    for arg in args:
        total += arg
    return total

# Subtraction
def subtract(*args):
    if not args:
        return 0
    total = args[0]
    for arg in args[1:]:
        total -= arg
    return total

# Multiplication
def multiply(*args):
    if not args:
        return 0
    total = 1
    for arg in args:
        total *= arg
    return total

# Division
def divide(*args):
    if not args:
        return 0
    total = args[0]
    for arg in args[1:]:
        if arg == 0:
            print("Error: Division by zero is not possible")
            return None
        total /= arg
    return total

# Power
def power(*args):
    if not args:
        return 0
    total = args[0]
    for arg in args[1:]:
        total **= arg
    return total

# Factorial
def factorial(*args):
    if len(args) != 1:
        print("Error: Factorial requires exactly one number")
        return None
    arg = args[0]
    if arg < 0 or not arg.is_integer():
        print("Error: Factorial is only defined for non-negative integers")
        return None
    try:
        return math.factorial(int(arg))
    except OverflowError:
        print("Error: Number too large for factorial")
        return None

# Square root
def sqrt(*args):
    if len(args) != 1:
        print("Error: Square root requires exactly one number")
        return None
    if args[0] < 0:
        print("Error: Cannot calculate square root of a negative number")
        return None
    return math.sqrt(args[0])

# Logarithm
def logarithm(*args):
    if len(args) != 1 and len(args) != 2:
        print("Error: Logarithm requires one number (and optionally a base)")
        return None
    if args[0] <= 0:
        print("Error: Logarithm is only defined for positive numbers")
        return None
    base = args[1] if len(args) == 2 else math.e
    return math.log(args[0], base)

# Sum of n natural numbers
def sum_of_n_numbers():
    n = input("Enter how many numbers you want to calculate: ")
    try:
        n = int(n)
    except ValueError:
        print("Error: Please enter a valid integer.")
        return None
    if n < 0:
        print("n must be positive.")
        return None
    elif n == 0:
        print("The sum is 0.")
        return None
    else:
        result = n * (n + 1) // 2
        return result, n

# Arithmetic Mean
def arithmetic_mean(*args):
    finish = 0
    for arg in args:
        finish += arg
    return finish / len(args)

# Geometric Mean
def geometric_mean(*args):
    finish = 1
    for arg in args:
        finish *= arg
    return finish ** (1 / len(args))

# Median
def median_answer(*args):
    sorted_args = sorted(args)
    length = len(sorted_args)
    if len(sorted_args) % 2 != 0 : 
        return args[(length - 1) // 2]
    elif len(sorted_args) % 2 == 0 : 
        answer = sorted_args[(length // 2) - 1] + sorted_args[length // 2 ] 
        return answer / 2
    else : 
        print("an error occurred")

# Mode
def mode_answer(*args):
    try:
        mode_value = st.mode(args)
        return mode_value
    except StatisticsError:
        print("No unique mode found")
        return None
def percentage_calculator(*args) :
    if len(args) != 2 : 
        print("percentage calculation needs  only 2 arguments (number, percentage)")
        return None 
    return (args[0] * args[1]) / 100
#LCM   
def LCM(*args):
    args = [int(arg) for arg in args]
    result = args[0]
    if not args:
        return None 
    args = [int(arg) for arg in args]
    for num in args[1 :] : 
        result = (result  * num) // math.gcd(result, num)
    if not args:
        return None 
    return result 
# Main loop to handle operations
while True:
    operator = input("Enter the operator  (+, -, *, /, **, !, √, log, sum of n numbers,LCM, AM (arithmetic mean), GM (geometric mean), median, mode, %(percentage),'exit' (to quit) or help : " )
    if operator.lower() == "help":
        OPERATOR = {
        "+": "Addition",
        "-": "Subtraction",
        "*": "Multiplication",
        "/": "Division",
        "**": "Power",
        "!": "Factorial",
        "LCM" : "Least common multiple ", 
        "√": "Square root",
        "log": "Logarithm",
        "sum of n numbers": "Sum of first N natural numbers",
        "AM": "Arithmetic mean",
        "GM": "Geometric mean",
        "median": "Median",
        "mode": "Mode",
        "%": "Percentage calculation",
        "exit": "Exit the calculator"
    }
        for key, value in OPERATOR.items():
            print(f"{key} : {value}")
            continue
        again = input("do you want to continue (Y/N) : ")
        if again.upper() != "Y" :
            break
        elif again.upper() == "Y" : 
            operator = input("Enter the operator  (+, -, *, /, **, !, √, log, sum of n numbers,LCM,  AM, (arithmetic mean), GM (geometric mean), median, mode, %(percentage),'exit' (to quit) or help : " )
            
        else : 
            print("invalid input!")
    if operator.lower() == "exit":
        print("Exiting... Thanks for using!")
        break
    if operator == "LCM" : 
        print("LCM can be calculated to only integers!")

    if operator != "sum of n numbers":
        numbers = input("Enter the numbers separated by a space: ")
        try:
            args = list(map(float, numbers.split()))
        except ValueError:
            print("Error: Please enter valid numeric values.")
            continue
    else:
        args = []
    result = None
    if operator == "+":
        result = add(*args)
    elif operator == "-":
        result = subtract(*args)
    elif operator == "*":
        result = multiply(*args)
    elif operator == "/":
        result = divide(*args)
    elif operator == "**":
        result = power(*args)
    elif operator == "√":
        result = sqrt(*args)
    elif operator == "!":
        result = factorial(*args)
    elif operator == "log":
        result = logarithm(*args)
    elif operator == "sum of n numbers":
        result = sum_of_n_numbers()
    elif operator.upper() == "AM":
        result = arithmetic_mean(*args)
    elif operator.upper() == "GM":
        result = geometric_mean(*args)
    elif operator.lower() == "median":
        result = median_answer(*args)
    elif operator.lower() == "mode":
        result = mode_answer(*args)
    elif operator == "%" : 
        result = percentage_calculator(*args) 
    elif operator == "LCM" : 
        result = LCM(*args)
    elif operator == "" : 
        print("you did not enter a operator ")
    else : 
        print("Error: Invalid operator")

    # Printing the result
    if result is not None:
        if operator == "sum of n numbers":
            print(f"The sum of the first {result[1]} natural numbers is: {result[0]}")
        else:
            print("Result:", result)
    else:
        print("No valid result due to an error.")
    calculate_again = input("want to use again? (Y/N) : ")
    if calculate_again == "Y" : 
        continue
    elif calculate_again != "Y" : 
        print("thanks for using 👍")
        break
    else : 
        print("invalid input ")
        break


