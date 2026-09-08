from datetime import date

# WRAPPED THE CALCULATION IN A FUNCTION
def calculate_age(B_YEAR, B_MONTH, B_DAY, P_YEAR, P_MONTH, P_DAY):
    YEARS = P_YEAR - B_YEAR
    MONTHS = P_MONTH - B_MONTH
    DAYS = P_DAY - B_DAY

    if DAYS < 0:
        MONTHS -= 1
        if P_MONTH == 1:
            prev_month = 12
            prev_month_year = P_YEAR - 1
        else:
            prev_month = P_MONTH - 1
            prev_month_year = P_YEAR

        if prev_month == 12:
            days_in_prev_month = (date(prev_month_year + 1, 1, 1) - date(prev_month_year, prev_month, 1)).days
        else:
            days_in_prev_month = (date(prev_month_year, prev_month + 1, 1) - date(prev_month_year, prev_month, 1)).days

        DAYS += days_in_prev_month

    if MONTHS < 0:
        YEARS -= 1
        MONTHS += 12

    return YEARS, MONTHS, DAYS

# FOR TERMINAL 
if __name__ == "__main__":
    B_YEAR = int(input("Enter Your Birth Year: "))
    B_MONTH = int(input("Enter Your Birth Month: "))
    B_DAY = int(input("Enter Your Birth Day: "))
 
    P_YEAR = int(input("Enter Present Year: "))
    P_MONTH = int(input("Enter Present Month: "))
    P_DAY = int(input("Enter Present Day: "))
 
    YEARS, MONTHS, DAYS = calculate_age(B_YEAR, B_MONTH, B_DAY, P_YEAR, P_MONTH, P_DAY)
    print("Your Age is:", YEARS, "Years", MONTHS, "Months", DAYS, "Days")