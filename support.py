def binary_search(sorted_list, el):
    while True:
        i = int(len(sorted_list)/2)
        if el > sorted_list[i]:
            sorted_list = sorted_list[i:]
        elif el < sorted_list[i]:
            sorted_list = sorted_list[:i]
        else:
            return True

        if i == 0:
            return False
