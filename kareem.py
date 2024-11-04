def check_even_odd(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

# Example usage
num = 10
result = check_even_odd(num)
print(f"{num} is {result}")
