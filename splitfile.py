from itertools import zip_longest

def grouper(n, iterable, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

n = 5000000

with open(r'F:\learn\test\batch2.log', encoding="utf-8") as f:
    for i, g in enumerate(grouper(n, f, fillvalue=''), 1):
        with open(r'F:\learn\test\batch2.log{0:08d}'.format(i), 'w', encoding="utf-8") as fout:
            fout.writelines(g)