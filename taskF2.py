def read_data(filename):
    tasks_input = []
    with open("data/" + filename) as f:
        t = int(f.readline().rstrip())
        for _ in range(t):
            organisms = []
            n, l = map(int, f.readline().rstrip().split())
            for _ in range(n):
                is_ill = f.readline().strip()
                seq = f.readline().strip()
                organisms.append((is_ill, seq))
            tasks_input.append(organisms)
    return tasks_input


def taskF2(organisms):
    disease_stat = get_disease_stat(organisms)
    print(disease_stat)
    params = []
    for stat_in_pos in disease_stat:
        params.append(calc_param(stat_in_pos))
    max_score = max(params)
    intervals = [i for i, p in enumerate(params) if p > 2]
    if len(intervals) == 1:
        return f"{intervals[0]} {intervals[0]}"
    if len(intervals) == 0:
        idx = params.index(max_score)
        return f"{idx} {idx}"
    print(params)
    return f"{intervals[0]} {intervals[-1]}"


def get_disease_stat(organisms):
    # order: A, T, G, C
    order = ["A", "T", "G", "C"]
    disease_stat = [{"ill": [0, 0, 0, 0], "ok": [0, 0, 0, 0]} for _ in range(len(organisms[0][1]))]
    dds = 0
    oks = 0
    for is_ill, seq in organisms:
        if is_ill == "+":
            oks += 1
            for i, sign in enumerate(seq):
                disease_stat[i]["ill"][order.index(sign)] += 1
        else:
            dds += 1
            for i, sign in enumerate(seq):
                disease_stat[i]["ok"][order.index(sign)] += 1

    for piec in disease_stat:
        for i in range(4):
            piec["ill"][i] = piec["ill"][i]/dds
            piec["ok"][i] = piec["ill"][i] / oks

    return disease_stat


def calc_param(stat_in_pos):
    score = 1
    for i in range(4):
        score += (stat_in_pos["ill"][i] - stat_in_pos["ok"][i])**2
    return score


answers = []
for task_par in read_data("final/Q2/4.txt"):
    answers.append(taskF2(task_par))


with open("output/output-04.txt", "w") as w:
    for ans in answers:
        w.write(ans + "\n")
