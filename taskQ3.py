def read_params(filename: str) -> list:
    tasks_parameters = []
    with open("data/" + filename) as f:
        f.readline()
        params = []
        for line in f:
            if len(line.split()) > 1:
                params.append(line.strip())
            if len(line.split()) == 1 and len(params) > 0:
                tasks_parameters.append(params)
                params = []
        tasks_parameters.append(params)
    return tasks_parameters


def taskQ3(parameters: list, method: str = "naive"):
    parents = list(map(lambda x: int(x)-1, parameters[0][0].split()))
    informations = list(map(int, parameters[0][1].split()))
    diseases = [list(map(lambda x: int(x)-1, p.split()[1:])) for p in parameters[1]]
    patients = [list(map(lambda x: int(x)-1, p.split()[1:])) for p in parameters[2]]

    tree = _create_tree(parents, informations)
    cache_disease = {}

    sparse_table = None
    if method == "fast":
        sparse_table = _preprocessing(tree)
        print("complete preproc")

    print("tree vertex:", len(tree))
    print("patients count:", len(patients))
    print("disease count:", len(diseases))

    ans = []
    for p, patient in enumerate(patients):
        likely_disease = _calc_likely_disease(tree, patient, diseases, sparse_table, cache_disease)
        ans.append(likely_disease)
        print("patient calculated:", p)
    return "\n".join(ans)


def _create_tree(parents: list, informations: list) -> dict:
    tree = {0: (None, informations[0], 1)}
    identifier = 1
    for parent, info in zip(parents, informations[1:]):
        tree[identifier] = (parent, info, tree[parent][2] + 1)
        identifier += 1
    return tree


def _preprocessing(tree: dict) -> list:
    """
    Calculate sparse table for fast LCA finding
    """
    sparse_table = [[tree[i][0]] for i in range(len(tree))]

    # root is completed so nodes_ended = 1
    nodes_ended = 1
    j = 1
    while nodes_ended != len(tree):
        for i in range(len(tree)):
            first_jump = sparse_table[i][-1]
            jump_to = None
            if first_jump is not None:
                jump_to = sparse_table[first_jump][j - 1]
            sparse_table[i].append(jump_to)

            if sparse_table[i][-1] is None and sparse_table[i][-2] is not None:
                nodes_ended += 1
        j += 1
    return sparse_table


def _get_lca_naive(tree: dict, q: int, d: int) -> int:
    q_depth = tree[q][2]
    d_depth = tree[d][2]

    while q_depth != d_depth:
        if q_depth > d_depth:
            q_depth -= 1
            q = tree[q][0]
        else:
            d_depth -= 1
            d = tree[d][0]

    while d != q:
        q = tree[q][0]
        d = tree[d][0]
    return d


def _get_lca_fast(tree: dict, q: int, d: int, st: list) -> int:
    q_depth = tree[q][2]
    d_depth = tree[d][2]

    if q_depth < d_depth:
        q, d = d, q

    need = abs(q_depth - d_depth)

    for j in range(len(st[q])-1, -1, -1):
        jump_on = 2**j

        if jump_on <= need:
            q = st[q][j]
            need -= jump_on

    for j in range(len(st[d])-1, -1, -1):
        if st[d][j] != st[q][j]:
            q = st[q][j]
            d = st[d][j]

    if q == d:
        return q

    return st[d][0]


def _calc_likely_disease(tree: dict, patient: list, diseases: list, sparse_table: list, cache_disease: dict) -> str:
    max_score = 0
    i_max_score = 0
    for i_des, disease in enumerate(diseases):
        score = 0
        for q in patient:
            key = f"{i_des}-{q}"
            if key in cache_disease:
                add_score = cache_disease[key]
            else:
                add_score = _find_max_info(tree, disease, q, sparse_table)
                cache_disease[key] = add_score
            score += add_score

        if score > max_score:
            max_score = score
            i_max_score = i_des
    return str(i_max_score + 1)


def _find_max_info(tree: dict, disease: list, q: int, st: list) -> int:
    max_value = 0
    for d in disease:
        if st:
            lca_id = _get_lca_fast(tree, q, d, st)
        else:
            lca_id = _get_lca_naive(tree, q, d)

        value = tree[lca_id][1]
        if value > max_value:
            max_value = value

    return max_value


# level 1
params1 = read_params("qual/Q3/1.txt")
with open("results/qual/Q3/outputQ3L1.txt", "w") as w:
    w.write(taskQ3(params1) + "\n")

# level 2
params2 = read_params("qual/Q3/2.txt")
with open("results/qual/Q3/outputQ3L2.txt", "w") as w:
    w.write(taskQ3(params2, "fast") + "\n")

# level 3
params3 = read_params("qual/Q3/3.txt")
with open("results/qual/Q3/outputQ3L3.txt", "w") as w:
    w.write(taskQ3(params3, "fast") + "\n")

# level 4
params4 = read_params("qual/Q3/4.txt")
with open("results/qual/Q3/outputQ3L4.txt", "w") as w:
    w.write(taskQ3(params4, "fast") + "\n")
