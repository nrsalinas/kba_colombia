#!/usr/bin/env python
# coding: utf-8

# ### Jacknife resampling
# Simple resampling analysis of the dataset to calculate the support of solution's score and ranking.

# In[1]:


import subprocess
from shutil import rmtree
from os import walk, mkdir


# In[2]:


analysis_folder = "/home/nelson/Data/kba/colombia/analyses/jacknife/"
ackbar_bin = "/home/nelson/Data/kba/ackbar/ackbar.py"
iterations = [x for x in range(0, 500)]


# In[22]:


rmtree(analysis_folder)
mkdir(analysis_folder)


# In[23]:


config_text = """
distribution_file = {0}
iucn_file = /home/nelson/Data/kba/colombia/amenazadas_categorias.csv

taxonomic_groups_file = 
taxonomic_assignments_file = /home/nelson/Data/kba/colombia/amenazadas_grupos.csv

kba_species_file = /home/nelson/Data/kba/colombia/Colombia_IBA_trigger_species.csv
kba_directory = /home/nelson/Dropbox/Humboldt/Postdoc/KBA_by_IUCN/Colombia_KBA
kba_index = SitRecID

outfile_root = {1}
overwrite_output = True

cell_size = 0.1
offset_lat = 0.033
offset_lon = 0.033

focal_area_directory = {2}

pop_max_distance = 1

eps = 0.2
iters = 10000
max_kba = 50
congruency_factor = 12"""


# In[24]:


occs = pd.read_csv("amenazadas_ocurrencias.csv")


# In[ ]:


for it in iterations:
    print("#######  Iteration {0}  ######".format(it))
    folder_name = "{0:0>3d}".format(it)
    mkdir(analysis_folder + folder_name)
    thindx = np.random.choice(occs.shape[0], int(occs.shape[0] * 0.7), replace=False)
    dist_file = analysis_folder + folder_name + "/occurences.csv"
    occs.loc[thindx].to_csv(dist_file, index=False)

    focus_master_dir = "/home/nelson/Data/kba/colombia/Colombia_regiones"
    for d, s, f in walk(focus_master_dir):
        for file in f:
            if file.endswith(".shp"):

                foc_dir = d#"/".join([d, file])
                reg = file.rstrip(".shp")
                #root = "{0}cell_size_{1}_offset_{2}_{3}".format(analysis_folder, c, o, reg)
                out_dir = analysis_folder + folder_name + "/" + reg
                tct = config_text.format(dist_file, out_dir, foc_dir)
                config_file = analysis_folder + folder_name + "/config.txt"

                with open(config_file, "w") as fh:
                    fh.write(tct)

                ackbargs = [ackbar_bin, config_file]
                #print(ackbargs)
                out, err = None, None

                with subprocess.Popen(ackbargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pr:
                    out, err = pr.communicate()
                
                if len(err) > 0:
                    print(err.decode('utf8'))

