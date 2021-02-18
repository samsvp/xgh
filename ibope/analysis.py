#%%
from data import months

for m in months:
    channels = m[1].split("\n")
    for c in channels:
        print(" ".join(c.replace("–","").replace(":","").split(" ")[1:-1]), c.split(" "))
        print(c.split(" ")[-1])
    #print(m[1].split(" ")[-1])