from pandaslite import *

df = DataFrame({
    "x": range(10),
    "y": range(10),
    "z": ["a" if i%2==0 else "b" for i in range(10)],
    "a": ["a" if i%3==0 else "b" for i in range(10)],
    "b": ["a" if i%4==0 else "b" for i in range(10)]
})

print df.groupby(["a", "b", "z"]).apply(lambda x: x**2)
print df==1
