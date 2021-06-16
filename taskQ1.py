def read_states(filename):
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


def taskQ1(states):
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


answers = []
for params in read_states("qual/inputQ1LV.txt"):
    answers.append(taskQ1(params))

with open("output/outputQ1LV.txt", "w") as w:
    for ans in answers:
        w.write(ans + "\n")
