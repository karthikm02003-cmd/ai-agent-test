def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error! Division by zero."
    return x / y

print("Simple Calculator")

while True:
    try:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
    except ValueError:
        print("Invalid input. Please enter numbers only.")
        continue

    print("Select operation:")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")

    choice = input("Enter choice(1/2/3/4) or operator(+, -, *, /): ")

    if choice in ('1', '+'):
        print(f"{num1} + {num2} = {add(num1, num2)}")
    elif choice in ('2', '-'):
        print(f"{num1} - {num2} = {subtract(num1, num2)}")
    elif choice in ('3', '*'):
        print(f"{num1} * {num2} = {multiply(num1, num2)}")
    elif choice in ('4', '/'):
        result = divide(num1, num2)
        print(f"{num1} / {num2} = {result}")
    else:
        print("Invalid input. Please enter a valid operation.")

    another_calculation = input("Do you want to perform another calculation? (yes/no): ")
    if another_calculation.lower() != 'yes':
        break