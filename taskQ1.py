def read_states(filename: str) -> list:
    tasks_parameters = []
    with open("data/" + filename) as f:
        f.readline()
        params = []
        for line in f:
            if len(line.split()) == 1:
                params.append(line.strip())
            if len(line.split()) == 2 and len(params) > 0:
                tasks_parameters.append(params)
                params = []
        tasks_parameters.append(params)
    return tasks_parameters


def taskQ1(states: list) -> str:
    codes = []
    for i in range(len(states[0])):
        code = ""
        for state in states:
            code += state[i]
        codes.append(code)

    alphabet = {}
    for i, code in enumerate(set(codes)):
        alphabet[code] = i+1

    ans = []
    for code in codes:
        ans.append(str(alphabet[code]))

    return f"{len(alphabet)}\n{' '.join(ans)}"


# level 1
answers1 = []
for params in read_states("qual/Q1/1.txt"):
    answers1.append(taskQ1(params))
with open("results/qual/Q1/outputQ1L1.txt", "w") as w:
    for ans in answers1:
        w.write(ans + "\n")

# level 2
answers2 = []
for params in read_states("qual/Q1/2.txt"):
    answers2.append(taskQ1(params))
with open("results/qual/Q1/outputQ1L2.txt", "w") as w:
    for ans in answers2:
        w.write(ans + "\n")
