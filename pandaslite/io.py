from .core import DataFrame
import csv


# Utils...
def read_csv(f, sep=","):
    data = []
    columns = None
    for line in csv.reader(open(f), delimiter=sep):
        if columns is None:
            columns = line
            continue
        data.append(dict(zip(columns, line)))
    return DataFrame(data)

def read_table(f, sep="\t"):
    return read_csv(f, sep=sep)

