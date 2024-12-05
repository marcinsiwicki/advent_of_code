"""
Advent of Code 2024: Day 5
"""


def is_sorted(order_map, pagenums) -> bool:
    """Check if list is already in correct order per rules."""
    valid_match = []
    for i, pagenum in enumerate(pagenums):
        if pagenum in order_map:
            for dep in order_map[pagenum]:
                if dep in pagenums:
                    valid_match.append(dep in pagenums[i:])
    return False not in valid_match



def part1(orders, print_req):
    """Figure out what is printing correctly."""
    order_map = {}
    for o in orders:
        f, s = o[0], o[1]
        if f in order_map:
            order_map[f].append(s)
        else:
            order_map[f] = [s]

    running_total = 0
    incorrect_pagenums = []
    for pagenums in print_req:
        if is_sorted(order_map, pagenums):
            running_total += pagenums[len(pagenums) // 2]
        else:
            incorrect_pagenums.append(pagenums)

    return running_total, incorrect_pagenums


def part2(orders, to_sort):
    """Take incorrectly sorted pages and re-sort them."""
    order_map = {}
    for o in orders:
        f, s = o[0], o[1]
        if f in order_map:
            order_map[f].append(s)
        else:
            order_map[f] = [s]

    for pagenums in to_sort:
        while not is_sorted(order_map, pagenums): # interate algo until sorted
            for i, pagenum in enumerate(pagenums):
                if pagenum in order_map:
                    for dep in order_map[pagenum]:
                        if dep in pagenums and dep not in pagenums[i:]:
                            cur_pos = pagenums.index(dep)
                            pagenums.insert(i, pagenums.pop(cur_pos))

    running_total = 0
    for l in to_sort:
        running_total += l[len(l) // 2]

    return running_total


if __name__ == '__main__':
    page_orders = []
    pages_to_print = []

    with open('advent_of_code/2024/day05/input.txt', 'r') as f:
        list_to_update = page_orders
        for l in f.readlines():
            if l == '\n':
                list_to_update = pages_to_print
            else:
                list_to_update.append(l)

    page_orders = [i.strip().split('|') for i in page_orders]
    page_orders = [[int(i) for i in l] for l in page_orders]

    pages_to_print = [i.strip().split(',') for i in pages_to_print]
    pages_to_print = [[int(i) for i in l] for l in pages_to_print]

    n_correct, incorrect_results = part1(page_orders, pages_to_print)
    print(f'Correctly ordered reqs: {n_correct}')
    print(f'Incorrectly ordered reqs: {part2(page_orders, incorrect_results)}')