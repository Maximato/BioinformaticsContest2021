from bisect import bisect_left


def read_data(filename: str) -> (list, list, int):
    with open("data/" + filename) as f:
        n, d = map(int, f.readline().strip().split())
        isoforms = []
        for _ in range(n):
            isoforms.append(f.readline().strip().split(","))

        q = int(f.readline().strip())
        reads = []
        for _ in range(q):
            reads.append(f.readline().strip().split(","))
    return isoforms, reads, d


def taskF5(isoforms: list, reads: list, d: int) -> list:
    print("preprocessing")
    for i, iso in enumerate(isoforms):
        isoforms[i] = {"starts": [int(el.split("-")[0]) for el in iso],
                       "ends": [int(el.split("-")[1]) for el in iso]}

    for i, r in enumerate(reads):
        reads[i] = [tuple(map(int, el.split("-"))) for el in r]

    print(f"isoforms: {len(isoforms)}")
    print(f"reads: {len(reads)}")
    answers = []
    for ir, r in enumerate(reads):
        print(f"read {ir} of {len(reads)} is running")
        matches = []
        for i, iso in enumerate(isoforms):
            if _is_matching(r, iso, d):
                matches.append(i)

        if len(matches) == 0:
            answers.append("-1 0")
        else:
            answers.append(f"{matches[0]} {len(matches)}")
    return answers


def _is_matching(r: list, iso: dict, d: int) -> bool:
    # find start interval
    start_pos = _find_closest_in_sorted(r[0][1], iso["ends"])
    if r[0][1]-d <= iso["ends"][start_pos] <= r[0][1] + d:
        if iso["starts"][start_pos] > r[0][0] + d:
            return False
    else:
        return False

    # finding end interval
    end_pos = _find_closest_in_sorted(r[-1][0], iso["starts"])
    if r[-1][0]-d <= iso["starts"][end_pos] <= r[-1][0] + d:
        if iso["ends"][end_pos] < r[-1][1] - d:
            return False
    else:
        return False

    if len(r) != end_pos - start_pos + 1:
        return False

    if len(r) <= 2:
        return True

    sub_iso_starts = iso["starts"][start_pos+1:end_pos]
    sub_iso_ends = iso["ends"][start_pos+1:end_pos]
    sub_r = r[1:-1]

    for s, e, r_interv in zip(sub_iso_starts, sub_iso_ends, sub_r):
        if not (r_interv[0] - d <= s <= r_interv[0] + d):
            return False
        if not (r_interv[1] - d <= e <= r_interv[1] + d):
            return False
    return True


def _find_closest_in_sorted(value: int, sorted_values: list) -> int:
    pos = bisect_left(sorted_values, value)
    if pos == 0:
        return 0

    if pos == len(sorted_values):
        return pos - 1

    before = sorted_values[pos - 1]
    after = sorted_values[pos]
    if after - value < value - before:
        return pos
    else:
        return pos - 1


# level 1
with open("results/final/F5/F5L1.txt", "w") as w:
    for ans in taskF5(*read_data("final/F4/1.txt")):
        w.write(ans + "\n")

# level 2
with open("results/final/F5/F5L2.txt", "w") as w:
    for ans in taskF5(*read_data("final/F4/2.txt")):
        w.write(ans + "\n")

# level 3
with open("results/final/F5/F5L3.txt", "w") as w:
    for ans in taskF5(*read_data("final/F4/3.txt")):
        w.write(ans + "\n")

# level 4
with open("results/final/F5/F5L4.txt", "w") as w:
    for ans in taskF5(*read_data("final/F4/4.txt")):
        w.write(ans + "\n")

# level 5
with open("results/final/F5/F5L5.txt", "w") as w:
    for ans in taskF5(*read_data("final/F4/5.txt")):
        w.write(ans + "\n")

# level 6
with open("results/final/F5/F5L6.txt", "w") as w:
    for ans in taskF5(*read_data("final/F4/6.txt")):
        w.write(ans + "\n")
