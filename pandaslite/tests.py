from pandaslite import *

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
df.groupby("z").apply(lambda x: x**2)

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
