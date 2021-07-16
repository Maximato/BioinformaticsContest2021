def read_data(filename: str) -> list:
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


def taskF2(organisms: list, power: float) -> str:
    print("disease stat collecting")
    disease_stat, ill_count, health_count = _get_disease_stats(organisms)
    print(disease_stat)

    print("chi2 calculation")
    chi2_calculations = []
    for stat_in_pos in disease_stat:
        chi2_calculations.append(_calc_chi2(stat_in_pos, ill_count, health_count))
    print(chi2_calculations)

    print("find interval\n")
    max_correlation = max(chi2_calculations)

    intervals = [i for i, chi2 in enumerate(chi2_calculations) if chi2 > max_correlation*power]

    if len(intervals) == 1:
        return f"{intervals[0]} {intervals[0]}"

    return f"{intervals[0]} {intervals[-1]}"


def _get_disease_stats(organisms: list) -> (list, int, int):
    order = ["A", "T", "G", "C"]
    disease_stat = [{"ill": [0, 0, 0, 0], "ok": [0, 0, 0, 0]} for _ in range(len(organisms[0][1]))]
    ill_count = 0
    health_count = 0
    for is_ill, seq in organisms:
        if is_ill == "+":
            health_count += 1
            for i, sign in enumerate(seq):
                disease_stat[i]["ill"][order.index(sign)] += 1
        else:
            ill_count += 1
            for i, sign in enumerate(seq):
                disease_stat[i]["ok"][order.index(sign)] += 1

    return disease_stat, ill_count, health_count


def _calc_chi2(stat_in_pos: dict, ill_count: int, health_count: int) -> float:
    # H0 hypothesis - stat position do not correlate with disease
    expected = [(stat_in_pos["ill"][i] + stat_in_pos["ok"][i])/(ill_count+health_count)*health_count for i in range(4)]

    score = 0
    for i in range(4):
        if expected[i] != 0:
            score += 1/expected[i]*(stat_in_pos["ok"][i]-expected[i])**2
    return score


# level 1
with open("output/F2L1.txt", "w") as w:
    for task_par in read_data("final/Q2/1.txt"):
        w.write(taskF2(task_par, power=0.9) + "\n")

# level 2
with open("output/F2L2.txt", "w") as w:
    for task_par in read_data("final/Q2/2.txt"):
        w.write(taskF2(task_par, power=0.8) + "\n")

# level 3
with open("output/F2L3.txt", "w") as w:
    for task_par in read_data("final/Q2/3.txt"):
        w.write(taskF2(task_par, power=0.7) + "\n")

# level 4
with open("output/F2L4.txt", "w") as w:
    for task_par in read_data("final/Q2/4.txt"):
        w.write(taskF2(task_par, power=0.7) + "\n")
