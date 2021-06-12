import os
import pandas as pd

print("Loading files...")

not_processed = []
dfs = []
for d, _, f in os.walk("./dataset/scraped_trial2"):
    for file in f:
        print("Processing: ", file)
        current_file = os.path.join(d, file)
        try:
            data = pd.read_json(current_file, lines=True)
            dfs.append(data)
        except:
            not_processed.append(current_file)

print("Saving to parquet...")
df = pd.concat(dfs, ignore_index=True)
df.to_parquet("dataset/dataset_trial2.parquet", compression="gzip")

print("Duplicated: ", df[df.duplicated(['title'])].size)
print(df.info())
print(df.head())

with open("not_processed.txt", "w") as f:
    for line in not_processed:
        f.write(line + "\n")
