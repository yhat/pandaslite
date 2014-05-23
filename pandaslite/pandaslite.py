from prettytable import PrettyTable
from collections import OrderedDict
import random
import stats
from copy import deepcopy
import csv


def guess_type(x):
    try:
        return int(x)
    except:
        try:
            return float(x)
        except:
            return x
def trycast(dtype, x):
    try:
        return dtype(x)
    except:
        return None

class Series(object):
    def __init__(self, x):
        dtype = float
        for i in x:
            if isinstance(i, float):
                continue
            elif isinstance(i, int) and dtype not in (bool, str):
                dtype = int
            elif isinstance(i ,bool) and dtype not in (str):
                dtype = bool
            elif isinstance(i, str):
                dtype = str
                break
        # TODO: get this working...
        self.x = map(lambda i: trycast(dtype, i), x)
        self.x = x
        self.dtype = dtype

    def _to_prettytable(self):
        t = PrettyTable()
        t.add_column('value', self.x)
        return t

    def __repr__(self):
        return str(self.head())
    
    def __str__(self):
        return str(self._to_prettytable())
    
    def __html__(self):
        return self._to_prettytable().get_html_string()

    def __getitem__(self, idx):
        if isinstance(idx, int):
            idx = [idx]
        elif isinstance(idx, slice):
            return Series(self.x[idx])
        else:
            newx = []
            for i in idx:
                newx.append(self.x[i])
            return Series(newx)

    def __iter__(self):
        for i in self.x:
            yield i

    def __add__(self, x2):
        return Series(self.x + x2.x)

    def __eq__(self, x2):
        return [ix==x2 for ix in self.x]

    def is_null(self):
        return self.apply(lambda x: x is None)

    def __len__(self):
        return len(self.x)

    def size(self):
        return len(self)

    def iterrows(self):
        for i in range(len(self)):
            yield self[i]

    def ix(self, idx):
        return self[idx]

    def head(self, n=6):
        n = min(n, len(self))
        return self[range(0, n)]

    def tail(self, n=6):
        n = min(n, len(self))
        return self[range(len(self)-n, len(self))]

    def groupby(self, by):
        return self

    def apply(self, func):
        return Series(map(func, self.x))

    def describe(self):
        df = OrderedDict([("names", ["mean", "stdev", "count", "min", "max"])])
        if stats.is_numeric(self.x)==False:
            return
        df['value'] = [stats.mean(self.x), stats.stdev(self.x),
                len([i for i in self if i is not None]),
                min(self.x), max(self.x)]
        return DataFrame(df)
    
    def unique(self):
        return list(set(self.x))

    # Maths!
    def min(self):
        return min(self.x)

    def max(self):
        return max(self.x)
    
    def abs(self):
        return map(abs, self.x)

    def div(self, x):
        return map(lambda d: d / x, self.x)
    
    def divide(self, x):
        return self.div(x)

    def fillna(self, method=None, value=None):
        methods = { 'bfill', 'ffill', None }
        if value:
            return self.apply(lambda x: value if x is None else x)
        elif method in methods:
            if method=='ffill':
                for i in range(1, len(self)):
                    if self.x[i] is None:
                        self.x[i] = self.x[i-1]
                return self
            elif method=='bfill':
                for i in range(len(self) - 1, 0, -1):
                    if self.x[i-1] is None:
                        self.x[i-1] = self.x[i]
                return self

    def ffill(self):
        return self.fillna(method='ffill')
    
    def bfill(self):
        return self.fillna(method='bfill')


class DataFrame(object):
    def __init__(self, d, index=None):
        self.index = {}
        if index:
            pass
            # self.index = DataFrame({k: v for k, v in d.items() if k in index})

        lens = None
        self.d = {}
        if isinstance(d, dict):
            for k,v in d.items():
                if lens:
                    if len(v) != lens:
                        raise Exception("Values must be same length")
                else:
                    lens = len(v)
            for k, v in d.items():
                if isinstance(v, list):
                    v = Series(v)
                self.d[k] = v
        elif isinstance(d, list):
            for row in d:
                for k, v in row.items():
                    if k not in self.d:
                        self.d[k] = []
                    self.d[k].append(v)
            self = DataFrame(self.d)

    def _to_prettytable(self):
        t = PrettyTable()
        if "index" in self.columns():
            v = self['index']
            display_v = []
            for val in getattr(v, "x", v):
                if val not in display_v:
                    display_v.append(val)
                else:
                    display_v.append("")
            t.add_column("index", display_v)

        for k, v in self:
            if k=="index":
                continue
            t.add_column(k, getattr(v, "x", v))
        return t

    def __repr__(self):
        return str(self.head())
    
    def __str__(self):
        return str(self._to_prettytable())
    
    def __html__(self):
        return self._to_prettytable().get_html_string()

    def __iter__(self):
        for k,v in self.d.items():
            yield k, v

    def __getattr__(self, name):
        return self.d[name]

    def __setitem__(self, key, value):
        if isinstance(value, Series):
            self.d[key] = value
        elif isinstance(value, list):
            self.d[key] = Series(value)
        else:
            self.d[key] = Series([value for _ in range(len(self))])
        
    def __getitem__(self, idx):
        if isinstance(idx, str):
            return self.d[idx]
        elif isinstance(idx, int):
            idx = [idx]
        elif isinstance(idx, list):
            if isinstance(idx[0], str):
                return DataFrame({k: v for k, v in self if k in idx})
        elif isinstance(idx, slice):
            return DataFrame({ k: self.d[k][idx] for k in self.columns() })
        elif isinstance(idx, tuple):
            row_idx, col_idx = idx
            return DataFrame({ k: self.d[k][row_idx] for k in self.columns()[col_idx] })
        return DataFrame({ k: self.d[k][idx] for k in self.columns() })

    def __eq__(self, x):
        return DataFrame({k: v==x for k,v in self})

    def __add__(self, d2):
        for k,v in d2.d.items():
            self.d[k] += v
        return self

    def __len__(self):
        return len(self.d[self.d.keys()[0]])

    def dtypes(self):
        return DataFrame({"column": [k for k,v in self], "dtype": [v.dtype for k,v in self]})

    def size(self):
        return len(self)

    def columns(self):
        return self.d.keys()

    def is_null(self):
        return DataFrame({k: v.is_null() for k, v in self })

    def iterrows(self):
        for i in range(len(self)):
            yield self[i]

    def head(self, n=6):
        n = min(n, len(self))
        return self[range(0, n)]

    def tail(self, n=6):
        n = min(n, len(self))
        return self[range(len(self)-n, len(self))]

    def groupby(self, by):
        if isinstance(by, str):
            by = [by]

        keys = {}
        for k in by:
            keys[k] = sorted(self[k].unique())
        groups = {}
        for row in self.iterrows():
            _group = []
            for k, levels in keys.items():
                for level in levels:
                    if all(level==row[k]):
                        _group.append(row[k].x[0])
            _group = tuple(_group)
            cols = [col for col in row.columns() if col not in by]
            if _group not in groups:
                groups[_group] = row[cols]
            else:
                groups[_group] += row[cols]

        return GroupedDataFrame(groups.keys(), groups.values())

    def apply(self, func):
        for k, v in self:
            def f2(x):
                try:
                    return func(x)
                except:
                    return None
            self.d[k] = v.apply(f2)
        return self

    def describe(self):
        df = OrderedDict([("names", ["mean", "stdev", "count", "min", "max"])])
        for k, v in self:
            if stats.is_numeric(v.x)==False:
                continue
            df[k] = [
                stats.mean(v.x),
                stats.stdev(v.x),
                len([i for i in v if i is not None]),
                v.min(),
                v.max()
            ]
        return DataFrame(df)


class GroupedDataFrame(object):
    def __init__(self, names, dfs):
        self.names = sorted(names)
        self.dfs = dfs

    def __iter__(self):
        for name, df in zip(self.names, self.dfs):
            yield name, df
    
    def apply(self, func):
        final_df = None
        for name, df in zip(self.names, self.dfs):
            for k, v in df.d.items():
                v.apply(func)
            df['index'] = name
            # remove keys
            for group in self.names:
                for k in list(group):
                    continue
                    del df.d[k]
            if final_df:
                final_df += df
            else:
                final_df = df
        return final_df

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

