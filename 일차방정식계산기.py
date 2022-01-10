print("Pancake's linear equation Solver.")

# input equation
ec = False
while not ec:
    e = input("Enter Equation. (variable must be 'x') ")

    if not "=" in e:
        print("Wrong equation. (MUST INCLUDE '=')")
    else:
        ec = 1

# making parts before parsing
eq = {}
e = e.split("=")
eq['left'] = {'exp':e[0]}
eq['right'] = {'exp':e[1]}

# pre-solving equation
if eq['left']['exp'] == eq['right']['exp']:
    print("There are innumerable solutions to the equation.")
else:
    # parsing equation's left part
    if "x" in eq['left']['exp']:
        if eq['left']['exp'].split("x")[0] != "" and eq['left']['exp'].split("x")[0] != "-":
            eq['left']['a'] = eval(eq['left']['exp'].split("x")[0])
        elif eq['left']['exp'].split("x")[0] == "-":
            eq['left']['a'] = -1
        else:
            eq['left']['a'] = 1
        try:
            if len(eq['left']['exp'].split("x")[1]) > 1:
                eq['left']['b'] = eval(eq['left']['exp'].split("x")[1])
            else:
                eq['left']['b'] = 0
        except IndexError:
            eq['left']['b'] = 0
    else:
        eq['left']['a'] = 0
        eq['left']['b'] = eval(eq['left']['exp'])

    # parsing equation's right part
    if "x" in eq['right']['exp']:
        if eq['right']['exp'].split("x")[0] != "" and eq['right']['exp'].split("x")[0] != "-":
            eq['right']['c'] = eval(eq['right']['exp'].split("x")[0])
        elif eq['right']['exp'].split("x")[0] == "-":
            eq['left']['c'] = -1
        else:
            eq['right']['c'] = 1
        try:
            if len(eq['right']['exp'].split("x")[1]) > 1:
                eq['right']['d'] = eval(eq['right']['exp'].split("x")[1])
            else:
                eq['right']['d'] = 0
        except IndexError:
            eq['right']['d'] = 0
    else:
        eq['right']['c'] = 0
        eq['right']['d'] = eval(eq['right']['exp'])

    # solving
    if eq['left']['a']-eq['right']['c'] != 0:
        eq["answer"] = int(eval(f"({eq['right']['d']}-{eq['left']['b']})/({eq['left']['a']}-{eq['right']['c']})")) \
                       if eval(f"({eq['right']['d']}-{eq['left']['b']})/({eq['left']['a']}-{eq['right']['c']})") % 1 == 0 \
                       else round(eval(f"({eq['right']['d']}-{eq['left']['b']})/({eq['left']['a']}-{eq['right']['c']})"), 10)
        print(f"The answer is {eq['answer']}")
    else:
        print("x does not exist.")

