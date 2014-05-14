from prettytable import PrettyTable
from collections import OrderedDict
import random
import stats


class GroupedDataFrame(object):
    def __init__(self, names, dfs):
        self.names = names
        self.dfs = dfs

    def __iter__(self):
        for name, df in zip(self.names, self.dfs):
            yield name, df
    
    def apply(self, func):
        final_df = None
        for df in self.dfs:
            for k, v in df.d.items():
                def f2(x):
                    try:
                        return func(x)
                    except:
                        return None
                df.d[k] = map(f2, v)
            if final_df:
                final_df += df
            else:
                final_df = df
        return final_df

class DataFrame(object):
    def __init__(self, d, index=None):
        lens = None
        for k,v in d.items():
            if lens:
                if len(v) != lens:
                    raise Exception("Values must be same length")
            else:
                lens = len(v)
        self.d = d
        self.index = {}
        if index:
            for row in self.iterrows():
                print row[index]
    
    def _to_prettytable(self):
        t = PrettyTable()
        for k, v in self.index.items():
            t.add_column(k, v)
        for k, v in self.d.items():
            t.add_column(k, v)
        return t

    def __repr__(self):
        return str(self.head())
    
    def __str__(self):
        return str(self._to_prettytable())
    
    def __html__(self):
        return self._to_prettytable().get_html_string()

    def __getattr__(self, name):
        return DataFrame({ name: self.d[name] })

    def __getitem__(self, idx):
        if isinstance(idx, str):
            return self.d[idx]
        elif isinstance(idx, int):
            idx = [idx]
        elif isinstance(idx, list):
            if isinstance(idx[0], str):
                return DataFrame({k: v for k, v in self.d.items() if k in idx})
        newd = {}
        for k, v in self.d.items():
            newd[k] = []
            for i in idx:
                newd[k].append(v[i])
        return DataFrame(newd)

    def __add__(self, d2):
        for k,v in d2.d.items():
            self.d[k] += v
        return self

    def __len__(self):
        return len(self.d[self.d.keys()[0]])

    def size(self):
        return len(self)

    def columns(self):
        return self.d.keys()

    def iterrows(self):
        for i in range(len(self)):
            yield self[i]

    def head(self, n=6):
        return self[range(0, n)]

    def tail(self, n=6):
        return self[range(len(self)-n, len(self))]

    def groupby(self, by):
        if isinstance(by, str):
            by = [by]

        keys = {}
        for k in by:
            keys[k] = sorted(list(set(self.d[k])))
        groups = {}
        for row in df.iterrows():
            _group = []
            for k, levels in keys.items():
                for level in levels:
                    if level==row[k][0]:
                        _group.append(row[k][0])
            _group = tuple(_group)
            cols = [col for col in row.columns() if col not in by]
            if _group not in groups:
                groups[_group] = row[cols]
            else:
                groups[_group] += row[cols]

        
        return GroupedDataFrame(groups.keys(), groups.values())

    def apply(self, func):
        for k, v in self.d.items():
            def f2(x):
                try:
                    return func(x)
                except:
                    return None
            self.d[k] = map(f2, v)
        return self

    def describe(self):
        df = OrderedDict([("names", ["mean", "stdev", "count"])])
        for k, v in self.d.items():
            if stats.is_numeric(v)==False:
                continue
            df[k] = [stats.mean(v), stats.stdev(v), len([i for i in v if i is not None])]
        return DataFrame(df)

df = DataFrame({
    "x": range(10),
    "y": range(10),
    "z": ["a" if i%2==0 else "b" for i in range(10)],
    "a": [random.choice(["x", "y"]) for i in range(10)],
    "b": [random.choice([None, "y"]) for i in range(10)]
}, index=['a'])
print df
print df.__str__()
print df.__html__()
print len(df)
print df.head()
print df.tail()
print df.x
print df.y

print "groupby iterator"
for name, frame in df.groupby("z"):
    print frame.apply(lambda x: x*2)
# df.groupby("z").apply(lambda x: x**2)

print "groupby iterator"
print "-"*80
for name, frame in df.groupby(["z", "a"]):
    print frame.apply(lambda x: x*2)

print "groupby one liner"
print df.groupby("z").apply(lambda x: x**2)

print df.describe()
df = DataFrame({
    "x": range(10),
    "y": range(10),
    "z": ["a" if i%2==0 else "b" for i in range(10)],
    "a": [random.choice(["x", "y"]) for i in range(10)],
    "b": [random.choice([None, "y"]) for i in range(10)]
}, index=['a'])
