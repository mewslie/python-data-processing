# extract cluster id and cluster labels from unformatted text file
# save clusters to csv file

import pathlib
import pandas as pd

file_dir = r'C:\Users\pswon\Documents\Bgerm\pdfs'
file_name = "harrison2018_suppl_clusters.txt"
file_path = pathlib.Path(file_dir, file_name)

clusters = {}
with open(file_path) as f:
    this_members = []  # keep cluster members
    rubbish = {}  # keep other lines for debugging
    for line in f:
        this_cluster = line.strip()
        if line.startswith("C_") or line.startswith("desat"):  # end this cluster
            if this_cluster in clusters:
                clusters[this_cluster] = clusters[this_cluster] + this_members
            else:
                clusters[this_cluster] = this_members
            this_members = []  # clear members
        elif line.startswith("Bger_"):
            this_members.append(this_cluster)
        elif not line.startswith("Figure"):
            if this_cluster in rubbish:
                rubbish[this_cluster] += 1
            else:
                rubbish[this_cluster] = 1
print(clusters["C_611283"])  # check

# convert to pandas df
clusters_df = pd.DataFrame([(key, var) for (key, L) in clusters.items() for var in L], columns=['cluster', 'member'])
print(clusters_df.head(10))
clusters_df.to_csv(pathlib.Path(file_dir, "harrison2018_suppl_clusters.csv"), index=False)
