from bisect import bisect_left, insort_left


def read_str_parameters(filename, rows):
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


def taskQ2L1(parameters):
    masses = list(map(float, parameters[1].split()))
    adducts = list(map(float, parameters[2].split()))
    signals = list(map(float, parameters[3].split()))
    answers = []
    for i, signal in enumerate(signals):
        print(i)
        answers.append(_find_closest_pair(signal, masses, adducts))
    return "\n".join(answers)


def taskQ2L2(parameters):
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
        closest_sum_index = _find_closest_sum_index(signal, sorted_summes)
        answers.append(sorted_data[closest_sum_index][0])
        i += 1
    return "\n".join(answers)


def taskQ2L3(parameters):
    masses = list(map(float, parameters[1].split()))
    adducts = list(map(float, parameters[2].split()))
    signals = list(map(float, parameters[3].split()))

    mass_indexes = [i+1 for i in range(len(masses))]
    adduct_indexes = [i+1 for i in range(len(adducts))]

    sorted_masses = [(index, mass) for mass, index in sorted(zip(masses, mass_indexes))]
    sorted_adducts = [(index, adduct) for adduct, index in sorted(zip(adducts, adduct_indexes))]

    sorted_summes = []
    sorted_summes_ind = []
    print("run summes")
    for m in sorted_masses:
        for a in sorted_adducts:
            ind = f"{m[0]} {a[0]}"
            summ = m[1] + a[1]

            # делаю сортированный список с суммами
            sorted_summes.append(summ)
            sorted_summes_ind.append(ind)

    print("run signals:", len(signals))
    answers = []
    i = 0
    for signal in signals:
        if i % 100 == 0:
            print(i)
        closest_summ_ind = _find_closest_sum_index(signal, sorted_summes)
        answers.append(sorted_summes_ind[closest_summ_ind])
        i += 1
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
    return f"{pair[0] + 1} {pair[1] + 1}"


def _find_closest_sum_index(signal, sorted_summes):
    pos = bisect_left(sorted_summes, signal)
    if pos == 0:
        return 0

    if pos == len(sorted_summes):
        return pos - 1

    before = sorted_summes[pos - 1]
    after = sorted_summes[pos]
    if after - signal < signal - before:
        return pos
    else:
        return pos - 1


answers = []
for params in read_str_parameters("qual/inputQ2L5.txt", 4):
    answers.append(taskQ2L3(params))

with open("output/outputQ2L5.txt", "w") as w:
    for ans in answers:
        w.write(ans + "\n")
