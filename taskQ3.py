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


def taskQ3L1(parameters):
    parents = parameters[0][0].split()
    informations = list(map(int, parameters[0][1].split()))
    tree = Tree()
    tree.create_node('1', '1', data=informations[0])
    identifier = 2
    for p, i in zip(parents, informations[1:]):
        tree.create_node(str(identifier), str(identifier), parent=p, data=i)
        identifier += 1
    # tree.show()

    diseases = parameters[1]
    patients = parameters[2]
    ans = []
    print("patients count:", len(patients))
    print("desiase count:", len(diseases))
    pair_value = {}
    for p, patient in enumerate(patients):
        max_hpo = 0
        likely_disease = 0
        for i, disease in enumerate(diseases):
            hpo = _calc_HPO_2(patient.split()[1:], disease.split()[1:], tree, pair_value)
            if hpo > max_hpo:
                max_hpo = hpo
                likely_disease = i + 1
        ans.append(str(likely_disease))
        print("patient calculated:", p)
    return "\n".join(ans)


def _get_closest_parent(tree, q, d):
    if d == "1" or q == "1" or q == d:
        return d
    qparents = {q}
    dparents = {d}
    while True:
        qparent = tree.parent(q)
        dparent = tree.parent(d)
        if qparent is not None:
            qparent = qparent.tag
        else:
            qparent = '1'

        if dparent is not None:
            dparent = dparent.tag
        else:
            dparent = '1'

        if qparent == dparent or (qparent in dparents):
            return qparent
        if dparent in qparents:
            return dparent
        qparents.add(qparent)
        dparents.add(dparent)
        q = qparent
        d = dparent


def _calc_HPO_1(patient, disease, tree):
    hpo = 0
    for q in patient:
        max_value = 0
        for d in disease:
            closes_parent_id = _get_closest_parent(tree, q, d)
            value = tree.get_node(closes_parent_id).data
            if value > max_value:
                max_value = value
        hpo += max_value
    return hpo


def _calc_HPO_2(patient, disease, tree, pair_value):
    hpo = 0
    for q in patient:
        max_value = 0
        for d in disease:
            pair1 = q + " " + d
            pair2 = d + " " + q
            if pair1 in pair_value:
                value = pair_value[pair1]
            elif pair2 in pair_value:
                value = pair_value[pair2]
            else:
                closes_parent_id = _get_closest_parent(tree, q, d)
                value = tree.get_node(closes_parent_id).data
                pair_value[pair1] = value
            if value > max_value:
                max_value = value
        hpo += max_value
    return hpo


params = read_one_task_params("qual/inputQ3L4.txt")
answer = taskQ3L1(params)

with open("output/outputQ3L4.txt", "w") as w:
    w.write(answer + "\n")
