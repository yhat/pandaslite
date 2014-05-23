from pandaslite import *


df = read_csv("./data/iris.csv")
print df.head()
print df.dtypes()

df = read_table("./data/iris.txt", sep="\t")
print df.head()
print df.dtypes()

df = read_csv("./data/iris.pipe", sep="|")
print df.head()
print df.dtypes()

