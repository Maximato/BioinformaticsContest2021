def _get_closest_parent(tree, q, d):
    if d == "1" or q == "1" or q == d:
        return d
    qparents = [q]
    dparents = [d]
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

        if qparent == dparent or _binary_search(dparents, qparent):
            return qparent
        if _binary_search(qparents, dparent):
            return dparent

        insort_left(qparents, qparent)
        insort_left(dparents, dparent)
        q = qparent
        d = dparent
