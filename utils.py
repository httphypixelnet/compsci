import tkinter as tk
from tkinter import ttk
from flask import Flask, jsonify
import threading
import urllib.parse

def simplecalculator(inp: str):
    def tokenize(expression):
        tokens = []
        current_number = ''
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            else:
                if current_number:
                    tokens.append(float(current_number))
                    current_number = ''
                if char in '+-*/^()':
                    tokens.append(char)
        if current_number:
            tokens.append(float(current_number))
        return tokens

    def shunting_yard(tokens):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       (precedence[operator_stack[-1]] > precedence[token] or
                        (precedence[operator_stack[-1]] == precedence[token] and token != '^'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()

        while operator_stack:
            output_queue.append(operator_stack.pop())

        return output_queue

    def evaluate_rpn(rpn):
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            else:
                b, a = stack.pop(), stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)
        return stack[0]

    tokens = tokenize(inp)
    rpn = shunting_yard(tokens)
    result = evaluate_rpn(rpn)
    return result

def calculatorOLD(inp: str):
    objects = list()
    s = list()
    supported_chars = {"*": 2, "-": 3, "+": 3, "/": 2, "(": 0, ")": 0, "^": 1}

    def stack(input: str):
        try:
            int(input)
            objects.append({"type": "int", "value": input, "used": False, "valid": True})
        except ValueError:
            if (input not in supported_chars):
                return
            objects.append({"type": "str", "value": input, "used": False, "valid": True})
    inputArray = list(inp)
    for index in inputArray:
        stack(index)
    i = 0
    while i < len(objects) - 1:
        if objects[i]["type"] == "int" and objects[i + 1]["type"] == "int":
            combined_value = objects[i]["value"] + objects[i + 1]["value"]
            objects[i]["value"] = combined_value
            del objects[i + 1]
        else:
            i += 1
    print(objects)
    for n in range(len(objects)):
        try:
            supported_chars[objects[n]["value"]]
        except:
            objects[n]["valid"] = False
        if (not objects[n]["used"] and (objects[n]["type"] == "str" and supported_chars[objects[n]["value"]])):
            if (objects[n-1]["type"] == "int" and objects[n+1]["type"] == "int"):
                if (objects[n-1]["used"]):
                    s.append(eval(f'{s[len(s)-1]} {objects[n]["value"]} {objects[n+1]["value"]}'))
                else:
                    objects[n]["used"] = True
                    objects[n+1]["used"] = True
                    s.append(eval(f'{objects[n-1]["value"]} {objects[n]["value"]} {objects[n+1]["value"]}'))
    return s[len(s)-1]

def calculator(inp: str):
    def tokenize(expression):
        tokens = []
        current_number = ''
        for char in expression:
            if char.isdigit() or char == '.':
                current_number += char
            else:
                if current_number:
                    tokens.append(float(current_number))
                    current_number = ''
                if char in '+-*/^()':
                    tokens.append(char)
        if current_number:
            tokens.append(float(current_number))
        return tokens

    def shunting_yard(tokens):
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        output_queue = []
        operator_stack = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)
            elif token in precedence:
                while (operator_stack and operator_stack[-1] != '(' and
                       (precedence[operator_stack[-1]] > precedence[token] or
                        (precedence[operator_stack[-1]] == precedence[token] and token != '^'))):
                    output_queue.append(operator_stack.pop())
                operator_stack.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output_queue.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()

        while operator_stack:
            output_queue.append(operator_stack.pop())

        return output_queue

    def evaluate_rpn(rpn):
        stack = []
        for token in rpn:
            if isinstance(token, float):
                stack.append(token)
            else:
                b, a = stack.pop(), stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)
        return stack[0]

    tokens = tokenize(inp)
    rpn = shunting_yard(tokens)
    result = evaluate_rpn(rpn)
    return result

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")

        self.display = tk.Entry(master, width=30, justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.click(x)
            ttk.Button(master, text=button, command=cmd).grid(row=row, column=col, sticky='nsew')
            col += 1
            if col > 3:
                col = 0
                row += 1

        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        master.grid_columnconfigure(2, weight=1)
        master.grid_columnconfigure(3, weight=1)

    def click(self, key):
        if key == '=':
            try:
                result = calculator(self.display.get())
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, str(result))
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        else:
            self.display.insert(tk.END, key)

app = Flask(__name__)

@app.route('/api/calculator/<path:expression>')
def calculate(expression):
    try:
        decoded_expression = urllib.parse.unquote(expression)
        result = calculator(decoded_expression)
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

def run_flask():
    app.run(port=3030)

def start_gui():
    root = tk.Tk()
    CalculatorGUI(root)
    root.mainloop()

def start_server_and_gui():
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start GUI
    start_gui()