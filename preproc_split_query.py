import os

# file = "STATS/workload/dist_shift/workload.sql"

# out_fmt = "STATS/workload/dist_shift/query/q{}.sql"

file = "tpch100/workload/static/workload.sql"
out_fmt = "tpch100/workload/static/query/q{}.sql"

with open(file) as f:
    lines = f.readlines()
    for line in lines:
        id, sql = line.split(":")
        id = id.strip()
        with open(out_fmt.format(id), "a") as out:
            out.write(line)
    