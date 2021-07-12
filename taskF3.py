import random
import numpy as np


def read_data(filename):
    tasks_input = []
    with open("data/" + filename) as f:
        T = int(f.readline().rstrip())
        for _ in range(T):
            n_people, days = map(int, f.readline().rstrip().split())
            if days != 7:
                print("Warning! Days != 7")
            contacts_in_days = []
            for day in range(7):
                ncontacts = int(f.readline().rstrip())
                contacts = []
                for line in range(ncontacts):
                    a, b, p = f.readline().rstrip().split()
                    contacts.append([int(a), int(b), float(p)])
                contacts_in_days.append(contacts)
            tasks_input.append((n_people, contacts_in_days))
    return tasks_input


def taskF3_exact(n_people, contacts_in_days):
    print("size of group", n_people)

    max_spreader = None
    max_end_ilness = 0
    for spreader in range(n_people):
        mean_ilness = run_exact_simulation(spreader, contacts_in_days, 5)
        if mean_ilness > max_end_ilness:
            max_end_ilness = mean_ilness
            max_spreader = spreader
    print(f"max spreader: {max_spreader}. Score: {max_end_ilness}")
    return str(max_spreader)


def run_exact_simulation(spreader, contacts_in_days, times):
    scores = []
    for _ in range(times):
        pacients = {spreader}
        for day_contacts in contacts_in_days:
            next_pacients = set()
            for contact in day_contacts:
                if contact[0] in pacients:
                    if random.random() <= contact[2]:
                        next_pacients.add(contact[1])
            pacients = pacients.union(next_pacients)
        scores.append(len(pacients))
    return np.mean(scores)


def taskF3_fast(n_people, contacts_in_days, tn):
    print("size of group", n_people)

    if n_people < 100000:
        tops = range(n_people)
        print("exact simulation")
    else:
        tops = get_most_contactable(contacts_in_days, start=0, deep=3)
        print("most contactable:\n", tops)
        tops = [t[0] for t in tops]

    if tn == 0:
        sim_numb = 5
    else:
        sim_numb = 30

    max_spreader = None
    max_end_ilness = 0
    for i, spreader in enumerate(tops):
        if i % 50 == 0:
            print(f"spreader {i} of {len(tops)} is running...")

        mean_ilness = run_exact_simulation(spreader, contacts_in_days, sim_numb)
        if mean_ilness > max_end_ilness:
            max_end_ilness = mean_ilness
            max_spreader = spreader
    print(f"max spreader: {max_spreader}. Score: {max_end_ilness}\n")
    return str(max_spreader)


def get_most_contactable(contacts_in_days, start=0, deep=3):
    contact_counter = {}
    for i in range(start, start + deep):
        day_contacts = contacts_in_days[i]
        for a, b, p in day_contacts:
            if a in contact_counter:
                contact_counter[a] += p
            else:
                contact_counter[a] = p

    tops = sorted(contact_counter.items(), key=lambda x: x[1])[-100:]
    return tops


answers = []
for i, task_par in enumerate(read_data("final/3/test6")[:1]):
    print(f"task {i} processing ================")
    answers.append(taskF3_fast(*task_par, i))

with open("output/outputF3L6-2.txt", "w") as w:
    for ans in answers:
        w.write(ans + "\n")
