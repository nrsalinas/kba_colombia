#!/usr/bin/env python
# coding: utf-8

# # Candidate KBA delimitation of Colombian flora
# 
# ## Analysis iterations experiments
# 
# These experiments perform several Ackbar analyses to explore the effect of the number of search repetitions.

# In[1]:


import subprocess
from shutil import rmtree
from os import walk, mkdir


# In[3]:


analysis_folder = "/home/nelson/Data/kba/colombia/analyses/iterations/"
ackbar_bin = "/home/nelson/Data/kba/ackbar/ackbar.py"


# In[4]:


iters = [x for x in range(1000, 10001, 1000)]


# ## Analysis execution

# In[4]:


rmtree(analysis_folder)
mkdir(analysis_folder)


# In[5]:


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

focal_area_directory = 

pop_max_distance = 0

eps = 0.2
iters = {1}
max_kba = 50
congruency_factor = 12"""


# In[7]:


for i in iters:
    root = "{0}iterations_{1}".format(analysis_folder, str(i))
    tct = config_text.format(root, str(i))
    config_file = "{0}iterations_{1}.txt".format(analysis_folder, str(i))
    with open(config_file, "w") as fh:
        fh.write(tct)

    ackbargs = [ackbar_bin, config_file]
    out, err = None, None
    with subprocess.Popen(ackbargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pr:
        out, err = pr.communicate()
    if len(err) > 0:
        print(err.decode('utf8'))

