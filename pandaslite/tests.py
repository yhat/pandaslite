from pandaslite import *

df = DataFrame({
    "x": range(10),
    "y": range(10),
    "z": ["a" if i%2==0 else "b" for i in range(10)],
    "a": [random.choice(["x", "y"]) for i in range(10)],
    "b": [random.choice([None, "y"]) for i in range(10)]
})
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
df.groupby(["a", "b", "z"]).apply(lambda x: x**2)

print "groupby iterator"
print "-"*80
for name, frame in df.groupby(["z", "a"]):
    print frame.apply(lambda x: x*2)

print "groupby one liner"
print df.groupby(["a", "b", "z"]).apply(lambda x: x**2)

print "describe"
print df.describe()
df = DataFrame({
    "x": range(10),
    "y": range(10),
    "z": ["a" if i%2==0 else "b" for i in range(10)],
    "a": [random.choice(["x", "y"]) for i in range(10)],
    "b": [random.choice([None, "y"]) for i in range(10)]
})


print "series"
s = Series(range(100))
print s.head()

print s.apply(lambda x: x**2)

df = DataFrame({
    "x": range(10),
    "y": range(10)
})
print df.is_null()
print df.x
print df.describe()
print s.is_null()


print DataFrame([{"x": 1}, {"x": 2}, {"x": 3}, {"x": 10}])
df = DataFrame({
    "x": range(10),
    "y": range(10),
    "z": ["a" if i%2==0 else "b" for i in range(10)],
    "a": [random.choice(["x", "y"]) for i in range(10)],
    "b": [random.choice([None, "y"]) for i in range(10)]
})
print df
print df.head()
print df.b.fillna(value=10)
print df.b.fillna(method='bfill')

s = Series([None, None, 1, 2, 34, 4])
print s.fillna(method='bfill')
s = Series(['a', None, 'b', None])
print s.fillna(method='ffill')


df = DataFrame({
    "x": range(10),
    "y": range(10),
    "z": ["a" if i%2==0 else "b" for i in range(10)],
    "a": ["a" if i%3==0 else "b" for i in range(10)],
    "b": ["a" if i%4==0 else "b" for i in range(10)]
})

print df.groupby(["a", "b", "z"]).apply(lambda x: x**2)
print df==1

for c in df.columns():
    print c, df[c].dtype
print df.dtypes()
