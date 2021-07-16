def read_data(filename: str) -> (list, list):
    with open("data/" + filename) as f:
        n, m = map(int, f.readline().strip().split())
        known_hapl = []
        for _ in range(n):
            f.readline()
            h1 = list(f.readline().rstrip())
            h2 = list(f.readline().rstrip())
            known_hapl.append((h1, h2))

        unknown = []
        for _ in range(m):
            f.readline()
            u = list(f.readline().rstrip())
            unknown.append(u)
    return known_hapl, unknown


def taskF1(known_hapl: list, unknown: list, deep: int) -> list:
    print(f"known haplotype count: {len(known_hapl)}")
    print(f"unknown haplotype count: {len(unknown)}")

    gap_positions = [i for i, simb in enumerate(unknown[0]) if simb == "?"]

    length = len(known_hapl[0][0])
    print(f"{len(gap_positions)} gaps detected on length {length}")

    print("statistics collecting stage")
    # summ haplotypes
    for i, hapl in enumerate(known_hapl):
        known_hapl[i] = [str(int(hapl[0][k]) + int(hapl[1][k])) for k in range(length)]
    gap_stats = _collect_statistics(known_hapl, length, deep)

    print("recovering stage:")
    for i, u in enumerate(unknown):
        print(f"{i + 1} unknown recovering")
        _recovering(u, gap_positions, gap_stats)
    return unknown


def _collect_statistics(known_hapl: list, length: int, deep: int) -> dict:
    gap_stats = {"00": [[0 for i in range(length)] for _ in range(deep)],
                 "01": [[0 for i in range(length)] for _ in range(deep)],
                 "02": [[0 for i in range(length)] for _ in range(deep)],
                 "10": [[0 for i in range(length)] for _ in range(deep)],
                 "11": [[0 for i in range(length)] for _ in range(deep)],
                 "12": [[0 for i in range(length)] for _ in range(deep)],
                 "20": [[0 for i in range(length)] for _ in range(deep)],
                 "21": [[0 for i in range(length)] for _ in range(deep)],
                 "22": [[0 for i in range(length)] for _ in range(deep)],
                 "deep": deep
                 }

    for i in range(deep):
        for hapl in known_hapl:
            for pos in range(length - i):
                current = hapl[pos]
                forhead = hapl[pos + i]
                gap_stats[current + forhead][i][pos] += 1

    # convert to probability
    ks = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]
    for k in ks:
        for i, row in enumerate(gap_stats[k]):
            for j, el in enumerate(row):
                gap_stats[k][i][j] = el/len(known_hapl)
    return gap_stats


def _recovering(u: list, gap_positions: list, gap_stats: dict):
    deep = gap_stats["deep"]
    for pos in gap_positions:
        # first approximation
        prob_0 = gap_stats["00"][0][pos]
        prob_1 = gap_stats["11"][0][pos]
        prob_2 = gap_stats["22"][0][pos]

        if pos - deep < 0:
            for i in range(1, deep):
                after = u[pos + i]
                if after == "?":
                    continue

                prob_0 = prob_0*gap_stats["0" + after][i][pos]
                prob_1 = prob_1*gap_stats["1" + after][i][pos]
                prob_2 = prob_2*gap_stats["2" + after][i][pos]

        elif pos + deep >= len(u):
            for i in range(1, deep):
                prev = u[pos - i]
                prob_0 = prob_0*gap_stats[prev + "0"][i][pos - i]
                prob_1 = prob_1*gap_stats[prev + "1"][i][pos - i]
                prob_2 = prob_2*gap_stats[prev + "2"][i][pos - i]
        else:
            for i in range(1, deep):
                prev = u[pos - i]
                after = u[pos + i]
                if after == "?":
                    continue
                prob_0 = prob_0*gap_stats[prev + "0"][i][pos - i] * gap_stats["0" + after][i][pos]
                prob_1 = prob_1*gap_stats[prev + "1"][i][pos - i] * gap_stats["1" + after][i][pos]
                prob_2 = prob_2*gap_stats[prev + "2"][i][pos - i] * gap_stats["2" + after][i][pos]

        most_likely = "0"
        max_prob = prob_0
        if prob_1 > max_prob:
            most_likely = "1"
            max_prob = prob_1
        if prob_2 > max_prob:
            most_likely = "2"
        u[pos] = most_likely

    return u


# level 1
answers = taskF1(*read_data("final/Q1/1.txt"), deep=7)
with open("output/F1L1.txt", "w") as w:
    for ans in answers:
        w.write("".join(ans) + "\n\n")

# level 2
answers = taskF1(*read_data("final/Q1/2.txt"), deep=25)
with open("output/F1L2.txt", "w") as w:
    for ans in answers:
        w.write("".join(ans) + "\n\n")

# level 3
answers = taskF1(*read_data("final/Q1/3.txt"), deep=50)
with open("output/F1L3.txt", "w") as w:
    for ans in answers:
        w.write("".join(ans) + "\n\n")

# level 4
answers = taskF1(*read_data("final/Q1/4.txt"), deep=80)
with open("output/F1L4.txt", "w") as w:
    for ans in answers:
        w.write("".join(ans) + "\n\n")

# level 5
answers = taskF1(*read_data("final/Q1/5.txt"), deep=80)
with open("output/F1L5.txt", "w") as w:
    for ans in answers:
        w.write("".join(ans) + "\n\n")

# level 6
answers = taskF1(*read_data("final/Q1/6.txt"), deep=80)
with open("output/F1L6.txt", "w") as w:
    for ans in answers:
        w.write("".join(ans) + "\n\n")

# level 7
answers = taskF1(*read_data("final/Q1/7.txt"), deep=80)
with open("output/F1L7.txt", "w") as w:
    for ans in answers:
        w.write("".join(ans) + "\n\n")
