"""
XD CALCULATOR  
A normal + scientific calculator that runs in the terminal.

New in this version:
  * Safe expression evaluator (no eval() -> no security hole)
  * DEG / RAD mode for trigonometry
  * 'ans' (last answer) and 'm' (memory value) can be used inside expressions
  * Shortcuts: m+  m-  mc  mr   (like the M buttons on a real calculator)
  * More functions: asin, acos, atan, sinh, cosh, tanh, exp, log2, cbrt,
    floor, ceil, gcd, lcm, ncr, npr
  * Implicit multiplication:  2pi  ->  2*pi     3(4+5)  ->  3*(4+5)
  * Number base converter (binary / octal / hexadecimal)
  * Unit converter now works in BOTH directions and uses a table
    (37 if/elif blocks became one small function)
  * Better error messages and no crashes on wrong input
"""

import ast
import math
import operator
import os
import re
import statistics

HISTORY_FILE = "calculator_history.txt"
history = []          # list of strings like "5+3 = 8"
memory = 0            # Real calculator's M button
last_answer = 0       # the "ans" button
angle_mode = "DEG"    # "DEG" or "RAD"


#____________XD CALCULATOR____________________


class CalcError(Exception):
    """Our own error type. It carries a message we can show to the user."""


def ask_float(prompt):
    """Keep asking until the user types a valid number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("  Please enter a valid number.")


def ask_int(prompt, minimum=None):
    """Keep asking until the user types a whole number."""
    while True:
        try:
            value = int(input(prompt))
        except ValueError:
            print("  Please enter a whole number.")
            continue
        if minimum is not None and value < minimum:
            print(f"  The number must be at least {minimum}.")
            continue
        return value


def format_number(x):
    """Show 8.0 as 8 and 0.30000000000000004 as 0.3."""
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            return str(x)
        if x.is_integer() and abs(x) < 1e15:
            return str(int(x))
        return f"{x:.12g}"
    return str(x)


#-----------------SCIENTIFIC FUNCTIONS-----------------

def to_radians(x):
    return math.radians(x) if angle_mode == "DEG" else x


def from_radians(x):
    return math.degrees(x) if angle_mode == "DEG" else x


def clean(x):
    """Remove tiny rounding noise, e.g. sin(180) = 1.2e-16 -> 0."""
    return round(x, 12) + 0.0


def sin(x):
    return clean(math.sin(to_radians(x)))


def cos(x):
    return clean(math.cos(to_radians(x)))


def tan(x):
    if angle_mode == "DEG" and x % 180 == 90:
        raise ValueError("tan is undefined here")
    return clean(math.tan(to_radians(x)))


def asin(x):
    return clean(from_radians(math.asin(x)))


def acos(x):
    return clean(from_radians(math.acos(x)))


def atan(x):
    return clean(from_radians(math.atan(x)))


def factorial(x):
    if x < 0 or x != int(x) or x > 1000:
        raise ValueError("factorial needs a whole number from 0 to 1000")
    return math.factorial(int(x))


def cbrt(x):
    """Cube root that also works for negative numbers."""
    return math.copysign(abs(x) ** (1 / 3), x)


def ncr(n, r):
    return math.comb(int(n), int(r))


def npr(n, r):
    return math.perm(int(n), int(r))


def safe_power(a, b):
    """Stop things like 9**9**9 which would freeze the computer."""
    if abs(b) > 1000:
        raise OverflowError("exponent too large")
    return a ** b


FUNCTIONS = {
    "sqrt": math.sqrt, "cbrt": cbrt, "pow": safe_power,
    "sin": sin, "cos": cos, "tan": tan,
    "asin": asin, "acos": acos, "atan": atan,
    "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
    "log": math.log10, "log2": math.log2, "ln": math.log, "exp": math.exp,
    "abs": abs, "round": round, "floor": math.floor, "ceil": math.ceil,
    "fact": factorial, "ncr": ncr, "npr": npr,
    "gcd": math.gcd, "lcm": math.lcm,
}

OPERATORS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv, ast.Mod: operator.mod,
    ast.Pow: safe_power,
    ast.USub: operator.neg, ast.UAdd: operator.pos,
}


       #  SAFE EVALUATOR
       #  Python's eval() can run ANY code, so we read the expression as a
       #  tree (ast) and only allow numbers, + - * / etc. and our functions.

def evaluate(node, names):
    if isinstance(node, ast.Expression):
        return evaluate(node.body, names)

    if isinstance(node, ast.Constant):
        if type(node.value) in (int, float):
            return node.value
        raise CalcError("Invalid expression")

    if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = evaluate(node.left, names)
        right = evaluate(node.right, names)
        return OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        return OPERATORS[type(node.op)](evaluate(node.operand, names))

    if isinstance(node, ast.Name):
        if node.id in names:
            return names[node.id]
        raise CalcError(f"Unknown name: {node.id}")

    if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
            and node.func.id in FUNCTIONS and not node.keywords):
        args = [evaluate(arg, names) for arg in node.args]
        return FUNCTIONS[node.func.id](*args)

    raise CalcError("Invalid expression")


def prepare(expression):
    """Turn what the user typed into something Python can read."""
    expression = expression.lower()
    expression = expression.replace("^", "**").replace("×", "*").replace("÷", "/")
    # 2pi -> 2*pi , 3(4) -> 3*(4) , (2)(3) -> (2)*(3)
    expression = re.sub(r"(\d|\))\s*(?=[a-df-z(])", r"\1*", expression)
    expression = re.sub(r"(\))\s*(?=\d)", r"\1*", expression)
    return expression


def calculate(expression):
    """Calculate an expression typed by the user. Returns a number."""
    global last_answer
    names = {"pi": math.pi, "e": math.e, "ans": last_answer, "m": memory}

    try:
        tree = ast.parse(prepare(expression), mode="eval")
        result = evaluate(tree, names)
    except ZeroDivisionError:
        raise CalcError("Cannot divide by zero")
    except OverflowError:
        raise CalcError("Number is too big")
    except (ValueError, TypeError):
        raise CalcError("Math error (check the numbers you used)")
    except SyntaxError:
        raise CalcError("Invalid expression")
    except RecursionError:
        raise CalcError("Expression is too long")

    last_answer = result
    return result


#---------------------------PERCENTAGE----------------------------------

def percentage_menu():
    print("\n1. X% of Y")
    print("2. X is what % of Y")
    print("3. Increase X by Y%")
    print("4. Decrease X by Y%")
    print("5. Percentage change from X to Y")
    choice = input("Enter your choice (1-5): ").strip()

    if choice not in ("1", "2", "3", "4", "5"):
        print("Invalid choice")
        return

    x = ask_float("Enter X: ")
    y = ask_float("Enter Y: ")

    if choice == "1":
        print(f"Result = {format_number(x * y / 100)}")
    elif choice == "2":
        if y == 0:
            print("Y cannot be zero.")
        else:
            print(f"Result = {format_number(x / y * 100)}%")
    elif choice == "3":
        print(f"Result = {format_number(x + x * y / 100)}")
    elif choice == "4":
        print(f"Result = {format_number(x - x * y / 100)}")
    elif choice == "5":
        if x == 0:
            print("X cannot be zero.")
        else:
            print(f"Change = {format_number((y - x) / x * 100)}%")


#---------------------------STATISTICS---------------------------------

def stats_menu():
    n = ask_int("How many numbers? ", minimum=1)
    nums = [ask_float(f"Enter number {i + 1}: ") for i in range(n)]

    print(f"Sum      = {format_number(sum(nums))}")
    print(f"Average  = {format_number(sum(nums) / n)}")
    print(f"Median   = {format_number(statistics.median(nums))}")
    print(f"Maximum  = {format_number(max(nums))}")
    print(f"Minimum  = {format_number(min(nums))}")
    print(f"Range    = {format_number(max(nums) - min(nums))}")
    print(f"Std dev (population) = {format_number(statistics.pstdev(nums))}")
    if n > 1:
        print(f"Std dev (sample)     = {format_number(statistics.stdev(nums))}")


#  UNIT CONVERTER
#  Each row: (category, unit A, unit B, function A->B, function B->A)
#  Because we store both directions, every "↔" really works both ways.

def factor(f):
    """Make a pair of functions for simple 'multiply by a number' units."""
    return (lambda x: x * f), (lambda x: x / f)


CONVERSIONS = [
    ("Length",      "Km", "Miles", *factor(0.621371)),
    ("Weight",      "Kg", "lbs", *factor(2.20462)),
    ("Temperature", "°C", "°F",
        lambda c: c * 9 / 5 + 32, lambda f: (f - 32) * 5 / 9),
    ("Length",      "Meters", "Feet", *factor(3.28084)),
    ("Length",      "Centimeters", "Inches", *factor(0.393701)),
    ("Length",      "Meters", "Yards", *factor(1.09361)),
    ("Weight",      "Kg", "Grams", *factor(1000)),
    ("Weight",      "Grams", "Ounces", *factor(0.035274)),
    ("Temperature", "°C", "Kelvin",
        lambda c: c + 273.15, lambda k: k - 273.15),
    ("Temperature", "°F", "Kelvin",
        lambda f: (f - 32) * 5 / 9 + 273.15,
        lambda k: (k - 273.15) * 9 / 5 + 32),
    ("Speed",       "Km/h", "mph", *factor(0.621371)),
    ("Speed",       "m/s", "Km/h", *factor(3.6)),
    ("Time",        "Seconds", "Minutes", *factor(1 / 60)),
    ("Time",        "Minutes", "Hours", *factor(1 / 60)),
    ("Time",        "Hours", "Days", *factor(1 / 24)),
    ("Area",        "m²", "ft²", *factor(10.7639)),
    ("Area",        "Acres", "Hectares", *factor(0.404686)),
    ("Volume",      "Liters", "Gallons", *factor(0.264172)),
    ("Volume",      "Liters", "Milliliters", *factor(1000)),
    ("Pressure",    "Bar", "PSI", *factor(14.5038)),
    ("Pressure",    "Pascal", "Bar", *factor(1e-5)),
    ("Energy",      "Joules", "Calories", *factor(1 / 4.184)),
    ("Energy",      "kWh", "Joules", *factor(3600000)),
    ("Power",       "Watts", "Kilowatts", *factor(1e-3)),
    ("Power",       "Watts", "Horsepower", *factor(1 / 745.7)),
    ("Data",        "Bytes", "KB", *factor(1 / 1024)),
    ("Data",        "MB", "GB", *factor(1 / 1024)),
    ("Data",        "GB", "TB", *factor(1 / 1024)),
    ("Angle",       "Degrees", "Radians", *factor(math.pi / 180)),
    ("Frequency",   "Hz", "kHz", *factor(1e-3)),
    ("Frequency",   "MHz", "GHz", *factor(1e-3)),
    ("Force",       "Newton", "Kilonewton", *factor(1e-3)),
    ("Force",       "Newton", "Pound-force", *factor(0.224809)),
    ("Torque",      "N·m", "lb·ft", *factor(0.737562)),
    ("Resistance",  "Ω", "kΩ", *factor(1e-3)),
    ("Voltage",     "V", "mV", *factor(1000)),
    ("Current",     "A", "mA", *factor(1000)),
]


def unit_converter():
    print()
    for number, (category, a, b, _, _) in enumerate(CONVERSIONS, 1):
        print(f"{number:>2}. {category} ({a} ↔ {b})")

    choice = ask_int(f"Enter your choice (1-{len(CONVERSIONS)}): ", minimum=1)
    if choice > len(CONVERSIONS):
        print(f"Invalid choice! Please enter a number from 1 to {len(CONVERSIONS)}.")
        return

    category, a, b, a_to_b, b_to_a = CONVERSIONS[choice - 1]
    print(f"1. {a} → {b}")
    print(f"2. {b} → {a}")
    direction = input("Direction (1 or 2): ").strip()

    if direction == "1":
        value = ask_float(f"Enter value in {a}: ")
        print(f"{format_number(value)} {a} = {format_number(a_to_b(value))} {b}")
    elif direction == "2":
        value = ask_float(f"Enter value in {b}: ")
        print(f"{format_number(value)} {b} = {format_number(b_to_a(value))} {a}")
    else:
        print("Invalid direction.")


#------------------------NUMBER BASE CONVERTER----------------------------

def base_menu():
    print("\n1. Decimal → Binary / Octal / Hex")
    print("2. Binary  → Decimal")
    print("3. Octal   → Decimal")
    print("4. Hex     → Decimal")
    choice = input("Enter your choice (1-4): ").strip()

    try:
        if choice == "1":
            n = ask_int("Enter a whole number: ")
            print(f"Binary = {bin(n)[2:] if n >= 0 else '-' + bin(n)[3:]}")
            print(f"Octal  = {oct(n)[2:] if n >= 0 else '-' + oct(n)[3:]}")
            print(f"Hex    = {hex(n)[2:].upper() if n >= 0 else '-' + hex(n)[3:].upper()}")
        elif choice in ("2", "3", "4"):
            base = {"2": 2, "3": 8, "4": 16}[choice]
            text = input("Enter the number: ").strip()
            print(f"Decimal = {int(text, base)}")
        else:
            print("Invalid choice")
    except ValueError:
        print("That is not a valid number for this base.")

#-----------------MEMORY  (M+ M- MC MR)----------------------

def memory_add(value):
    global memory
    memory += value
    print(f"Memory = {format_number(memory)}")


def memory_menu():
    global memory
    print(f"\nCurrent memory value: {format_number(memory)}")
    print("1. M+ (Add to memory)")
    print("2. M- (Subtract from memory)")
    print("3. MC (Memory clear)")
    print("4. MR (Memory recall)")
    choice = input("Choose (1-4): ").strip()

    if choice == "1":
        memory_add(ask_float("Enter value to add: "))
    elif choice == "2":
        memory_add(-ask_float("Enter value to subtract: "))
    elif choice == "3":
        memory = 0
        print("Memory cleared.")
    elif choice == "4":
        print(f"Memory value: {format_number(memory)}")
    else:
        print("Invalid choice! Please enter a number from 1 to 4.")


#------------------HISTORY----------------------

def show_history():
    if not history:
        print("No history available.")
        return
    print("\n---History---")
    for i, item in enumerate(history, 1):
        print(f"{i}. {item}")
    print("_____________")


def save_history():
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        for item in history:
            file.write(item + "\n")
    print(f"History saved to '{HISTORY_FILE}'.")


def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            history = [line.strip() for line in file if line.strip()]
        print(f"History loaded: {len(history)} past calculations.")
    else:
        history = []
        print("No existing history found.")


def clear_history():
    global history
    history = []
    print("History cleared (not yet saved to file).")


