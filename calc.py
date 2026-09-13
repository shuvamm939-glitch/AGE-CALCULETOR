import  math
import os
HISTORY_FILE = "calculator_history.txt"
history = []
memory = 0 #Real calculator's M button

#____________XD CALCULATOR____________________

def calculate(expression):
    """Safely evaluate a mathematical expression typed by the user."""
    allowed_names = {
        'sqrt': math.sqrt,
        'pow': math.pow,
        'pi': math.pi,
        'e': math.e,
        'sin': lambda x: math.sin(math.radians(x)),
        'cos': lambda x: math.cos(math.radians(x)),
        'tan': lambda x: math.tan(math.radians(x)),
        'log': math.log10,
        'ln': math.log,
        'abs': abs,
        'fact': math.factorial,
        'round': round,
    }

    expression = expression.replace('^', '**')

    try:
        result = eval(expression, {"_builtins_": {}}, allowed_names)
        return result
    except ZeroDivisionError:
        return "Error: Invalid expression"
    except (SyntaxError, NameError, TypeError, ValueError):
        return "Error: Invalid expression"


#----------------PERCENTAGE--------------------

def percentage_menu():
    print("\n1.X% of Y  2.X is X% of what% of Y  3.Increase by Y% 4.Decrease X by Y%")
    ch = input("Enter your choice (1-4): ")
    x = float(input("Enter X: "))
    y = float(input("Enter Y: "))

    if ch == '1':
        print(f"Result = {x * y / 100}")
    elif ch == '2':
        print(f"Result = {(x / y) * 100}%")
    elif ch == '3':
        print(f"Result = {x + (x * y / 100)}")
    elif ch == '4':
        print(f"Result = {x - (x * y / 100)}")