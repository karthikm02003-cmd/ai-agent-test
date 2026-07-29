# Get input for the first number
num1 = float(input("Enter the first number: "))

# Get input for the second number
num2 = float(input("Enter the second number: "))

# Get input for the desired operation
operation = input("Enter operation (+, -, *, /): ")

# Perform the calculation based on the operation
if operation == '+':
    result = num1 + num2
    print(f"Result: {num1} + {num2} = {result}")
elif operation == '-':
    result = num1 - num2
    print(f"Result: {num1} - {num2} = {result}")
elif operation == '*':
    result = num1 * num2
    print(f"Result: {num1} * {num2} = {result}")
elif operation == '/':
    if num2 == 0:
        print("Error: Cannot divide by zero!")
    else:
        result = num1 / num2
        print(f"Result: {num1} / {num2} = {result}")
else:
    print("Error: Invalid operation. Please use +, -, *, or /.")