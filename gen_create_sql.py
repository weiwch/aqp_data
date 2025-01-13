import csv
import os
def generate_create_table(csv_file, table_name, default_data_type):
    with open(csv_file, mode="r", newline="") as file:
        reader = csv.reader(file)

        columns = next(reader)

        create_table = f"CREATE TABLE {table_name} ("
        column_definitions = [f"    {col} {default_data_type}" for col in columns]
        create_table += ",".join(column_definitions)
        create_table += ");\nGO\n"
    
    return create_table

def generate_bulk_insert(table_name, fpath):
    return f"BULK INSERT {table_name} FROM '{fpath}' WITH (FORMAT = 'CSV', FIELDTERMINATOR = ',',ROWTERMINATOR = '0x0a',FIRSTROW = 2,TABLOCK);\nGO\n"

if __name__ == "__main__":
    ds = "tpch"
    prefix = "tpch100/workload/static/data"
    flist = ['t0_100.csv', 't14_100.csv', 't16_100.csv', 't1_100.csv', 't21_50.csv', 't22_100.csv', 't2_50.csv', 't4_100.csv', 't5_50.csv', 't6_100.csv', 't9_100.csv']
    lst = []
    for fname in flist:
        lst.append(fname.split("_")[0][1:])
    print(",".join(lst))
    
    print(len(lst))
    exit()
    with open("docker_cp.sh", "w") as f:
        for fname in flist:
            fname_path = os.path.join(prefix, fname)
            f.write(f"docker cp {fname_path} sql1:/{ds}\n")
    
    with open("bulkinsert.sql", "w") as f:
        for fname in flist:
            res = generate_bulk_insert(fname.split("_")[0], "/" + ds + "/" + fname)
            f.write(res)    
    # exit()       
    with open("create.sql", "w") as f:
        for fname in flist:
            fname_path = os.path.join(prefix, fname)
            res = generate_create_table(fname_path, fname.split("_")[0], "FLOAT")
            f.write(res)
            