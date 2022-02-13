# Source: https://www.learnpython.org/

# Переменные, типы и структуры данных
## Целые числа
myint = 7
print(myint)

"""

## Числа с плавающей точкой
myfloat = 7.0
print(myfloat)
myfloat = float(7)
print(myfloat)

## Строки
mystring_1 = 'hello'
print(mystring_1)
mystring_2 = "hello"
print(mystring_2)
mystring_3 = "Don't worry about apostrophes"
print(mystring_3)

## Логические

yes = True
no = False

## Словари

phonebook = {
    "John": 938477566,
    "Jack": 938377264,
    "Jill": 947662781
}
print(phonebook)

phonebook["Jake"] = 938273443
del phonebook["Jill"]
for name, number in phonebook.items():
    print("Phone number of %s is %d" % (name, number))

# Условия

## Логические условия

x = 2
print(x == 2)  # prints out True
print(x == 3)  # prints out False
print(x < 3)  # prints out True

name = "John"
age = 23
if name == "John" and age == 23:
    print("Your name is John, and you are also 23 years old.")

if name == "John" or name == "Rick":
    print("Your name is either John or Rick.")

## Условие "in"

name = "John"
if name in ["John", "Rick"]:
    print("Your name is either John or Rick.")

statement = False
another_statement = True
if statement is True:
    # do something
    pass
elif another_statement is True:  # else if
    # do something else
    pass
else:
    # do another thing
    pass
## Условие "is"

x = [1, 2, 3]
y = [1, 2, 3]
print(x == y)  # Prints out True
print(x is y)  # Prints out False

## Условие "not"

print(not False)  # Prints out True
print((not False) == (False))  # Prints out False


# Функции

def my_function(username, greeting):
    print(f"Hello {username} From My Function! I wish you {greeting}!")


def sum_two_numbers(a, b):
    return a + b
"""