from bisect import bisect_left


def read_parameters(filename: str, rows: int) -> list:
    tasks_parameters = []
    with open("data/" + filename) as f:
        f.readline()
        params = []
        for i, line in enumerate(f):
            params.append(line.strip())
            if (i + 1) % rows == 0:
                tasks_parameters.append(params)
                params = []
    return tasks_parameters


def taskQ2_1(parameters: list) -> str:
    # solving for level 1 and 2
    masses = list(map(float, parameters[1].split()))
    adducts = list(map(float, parameters[2].split()))
    signals = list(map(float, parameters[3].split()))
    answers = []
    for i, signal in enumerate(signals):
        answers.append(_find_closest_pair(signal, masses, adducts))
    return "\n".join(answers)


def taskQ2_2(parameters: list) -> str:
    # solving for level 3
    masses = list(map(float, parameters[1].split()))
    adducts = list(map(float, parameters[2].split()))
    signals = list(map(float, parameters[3].split()))

    indexes = []
    summes = []
    print("run summes")
    for i, mass in enumerate(masses):
        for j, adduct in enumerate(adducts):
            indexes.append(f"{i + 1} {j + 1}")
            summes.append(mass + adduct)

    print("sort data")
    sorted_data = [(index, summ) for summ, index in sorted(zip(summes, indexes))]
    sorted_summes = [data[1] for data in sorted_data]

    print("run signals:", len(signals))
    answers = []
    i = 0
    for signal in signals:
        if i % 100 == 0:
            print(i)
        closest_sum_index = _find_closest_in_sorted(signal, sorted_summes)
        answers.append(sorted_data[closest_sum_index][0])
        i += 1
    return "\n".join(answers)


def taskQ2_3(parameters: list) -> str:
    # solving for level 4 and 5
    masses = list(map(float, parameters[1].split()))
    adducts = list(map(float, parameters[2].split()))
    signals = list(map(float, parameters[3].split()))

    print("add indexes and sort masses")
    indexes = [str(i+1) for i in range(len(masses))]
    masses_sorted_data = [(index, mass) for mass, index in sorted(zip(masses, indexes))]
    masses_sorted = [data[1] for data in masses_sorted_data]

    print(f"run signals in count: {len(signals)}")
    answers = []
    for i, signal in enumerate(signals):
        if i % 100 == 0:
            print(f"signal counting - {i}")

        min_diff = 10000000
        ans = "1 1"
        for i_a, a in enumerate(adducts):
            s = signal - a
            index_mass = _find_closest_in_sorted(s, masses_sorted)
            diff = abs(masses_sorted[index_mass] - s)
            if diff < min_diff:
                min_diff = diff
                ans = f"{masses_sorted_data[index_mass][0]} {i_a + 1}"

        answers.append(ans)
    return "\n".join(answers)


def _find_closest_pair(to: float, masses: list, adducts: list) -> str:
    minimal = 1e10
    pair = (0, 0)
    for i, mass in enumerate(masses):
        for j, adduct in enumerate(adducts):
            diff = abs(to - (mass + adduct))
            if diff < minimal:
                minimal = diff
                pair = (i, j)
    return f"{pair[0] + 1} {pair[1] + 1}"


def _find_closest_in_sorted(value: float, sorted_values: list) -> int:
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
with open("results/qual/Q2/outputQ2L1.txt", "w") as w:
    for params in read_parameters("qual/Q2/1.txt", 4):
        w.write(taskQ2_1(params) + "\n")

# level 2
with open("results/qual/Q2/outputQ2L2.txt", "w") as w:
    for params in read_parameters("qual/Q2/2.txt", 4):
        w.write(taskQ2_1(params) + "\n")

# level 3
with open("results/qual/Q2/outputQ2L3.txt", "w") as w:
    for params in read_parameters("qual/Q2/3.txt", 4):
        w.write(taskQ2_2(params) + "\n")

# level 4
with open("results/qual/Q2/outputQ2L4.txt", "w") as w:
    for params in read_parameters("qual/Q2/4.txt", 4):
        w.write(taskQ2_3(params) + "\n")

# level 5
with open("results/qual/Q2/outputQ2L5.txt", "w") as w:
    for params in read_parameters("qual/Q2/5.txt", 4):
        w.write(taskQ2_3(params) + "\n")
