def read_data(filename):
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


def taskF1(known_hapl, unknown):
    print(known_hapl)
    print(unknown)
    gap_positions = [i for i, simb in enumerate(unknown[0]) if simb == "?"]

    most_freq = collect_statistics(known_hapl, gap_positions)
    print(most_freq)
    print(gap_positions)
    for u in unknown:
        for i, pos in enumerate(gap_positions):
            u[pos] = str(most_freq[i])
    print(gap_positions)
    return unknown


def collect_statistics(known_hapl, gap_positions):
    most_freq = []
    for pos in gap_positions:
        freq = {0: 0, 1: 0, 2: 0}
        for hapl in known_hapl:
            freq[int(hapl[0][pos])+int(hapl[1][pos])] += 1
        most_freq.append(max(freq, key=freq.get))
    return most_freq


def taskF1_2(known_hapl, unknown):
    print(f"size known: {len(known_hapl)}, size unknown: {len(unknown)}")
    gap_positions = [i for i, simb in enumerate(unknown[0]) if simb == "?"]
    #gap_positions.reverse()

    length = len(known_hapl[0][0])
    print(f"gaps detected {len(gap_positions)} on length {length}")

    # summ haplotypes
    for i, hapl in enumerate(known_hapl):
        known_hapl[i] = [str(int(hapl[0][k])+int(hapl[1][k])) for k in range(length)]

    print("statistics collecting")
    gap_stats = collect_statistics2(known_hapl, length, n_iter=25)
    print(gap_stats)

    print("run recovering")
    for i, u in enumerate(unknown):
        print(f"{i+1} u recovering")
        recovering(u, gap_positions, gap_stats)
    return unknown


def collect_statistics2(known_hapl, length, n_iter=4):
    gap_stats = {"00": [[0 for i in range(length)] for _ in range(n_iter)],
                   "01": [[0 for i in range(length)] for _ in range(n_iter)],
                   "02": [[0 for i in range(length)] for _ in range(n_iter)],
                   "10": [[0 for i in range(length)] for _ in range(n_iter)],
                   "11": [[0 for i in range(length)] for _ in range(n_iter)],
                   "12": [[0 for i in range(length)] for _ in range(n_iter)],
                   "20": [[0 for i in range(length)] for _ in range(n_iter)],
                   "21": [[0 for i in range(length)] for _ in range(n_iter)],
                   "22": [[0 for i in range(length)] for _ in range(n_iter)],
                   "iterations": n_iter
                   }

    for i in range(n_iter):
        for hapl in known_hapl:
            for pos in range(length-i):
                current = hapl[pos]
                forhead = hapl[pos+i]
                gap_stats[current+forhead][i][pos] += 1
    #for key in ["00", "1.txt", "2.txt", "10", "11", "10", "20", "20", "22"]:
    #    gap_stats[key] = [[v/len(known_hapl) for v in gap_stats[key][i]] for i in range(n_iter)]
    return gap_stats


def recovering(u, gap_positions, gap_stats):
    #u_probs = [Q1 for _ in range(len(u))]

    # first approximation
    for pos in gap_positions:
        most_likely = "0"
        if gap_stats["11"][0][pos] > gap_stats[most_likely*2][0][pos]:
            most_likely = "Q1"
        if gap_stats["22"][0][pos] > gap_stats[most_likely*2][0][pos]:
            most_likely = "Q2"
        #u_probs[pos] = gap_stats[most_likely*Q2][0][pos]
        u[pos] = most_likely

    for i in range(1, gap_stats["iterations"]):
        for pos in gap_positions:
            if pos - i < 0:
                after = u[pos + i]
                prob_0 = gap_stats["0" + after][i][pos]
                prob_1 = gap_stats["Q1" + after][i][pos]
                prob_2 = gap_stats["Q2" + after][i][pos]
            elif pos+i >= len(u):
                prev = u[pos - i]
                prob_0 = gap_stats[prev + "0"][i][pos - i]
                prob_1 = gap_stats[prev + "Q1"][i][pos - i]
                prob_2 = gap_stats[prev + "Q2"][i][pos - i]
            else:
                prev = u[pos-i]
                after = u[pos+i]
                # probs
                prob_0 = gap_stats[prev + "0"][i][pos-i]*gap_stats["0" + after][i][pos]
                prob_1 = gap_stats[prev + "Q1"][i][pos-i]*gap_stats["Q1" + after][i][pos]
                prob_2 = gap_stats[prev + "Q2"][i][pos-i]*gap_stats["Q2" + after][i][pos]

            most_likely = "0"
            max_prob = prob_0
            if prob_1 > max_prob:
                most_likely = "Q1"
                max_prob = prob_1
            if prob_2 > max_prob:
                most_likely = "Q2"
                max_prob = prob_2
            u[pos] = most_likely
            #u_probs[pos] = max_prob
    return u


answers = taskF1_2(*read_data("final/Q1/7.txt"))

with open("output/outputF1L7.txt", "w") as w:
    for ans in answers:
        w.write("".join(ans) + "\n\n")
