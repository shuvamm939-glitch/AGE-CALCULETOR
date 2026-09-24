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
    else:
        print("Invalid choice")


#-----------------MULTI NUMBER STATS-----------------

def stats_menu():
    n = int(input("How many numbers? "))
    nums = [float(input(f"Enter number {i + 1}:")) for i in range(n)]
    print(f"sum = {sum(nums)}")
    print(f"Average = {sum(nums)/n}")
    print(f"Maximum = {max(nums)}")
    print(f"Minimum = {min(nums)}")

#-----------------UNIT CONVERTER-----------------

def unit_converter():
    global memory, ch
    print("""\n1. 1. Length (Km ↔ Miles)
2. Weight (Kg ↔ lbs)
3. Temperature (°C ↔ °F)
4. Length (Meters ↔ Feet)
5. Length (Centimeters ↔ Inches)
6. Length (Meters ↔ Yards)
7. Weight (Kg ↔ Grams)
8. Weight (Grams ↔ Ounces)
9. Temperature (°C ↔ Kelvin)
10. Temperature (°F ↔ Kelvin)
11. Speed (Km/h ↔ mph)
12. Speed (m/s ↔ Km/h)
13. Time (Seconds ↔ Minutes)
14. Time (Minutes ↔ Hours)
15. Time (Hours ↔ Days)
16. Area (m² ↔ ft²)
17. Area (Acres ↔ Hectares)
18. Volume (Liters ↔ Gallons)
19. Volume (Liters ↔ Milliliters)
20. Pressure (Bar ↔ PSI)
21. Pressure (Pascal ↔ Bar)
22. Energy (Joules ↔ Calories)
23. Energy (kWh ↔ Joules)
24. Power (Watts ↔ Kilowatts)
25. Power (Watts ↔ Horsepower)
26. Data (Bytes ↔ KB)
27. Data (MB ↔ GB)
28. Data (GB ↔ TB)
29. Angle (Degrees ↔ Radians)
30. Frequency (Hz ↔ kHz)
31. Frequency (MHz ↔ GHz)
32. Force (Newton ↔ Kilonewton)
33. Force (Newton ↔ Pound-force)
34. Torque (N·m ↔ lb·ft)
35. Electrical Resistance (Ω ↔ kΩ)
36. Electrical Voltage (V ↔ mV)
37. Electrical Current (A ↔ mA)""")
    ch = input("Enter your choice (1-37): ")

unit_converter()

# 1. Kilometer to Miles
if ch == '1':
    km = float(input("Enter distance in kilometers: "))
    miles = km * 0.621371
    print(f"{km} km is equal to {miles} miles")

# 2. Kilogram to Pounds
elif ch == '2':
    kg = float(input("Enter weight in kilograms: "))
    lbs = kg * 2.20462
    print(f"{kg} kg is equal to {lbs} lbs")

# 3. Celsius to Fahrenheit
elif ch == '3':
    c = float(input("Enter temperature in Celsius: "))
    f = (c * 9/5) + 32
    print(f"{c} °C is equal to {f} °F")

# 4. Meters to Feet
elif ch == '4':
    meters = float(input("Enter length in meters: "))
    feet = meters * 3.28084
    print(f"{meters} meters is equal to {feet} feet")

# 5. Centimeters to Inches
elif ch == '5':
    cm = float(input("Enter length in centimeters: "))
    inches = cm * 0.393701
    print(f"{cm} cm is equal to {inches} inches")

# 6. Meters to Yards
elif ch == '6':
    meters = float(input("Enter length in meters: "))
    yards = meters * 1.09361
    print(f"{meters} meters is equal to {yards} yards")

# 7. Kilograms to Grams
elif ch == '7':
    kg = float(input("Enter weight in kilograms: "))
    grams = kg * 1000
    print(f"{kg} kg is equal to {grams} grams")

# 8. Grams to Ounces
elif ch == '8':
    grams = float(input("Enter weight in grams: "))
    ounces = grams * 0.035274
    print(f"{grams} grams is equal to {ounces} ounces")

# 9. Celsius to Kelvin
elif ch == '9':
    c = float(input("Enter temperature in Celsius: "))
    kelvin = c + 273.15
    print(f"{c} °C is equal to {kelvin} K")

# 10. Fahrenheit to Kelvin
elif ch == '10':
    f = float(input("Enter temperature in Fahrenheit: "))
    kelvin = (f - 32) * 5/9 + 273.15
    print(f"{f} °F is equal to {kelvin} K")

# 11. Km/h to mph
elif ch == '11':
    kmh = float(input("Enter speed in km/h: "))
    mph = kmh * 0.621371
    print(f"{kmh} km/h is equal to {mph} mph")

# 12. m/s to Km/h
elif ch == '12':
    ms = float(input("Enter speed in m/s: "))
    kmh = ms * 3.6
    print(f"{ms} m/s is equal to {kmh} km/h")

# 13. Seconds to Minutes
elif ch == '13':
    seconds = float(input("Enter time in seconds: "))
    minutes = seconds / 60
    print(f"{seconds} seconds is equal to {minutes} minutes")

# 14. Minutes to Hours
elif ch == '14':
    minutes = float(input("Enter time in minutes: "))
    hours = minutes / 60
    print(f"{minutes} minutes is equal to {hours} hours")

# 15. Hours to Days
elif ch == '15':
    hours = float(input("Enter time in hours: "))
    days = hours / 24
    print(f"{hours} hours is equal to {days} days")

# 16. Square meters to Square feet
elif ch == '16':
    sqm = float(input("Enter area in square meters: "))
    sqft = sqm * 10.7639
    print(f"{sqm} m² is equal to {sqft} ft²")

# 17. Acres to Hectares
elif ch == '17':
    acres = float(input("Enter area in acres: "))
    hectares = acres * 0.404686
    print(f"{acres} acres is equal to {hectares} hectares")

# 18. Liters to Gallons
elif ch == '18':
    liters = float(input("Enter volume in liters: "))
    gallons = liters * 0.264172
    print(f"{liters} liters is equal to {gallons} gallons")

# 19. Liters to Milliliters
elif ch == '19':
    liters = float(input("Enter volume in liters: "))
    ml = liters * 1000
    print(f"{liters} liters is equal to {ml} milliliters")

# 20. Bar to PSI
elif ch == '20':
    bar = float(input("Enter pressure in bar: "))
    psi = bar * 14.5038
    print(f"{bar} bar is equal to {psi} PSI")

# 21. Pascal to Bar
elif ch == '21':
    pascal = float(input("Enter pressure in pascal: "))
    bar = pascal / 100000
    print(f"{pascal} Pa is equal to {bar} bar")

# 22. Joules to Calories
elif ch == '22':
    joules = float(input("Enter energy in joules: "))
    calories = joules / 4.184
    print(f"{joules} J is equal to {calories} calories")

# 23. kWh to Joules
elif ch == '23':
    kwh = float(input("Enter energy in kWh: "))
    joules = kwh * 3600000
    print(f"{kwh} kWh is equal to {joules} joules")

# 24. Watts to Kilowatts
elif ch == '24':
    watts = float(input("Enter power in watts: "))
    kilowatts = watts / 1000
    print(f"{watts} W is equal to {kilowatts} kW")

# 25. Watts to Horsepower
elif ch == '25':
    watts = float(input("Enter power in watts: "))
    hp = watts / 745.7
    print(f"{watts} W is equal to {hp} horsepower")

# 26. Bytes to KB
elif ch == '26':
    bytes_value = float(input("Enter data in bytes: "))
    kb = bytes_value / 1024
    print(f"{bytes_value} bytes is equal to {kb} KB")

# 27. MB to GB
elif ch == '27':
    mb = float(input("Enter data in MB: "))
    gb = mb / 1024
    print(f"{mb} MB is equal to {gb} GB")

# 28. GB to TB
elif ch == '28':
    gb = float(input("Enter data in GB: "))
    tb = gb / 1024
    print(f"{gb} GB is equal to {tb} TB")

# 29. Degrees to Radians
elif ch == '29':
    degrees = float(input("Enter angle in degrees: "))
    radians = degrees * 3.141592653589793 / 180
    print(f"{degrees}° is equal to {radians} radians")

# 30. Hz to kHz
elif ch == '30':
    hz = float(input("Enter frequency in Hz: "))
    khz = hz / 1000
    print(f"{hz} Hz is equal to {khz} kHz")

# 31. MHz to GHz
elif ch == '31':
    mhz = float(input("Enter frequency in MHz: "))
    ghz = mhz / 1000
    print(f"{mhz} MHz is equal to {ghz} GHz")

# 32. Newton to Kilonewton
elif ch == '32':
    newton = float(input("Enter force in Newtons: "))
    kn = newton / 1000
    print(f"{newton} N is equal to {kn} kN")

# 33. Newton to Pound-force
elif ch == '33':
    newton = float(input("Enter force in Newtons: "))
    lbf = newton * 0.224809
    print(f"{newton} N is equal to {lbf} lbf")

# 34. Newton-meter to Pound-foot
elif ch == '34':
    nm = float(input("Enter torque in N·m: "))
    lbft = nm * 0.737562
    print(f"{nm} N·m is equal to {lbft} lb·ft")

# 35. Ohms to Kilohms
elif ch == '35':
    ohms = float(input("Enter resistance in ohms: "))
    kohms = ohms / 1000
    print(f"{ohms} Ω is equal to {kohms} kΩ")

# 36. Volts to Millivolts
elif ch == '36':
    volts = float(input("Enter voltage in volts: "))
    millivolts = volts * 1000
    print(f"{volts} V is equal to {millivolts} mV")

# 37. Amps to Milliamps
elif ch == '37':
    amps = float(input("Enter current in amps: "))
    milliamps = amps * 1000
    print(f"{amps} A is equal to {milliamps} mA")

else:
    print("Invalid choice! Please enter a number from 1 to 37.")


#-----------------------------MEMORY FUNCTION--------------------------

def memory_menu():
    global memory
    print(f"\nCurrent memory value: {memory}")
    print("1. M+ (Add to memory)")
    print("2. M- (Subtract from memory)")
    print("3. MC (Memory clear)")
    print("4. MR (Memory recall)")
    ch = input("Choose (1-4): ")
    if ch == '1':
        value = float(input("Enter value to add: "))
        memory += value
    elif ch == '2':
        value = float(input("Enter value to subtract: "))
        memory -= value
    elif ch == '3':
        memory = 0
    elif ch == '4':
        print(f"Memory value: {memory}")
    else:
        print("Invalid choice! Please enter a number from 1 to 4.")


#---------------------------HISTORY----------------------------------

def show_history():
    if not history:
        print("No history available.")
    else:
        print("\n---History---")
        for i, item in enumerate(history, 1):
            print(f"{i}. {item}")
        print("_____________")

def save_history():
    with open(HISTORY_FILE, "w") as file:
        for item in history:
            file.write(item+"\n")
    print(f"History saved to '{HISTORY_FILE}'.")


def load_history():
    global history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            history = [line.strip() for line in file if line.strip()]
        print(f"History Loaded from '{len(history)} past calculations.'")
    else:
        history = []
        print("No existing history found.")


def clear_history():
    global history
    history = []
    print("History cleared(not yet saved to file).")


#---------------------------MAIN MENU---------------------------------
def print_menu():
    print("\n============XD CALCULATOR============")
    print(" Type any expression directly, e.g 5+3*2 - sqrt(16)")
    print(" Supported:+-*/^, sqrt(), sin(), cos(), tan(), log(), ln(), abs(), fact(), round() pi e")
    print(" Or type a command below:")
    print(" percent -> percentage calculations")
    print(" stats -> sum/average/max/min of many numbers")
    print(" convert -> unit conversions")
    print(" memory -> memory functions (M+, M-, MC, MR)")
    print(" history -> show calculation history")
    print(" save -> save history to file")
    print(" load -> load history from file")
    print(" clear -> clear history")
    print(" exit -> Quit")
    print("=====================================")


def calculator():
    load_history() #auto-load past history when program starts
    print_menu()

    while True:
        user_input = input("\nEnter expression or command: ").strip().lower()

        if user_input == "exit":
            print("Exiting calculator. Goodbye!")
            break
        elif user_input == "percent":
            percentage_menu()
        elif user_input == "stats":
            stats_menu()
        elif user_input == "convert":
            unit_converter()
        elif user_input == "memory":
            memory_menu()
        elif user_input == "history":
            show_history()
        elif user_input == "save":
            save_history()
        elif user_input == "load":
            load_history()
        elif user_input == "clear":
            clear_history()
        else:
            result = calculate(user_input)
            print(f"Result: {result}")
            history.append(f"{user_input} = {result}")


if __name__ == "__main__":
    calculator()
    

