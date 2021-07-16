def read_parameters(filename: str, rows: int) -> list:
    tasks_parameters = []
    with open("data/" + filename) as f:
        f.readline()
        params = []
        for i, line in enumerate(f):
            params.append(line.strip())
            if (i+1) % rows == 0:
                tasks_parameters.append(params)
                params = []
    return tasks_parameters


def taskB(params: list) -> str:
    ans = []
    s = params[0]
    ss = params[1]
    for i in range(len(s)):
        if s[i:i+len(ss)] == ss:
            ans.append(str(i+1))
    return " ".join(ans)


answers = []
for params in read_parameters("prequal/inputB.txt", 2):
    answers.append(taskB(params))

with open("results/prequal/outputB.txt", "w") as w:
    for ans in answers:
        w.write(ans + "\n")
