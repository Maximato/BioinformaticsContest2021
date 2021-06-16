from bisect import bisect_left


def read_str_parameters(filename, rows):
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


def taskQ2L1(parameters):
    masses = list(map(float, parameters[1].split()))
    adducts = list(map(float, parameters[2].split()))
    signals = list(map(float, parameters[3].split()))
    answers = []
    for signal in signals:
        answers.append(_find_closest_pair(signal, masses, adducts))
    return "\n".join(answers)


def taskQ2L2(parameters):
    masses = list(map(float, parameters[1].split()))
    adducts = list(map(float, parameters[2].split()))
    signals = list(map(float, parameters[3].split()))

    indexes = []
    summes = []
    for i, mass in enumerate(masses):
        for j, adduct in enumerate(adducts):
            indexes.append(f"{i+1} {j+1}")
            summes.append(mass + adduct)

    sorted_data = [(index, summ) for summ,index in sorted(zip(summes, indexes))]
    sorted_summes = [data[1] for data in sorted_data]

    answers = []
    for signal in signals:
        closest_sum_index = _find_closest_sum_index(signal, sorted_summes)
        answers.append(sorted_data[closest_sum_index][0])
    return "\n".join(answers)


def _find_closest_pair(to, masses, adducts):
    minimal = 1e10
    pair = (0, 0)
    for i, mass in enumerate(masses):
        for j, adduct in enumerate(adducts):
            diff = abs(to - (mass + adduct))
            if diff < minimal:
                minimal = diff
                pair = (i, j)
    return f"{pair[0]+1} {pair[1]+1}"


def _find_closest_sum_index(signal, sorted_summes):
    pos = bisect_left(sorted_summes, signal)
    if pos == 0:
        return 0

    if pos == len(sorted_summes):
        return pos-1

    before = sorted_summes[pos - 1]
    after = sorted_summes[pos]
    if after - signal < signal - before:
       return pos
    else:
       return pos - 1


answers = []
for params in read_str_parameters("qual/inputQ2L1.txt", 4):
    answers.append(taskQ2L1(params))

with open("output/outputQ2L1.txt", "w") as w:
    for ans in answers:
        w.write(ans + "\n")
