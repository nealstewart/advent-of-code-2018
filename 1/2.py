import pandas as pd


def get_cumsum(data: pd.Series):
    cumsum = 0
    i = 0
    while True:
        yield cumsum
        cumsum += data.iloc[i]
        i = (i + 1) % data.count()

def do_stuff():
    frequencies = set()

    data = pd.read_csv('input1.csv', header=None, index_col=None)[0]
    print("a")

    for sum in get_cumsum(data):
        print("b")
        print(sum)
        if (sum in frequencies):
            return sum
        frequencies.add(sum)

print(do_stuff())