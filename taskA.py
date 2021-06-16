def read_numb_parameters(filename):
    tasks_parameters = []
    with open("data/" + filename) as f:
        f.readline()
        for line in f:
            tasks_parameters.append(line.split())
    return tasks_parameters


def taskA(params):
    return str(int(params[0]) + int(params[1]))


answers = []
for params in read_numb_parameters("prequal/inputA.txt"):
    answers.append(taskA(params))

with open("output/outputA.txt", "w") as w:
    for ans in answers:
        w.write(ans + "\n")
