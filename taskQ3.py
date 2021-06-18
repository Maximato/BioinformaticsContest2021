from treelib import Tree


def read_one_task_params(filename):
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


def taskQ3L2(parameters):
    tree = _create_tree2(parameters)

    diseases = [p.split()[1:] for p in parameters[1]]
    patients = [p.split()[1:] for p in parameters[2]]
    print("tree vertex:", len(tree))
    print("patients count:", len(patients))
    print("disease count:", len(diseases))

    ans = []
    pair_value = {}
    for p, patient in enumerate(patients):
        likely_disease = _calc_likely_disease(tree, patient, diseases, pair_value)
        ans.append(likely_disease)
        print("patient calculated:", p)
    return "\n".join(ans)


def _create_tree1(parameters):
    parents = parameters[0][0].split()
    informations = list(map(int, parameters[0][1].split()))
    tree = Tree()
    tree.create_node('1', '1', data=informations[0])
    identifier = 2
    for p, i in zip(parents, informations[1:]):
        tree.create_node(str(identifier), str(identifier), parent=p, data=i)
        identifier += 1
    tree.show()
    return tree


def _create_tree2(parameters):
    parents = parameters[0][0].split()
    informations = list(map(int, parameters[0][1].split()))
    tree = dict()
    tree['1'] = (None, informations[0], 1)
    identifier = 2
    for parent, info in zip(parents, informations[1:]):
        tree[str(identifier)] = (parent, info, tree[parent][2] + 1)
        identifier += 1
    return tree


def _get_lca1(tree, q, d):
    q_depth = tree.depth(q)
    d_depth = tree.depth(d)

    while q_depth != d_depth:
        if q_depth > d_depth:
            q_depth -= 1
            q = tree.parent(q).tag
        else:
            d_depth -= 1
            d = tree.parent(d).tag

    while d != q:
        q = tree.parent(q).tag
        d = tree.parent(d).tag
    return d


def _get_lca2(tree, q, d):
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


def _calc_likely_disease(tree, patient, diseases, pair_value):
    max_score = 0
    i_max_score = 0
    for i_des, disease in enumerate(diseases):
        score = 0
        for q in patient:
            #pair = str(i_des) + " " + q
            #if pair in pair_value:
            #    dscore = pair_value[pair]
            #else:
            dscore = _calc_dscore(tree, disease, q)
            #pair_value[pair] = dscore
            score += dscore

        if score > max_score:
            max_score = score
            i_max_score = i_des
    return str(i_max_score + 1)


def _calc_dscore(tree, disease, q):
    max_value = 0
    for d in disease:
        value = tree[_get_lca2(tree, q, d)][1]
        if value > max_value:
            max_value = value
    return max_value


params = read_one_task_params("qual/inputQ3L3.txt")
answer = taskQ3L2(params)

with open("output/outputQ3L3.txt", "w") as w:
    w.write(answer + "\n")
