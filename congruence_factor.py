#!/usr/bin/env python
# coding: utf-8

# # Candidate KBA delimitation of Colombian flora
# 
# ## Congruence factor experiments
# 
# These experiments perform several Ackbar analyses using different values of congruence factor.

# In[1]:


import subprocess
from shutil import rmtree
from os import walk, mkdir


# In[50]:


analysis_folder = "/home/nelson/Data/kba/colombia/analyses/congruency_factor/"
ackbar_bin = "/home/nelson/Data/kba/ackbar/ackbar.py"


# In[51]:


rmtree(analysis_folder)
mkdir(analysis_folder)


# In[52]:


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

cell_size = 0.2
offset_lat = 0.1
offset_lon = 0.1

pop_max_distance = 0

eps = 0.2
iters = 10000
max_kba = 50
congruency_factor = {1}"""


# In[53]:


congs = ["0", "02", "04", "06", "08", "10", "12", "14"] 


# In[54]:


for c in congs:
    root = "{0}congruency_{1}".format(analysis_folder, c)
    tct = config_text.format(root, c)
    config_file = "{0}congruency_{1}.txt".format(analysis_folder, c)
    with open(config_file, "w") as fh:
        fh.write(tct)

    ackbargs = [ackbar_bin, config_file]
    out, err = None, None
    with subprocess.Popen(ackbargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pr:
        out, err = pr.communicate()
    
    if len(err.decode('utf8')):
        print(err.decode('utf8'))

