#!/usr/bin/env python
# coding: utf-8

# # Candidate KBA delimitation of Colombian flora
# 
# ## Cell size experiments
# 
# These experiments perform several Ackbar analyses using different resolutions of the geographic grid where KBA candidates will be estimated.
# 
# #### Memory usage
# 0.1 cell grid: 6.5 GB  
# 0.2 cell grid: 2 GB  
# 0.5cell grid: 0.3 GB

# In[1]:


import subprocess
from shutil import rmtree
from os import walk, mkdir


# In[3]:


analysis_folder = "/home/nelson/Data/kba/colombia/analyses/cell_size/"
ackbar_bin = "/home/nelson/Data/kba/ackbar/ackbar.py"


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

cell_size = {1}
offset_lat = {2}
offset_lon = {3}

focal_area_directory = {4}

pop_max_distance = 1 # 0 or 5?

eps = 0.2
iters = 10000
max_kba = 50
congruency_factor = 12"""


# In[6]:


cesis = ["0.2", "0.3", "0.4", "0.5"] # cell sizes


# In[7]:


for c in cesis:
    offs = list(map(lambda x: str(round(float(c) * x, 2)), [0, 0.333, 0.666]))
    
    for o in offs:
        root = "{0}cell_size_{1}_offset_{2}".format(analysis_folder, c, o)
        tct = config_text.format(root, c, o, o, "")
        config_file = "{0}cell_size_{1}_offset_{2}.txt".format(analysis_folder, c, o)
        with open(config_file, "w") as fh:
            fh.write(tct)

        ackbargs = [ackbar_bin, config_file]
        out, err = None, None
        with subprocess.Popen(ackbargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pr:
            out, err = pr.communicate()
        
        if len(err) > 0:
            print(err.decode('utf8'))


# In[8]:


focus_master_dir = "/home/nelson/Data/kba/colombia/Colombia_regiones"
cesis = ["0.1"]


# In[9]:


for c in cesis:
    offs = list(map(lambda x: str(round(float(c) * x, 3)), [0, 0.33333, 0.66666]))
    
    for o in offs:
        for d, s, f in walk(focus_master_dir):
            for file in f:
                if file.endswith(".shp"):
                    
                    foc_dir = d#"/".join([d, file])
                    reg = file.rstrip(".shp")
                    root = "{0}cell_size_{1}_offset_{2}_{3}".format(analysis_folder, c, o, reg)
                    tct = config_text.format(root, c, o, o, foc_dir)
                    config_file = "{0}cell_size_{1}_offset_{2}_{3}.txt".format(analysis_folder, c, o, reg)
                    
                    with open(config_file, "w") as fh:
                        fh.write(tct)

                    ackbargs = [ackbar_bin, config_file]
                    #print(ackbargs)
                    out, err = None, None
                    
                    with subprocess.Popen(ackbargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as pr:
                        out, err = pr.communicate()
                    if len(err) > 0:
                        print(err.decode('utf8'))

