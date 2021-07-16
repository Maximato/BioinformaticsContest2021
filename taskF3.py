import random
import numpy as np


def read_data(filename: str) -> list:
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


def taskF3(n_people: int, contacts_in_days: list, simulation_times: int = 100, short_simulation: int = 5,
           start_day: int = 0, deep: int = 3, top_count: int = 100, hard_limit: int = 100000) -> str:
    print("size of group", n_people)

    # find the most perspective people for simulation
    if n_people < hard_limit:
        spreaders = range(n_people)
        print("exact simulation")
    else:
        spreaders = _get_most_contactable(contacts_in_days, start_day, deep, top_count)
        simulation_times = short_simulation

    max_spreader = None
    max_infected = 0
    for i, spreader in enumerate(spreaders):
        if i % 50 == 0:
            print(f"spreader {i} of {len(spreaders)} is running...")

        mean_ilness = _run_exact_simulation(spreader, contacts_in_days, simulation_times)
        if mean_ilness > max_infected:
            max_infected = mean_ilness
            max_spreader = spreader

    print(f"max spreader: {max_spreader}. Score: {max_infected}\n")
    return str(max_spreader)


def _get_most_contactable(contacts_in_days: list, start_day: int, deep: int, top_count: int) -> list:
    contact_counter = {}
    for i in range(start_day, start_day + deep):
        day_contacts = contacts_in_days[i]
        for a, b, p in day_contacts:
            if a in contact_counter:
                contact_counter[a] += p
            else:
                contact_counter[a] = p

    tops = sorted(contact_counter.items(), key=lambda x: x[1], reverse=True)[:top_count]
    print("most contactable:\n", tops)
    tops = [t[0] for t in tops]
    return tops


def _run_exact_simulation(spreader: int, contacts_in_days: list, simulation_times: int) -> np.ndarray:
    scores = []
    for _ in range(simulation_times):
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


# level 1
with open("results/final/F3/F3L1.txt", "w") as w:
    for i, task_par in enumerate(read_data("final/F3/1.txt")):
        print(f"task {i} processing ================")
        w.write(taskF3(*task_par, simulation_times=100) + "\n")

# level 2
with open("results/final/F3/F3L2.txt", "w") as w:
    for i, task_par in enumerate(read_data("final/F3/2.txt")):
        print(f"task {i} processing ================")
        w.write(taskF3(*task_par, simulation_times=200) + "\n")

# level 3
with open("results/final/F3/F3L3.txt", "w") as w:
    for i, task_par in enumerate(read_data("final/F3/3.txt")):
        print(f"task {i} processing ================")
        w.write(taskF3(*task_par, simulation_times=100) + "\n")

# level 4
with open("results/final/F3/F3L4.txt", "w") as w:
    for i, task_par in enumerate(read_data("final/F3/4.txt")):
        print(f"task {i} processing ================")
        w.write(taskF3(*task_par, simulation_times=10, short_simulation=5, top_count=50) + "\n")

# level 5
with open("results/final/F3/F3L5.txt", "w") as w:
    for i, task_par in enumerate(read_data("final/F3/5.txt")):
        print(f"task {i} processing ================")
        if i == 7:
            tc = 5000
        else:
            tc = 1000
        w.write(taskF3(*task_par, simulation_times=10, short_simulation=5, top_count=tc, hard_limit=10000) + "\n")

# level 6
with open("results/final/F3/F3L6.txt", "w") as w:
    for i, task_par in enumerate(read_data("final/F3/6.txt")):
        print(f"task {i} processing ================")
        if i == 0:
            tc = 100
        else:
            tc = 1000
        w.write(taskF3(*task_par, short_simulation=10, top_count=tc, hard_limit=10000) + "\n")
