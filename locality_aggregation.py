#!/usr/bin/env python
# coding: utf-8

# # Candidate KBA delimitation of Colombian flora
# 
# ## Locality aggregation experiments
# 
# These experiments perform several Ackbar analyses using different thresholds to join close occurrences into a single population.

# In[1]:


import subprocess
from shutil import rmtree
from os import walk, mkdir


# In[3]:


analysis_folder = "/home/nelson/Data/kba/colombia/analyses/localities_aggregation/"
ackbar_bin = "/home/nelson/Data/kba/ackbar/ackbar.py"


# ### Analysis execution

# In[4]:


rmtree(analysis_folder)
mkdir(analysis_folder)


# In[12]:


config_text = """
distribution_file = /home/nelson/Data/kba/colombia/amenazadas_ocurrencias.csv
iucn_file = /home/nelson/Data/kba/colombia/amenazadas_categorias.csv

taxonomic_groups_file = 
taxonomic_assignments_file = /home/nelson/Data/kba/colombia/amenazadas_grupos.csv

kba_species_file = /home/nelson/Data/kba/colombia/Colombia_IBA_trigger_species.csv
kba_directory = /home/nelson/Dropbox/Humboldt/Postdoc/KBA_by_IUCN/Colombia_KBA
kba_index = SitRecID

outfile_root = {0}
overwrite_output = True

cell_size = {1}
offset_lat = 0
offset_lon = 0

#focal_area_directory = 

pop_max_distance = {2}

eps = 0.2
iters = 10000
max_kba = 50
congruency_factor = 12"""


# In[50]:


cesis = ["0.2", "0.5"]
locdists = range(0, 12, 2)


# In[13]:


for c in cesis:
    for p in locdists:
        root = "{0}cell_size_{1}_loc_dist_{2:02.0f}".format(analysis_folder, c, p)
        #print(root)
        tct = config_text.format(root, c, p)
        config_file = "{0}cell_size_{1}_loc_dist_{2:02.0f}.txt".format(analysis_folder, c, p)
        with open(config_file, "w") as fh:
            fh.write(tct)

        ackbargs = [ackbar_bin, config_file]
        out, err = None, None
        with subprocess.Popen(ackbargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pr:
            out, err = pr.communicate()

        if len(err):
            print(err.decode('utf8'))

