import pandas as pd

data = pd.read_csv('input1.csv', header=None)

print(data[0].cumsum())