from pandaslite import *


s = Series(range(10))
print s[1:4]

df = DataFrame({
    "x": range(10),
    "y": range(10)
})

print df[:4, :2]
