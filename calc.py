strings = numbers = []
supported_chars = ["*", "^", "-", "+", "/"]
def stack(input: str | int): 
    if input.__class__ == type[str]:
        strings.append(input)
    else: numbers.append(input)
    return
inputArray = list(input("Enter an equation to solve:\n--> "))
for index in range(len(inputArray)):
    try:
        n = int(inputArray[index])
        stack(n)
    except ValueError:
        if not (inputArray[index] in supported_chars):
            print("Error: invalid input.")
            exit()
        stack(inputArray[index])
