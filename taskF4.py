def read_data(filename):
    tasks_input = []
    with open("data/" + filename) as f:
        pass
    return tasks_input


def taskF4(par):
    return "pass"


answers = []
for task_par in read_data("final/input.txt"):
    answers.append(taskF4(task_par))

with open("output/output.txt", "w") as w:
    for ans in answers:
        w.write(ans + "\n")
