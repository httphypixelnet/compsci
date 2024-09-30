import utils
while True:
    print(utils.simplecalculator(input("Enter the expression: ")))
    if (input("Continue? y/n: ").lower() == "n"): break