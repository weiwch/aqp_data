import os
import subprocess
import csv
import re

def count_lines_in_file(file_path):
    """
    Count the number of lines in a file using wc -l command.

    Args:
        file_path (str): Path to the file.

    Returns:
        int: Number of lines in the file.
    """
    try:
        output = subprocess.check_output(f"wc -l {file_path}", shell=True)
        lines = int(output.split()[0])
        return lines
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        return None
    
if __name__ == "__main__":
    
    ds = "tpch"
    prefix = "tpch100/workload/static/data"
    out =  "tpch100/workload/static/pquery"
    query_fmt = "tpch100/workload/static/query/q{}.sql"
    flist = ['t0_100.csv', 't14_100.csv', 't16_100.csv', 't1_100.csv', 't21_50.csv', 't22_100.csv', 't2_50.csv', 't4_100.csv', 't5_50.csv', 't6_100.csv', 't9_100.csv']
    
    for fname in flist:
        id = fname.split("_")[0][1:]
        print(f"{out}/p{id}.txt")
        # continue
        with open(f"{out}/p{id}.txt", "w") as o:
        
            csv_file = os.path.join(prefix, fname)
            with open(csv_file, mode="r", newline="") as file:
                reader = csv.reader(file)

                columns = next(reader)
            o.write(str(len(columns))+" ")
            with open(query_fmt.format(id)) as f:
                queries = f.readlines()
            
            num_line = len(queries)
            o.write(str(num_line)+" ")
            card = count_lines_in_file(csv_file)-1
            o.write(str(card)+"\n")
            o.write(" ".join(columns)+"\n")
            mp={}
            for i, cname in enumerate(columns):
                mp[cname.strip()] = i
            
            pattern = r"where([\s\S]*?);" 
            for q in queries:
                q_t = []
                for i in range(len(columns)):
                    q_t.append("-1000000000000000000.00")
                    q_t.append("1000000000000000000.00")
                matches = re.findall(pattern, q, flags=re.IGNORECASE)
                if len(matches)!=1:
                    print(q)
                else:
                    cond = matches[0].strip().split(" and ")
                    for c in cond:
                        if "=" in c:
                            lp, rp = c.split("=")
                            if lp[-1] == "<":
                                pos = mp[lp[:-1].strip()] * 2
                                q_t[pos] = rp.strip()
                            elif lp[-1] == ">":
                                pos = mp[lp[:-1].strip()] * 2 + 1
                                q_t[pos] = rp.strip()
                            else:
                                pos = mp[lp.strip()] * 2
                                q_t[pos] = rp.strip()
                                q_t[pos+1] = rp.strip()
                        else:
                            if "<" in c:
                                lp, rp = c.split("<")
                                pos = mp[lp.strip()] * 2
                                q_t[pos] = rp.strip()
                            elif ">" in c:
                                lp, rp = c.split(">")
                                pos = mp[lp.strip()] * 2 + 1
                                q_t[pos] = rp.strip()
                            else:
                                print(c)
                                raise ValueError
                o.write(" ".join(q_t)+"\n")    