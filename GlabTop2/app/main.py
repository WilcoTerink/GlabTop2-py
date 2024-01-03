# -*- coding: utf-8 -*-
#
# GlabTop2-py: GlabTop2 (Glacier bed Topography) model
#
# Copyright (C) 2018  Wilco Terink
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#-Authorship information-########################################################################################################################
__author__ = 'Wilco Terink'
__copyright__ = 'Wilco Terink'
__version__ = '2.1.0'
__date__ ='January 2024'
#################################################################################################################################################

import streamlit as st
import configparser
import os, sys, io
import time
import subprocess

st.set_page_config(layout="wide")

# Read config template
myConfig = configparser.RawConfigParser()
myConfig.read('config_template.cfg')

st.markdown("<h1 style='text-align: center; color: #6897bb;'>GlabTop2-py</h1>", unsafe_allow_html=True)

c1 = st.container()
e1 = st.empty()
with c1:
    col1, col2 = st.columns([0.3, 0.7])
    with col1:
        st.markdown("<h2 style='text-align: left; color: #6897bb;'>Settings</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: #6897bb;'>Working directory</h3>", unsafe_allow_html=True)
        st.write('The working directory that is set below is the main processing directory. This is a folder on your local hard drive. \
            It should contain all the three required input files. The output files of GlabTop2-py will be saved in this folder as well.')

        workdir = st.text_input('Set working directory in field below:', help='For example: c:/myFolder')
        if workdir:
            if os.path.exists(workdir):
                # Set input_path and results_path in cfg
                myConfig.set('FOLDERS', 'input_path', workdir)
                myConfig.set('FOLDERS', 'results_path', workdir)

                st.markdown("<h3 style='text-align: left; color: #6897bb;'>Input files</h3>", unsafe_allow_html=True)
                # Set the RGI
                rgi = st.file_uploader('Select .dbf of the Randolph Glacier Inventory (RGI)', type='.dbf')
                if rgi:
                    if os.path.isfile(os.path.join(workdir, rgi.name)):
                        myConfig.set('INPUT_FILES', 'rgiDBF', rgi.name)
                        # Set the DEM
                        dem = st.file_uploader('Select .map of high-resolution Digital Elevation Model (DEM)', type='.map')
                        if dem:
                            if os.path.isfile(os.path.join(workdir, dem.name)):
                                myConfig.set('INPUT_FILES', 'demMap', dem.name)
                                # Set the GlacID map
                                glacid = st.file_uploader('Select .map with glacier IDs', type='.map')
                                if glacid:
                                    if os.path.isfile(os.path.join(workdir, glacid.name)):
                                        myConfig.set('INPUT_FILES', 'glacidMap', glacid.name)

                                        # Other settings
                                        st.markdown("<h3 style='text-align: left; color: #6897bb;'>Parameters</h2>", unsafe_allow_html=True)
                                        # rho
                                        rho = st.number_input('rho [kg/m3]', value=900.00, format='%.2f', min_value=0.00, max_value=2000.00)
                                        myConfig.set('PARAMETERS', 'rho', rho)
                                        # g
                                        g = st.number_input('g [m/s2]', value=9.81, format='%.2f', min_value=0.00)
                                        myConfig.set('PARAMETERS', 'g', g)
                                        # number of model runs
                                        n = st.number_input('number of model runs', value=3, format='%g', min_value=1)
                                        myConfig.set('PARAMETERS', 'n', n)
                                        # fraction of random cells to pick (from inner glacier area cells)
                                        r = st.number_input('fraction of random cells to pick [-]', value=.30, format='%.2f', min_value=0.05, max_value=1.00)
                                        myConfig.set('PARAMETERS', 'r', r)
                                        # shape factor f
                                        f = st.number_input('shape factor [-]', value=.80, format='%.2f', min_value=0.05)
                                        myConfig.set('PARAMETERS', 'f', f)
                                        # nr of elevation intervals. hmin for each glacier is calculated by dividing dH/intervals
                                        eIntervals = st.number_input('number of elevation intervals', value=20, format='%g', min_value=1)
                                        myConfig.set('PARAMETERS', 'eIntervals', eIntervals)
                                        # ice depth at glacier adjecent cells
                                        hga = st.number_input('ice depth at glacier adjecent cells [m]', value=0.00, format='%.2f', min_value=0.00)
                                        myConfig.set('PARAMETERS', 'hga', hga)

                                        # RUN
                                        r = st.button('Run GlabTop2-py')
                                        if r:
                                            with st.spinner('Running GlabTop2-py. Processing status is displayed on the right.\
                                                One moment please...'):
                                                with open(os.path.join(workdir, 'myConfig.cfg'), 'w') as f:
                                                    myConfig.write(f)
                                                
                                                p = subprocess.Popen([f"{sys.executable}", "-u", "-m", "GlabTop2.main", "-i", f"{os.path.join(workdir, 'myConfig.cfg')}"],
                                                    stdout=subprocess.PIPE)
                                                # Display subprocess output in empty placeholder
                                                with e1:
                                                    col3, col4 = st.columns([0.3, 0.7])
                                                    with col4:
                                                        for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
                                                            st.text(line)
                                            e2 = st.empty()
                                            with e2:
                                                st.write('GlabTop2-py completed successfully')
                                                time.sleep(3)
                                                st.write('Shell output will be cleared shortly...')
                                                time.sleep(3)
                                            e1.empty()
                                            e2.empty()

                                    else:
                                        st.write('###### :red[Error: provided .map for glacier IDs does not exist in working directory]')
                            else:
                                st.write('###### :red[Error: provided .map for DEM does not exist in working directory]')
                    else:
                        st.write('###### :red[Error: provided .dbf does not exist in working directory]')
            else:
                st.write('###### :red[Error: provided workding directory does not exist on your pc]')

    with col2:
        st.text(f'version {__version__}')
        st.text('Copyright (C) 2018 Wilco Terink')

        st.image('images/franz_josef.jpg', width=400)#, use_column_width='always')

        st.markdown("<h2 style='text-align: left; color: #6897bb;'>About</h2>", unsafe_allow_html=True)
        st.write('GlabTop2-py enables you to calculates the ice-thickness distribution for all glaciers in your area of interest. This \
            app is entirely based on the GlabTop2 concepts described by [Frey et al. (2014)](https://tc.copernicus.org/articles/8/2313/2014/tc-8-2313-2014.pdf)') 

        st.write('This app uses the GlabTop2-py Python package as [Source Code](https://github.com/WilcoTerink/GlabTop2-py). \
        The documentation for this package can be found [here](https://glabtop2-py.readthedocs.io/en/latest/index.html#). \
        The documentation also describes details about the required input files, and the output files that this app generates. \
        Because this app runs in the cloud, no manual installation is required.')

        st.markdown("<h2 style='text-align: left; color: #6897bb;'>What does it do?</h2>", unsafe_allow_html=True)

        st.write('The app carries out some geo-processing steps in the background to make an estimation of the ice-thickness of each glacier grid-cell \
            in your area of interest. It generates two files which will be stored on your local drive:')
        st.markdown('- [PCRaster scalar map](https://pcraster.geo.uu.nl/pcraster/4.4.0/documentation/pcraster_manual/sphinx/secdatbase.html#formscalar) with ice depths for each grid cell (Figure 1)')
        st.markdown('- A csv-file with for each glacier (GLACID) some properties (Figure 2)')

        st.markdown("<h2 style='text-align: left; color: #6897bb;'>Input requirements</h2>", unsafe_allow_html=True) 

        st.write('GlabTop2 is executed by going through the steps in the left panel. You should have one folder on your hard drive \
            where the required input files are stored. The following input is required:')
        st.markdown('- A shapefile with the outlines of the glaciers within your area of interest. The [Randolph Glacier Inventory (RGI)](https://www.glims.org/RGI/) is a recommended source for this. Make sure the shapefile attribute table contains the columns GLACID, Area, Zmin, Zmax, Slope, and Lmax. GLACID should be unique for each record in the attribute table.')
        st.markdown('- A high-resolution DEM in [PCRaster scalar format](https://pcraster.geo.uu.nl/pcraster/4.4.0/documentation/pcraster_manual/sphinx/secdatbase.html#formscalar)')
        st.markdown('- A raster with gridded glacier outlines (of glaciers found in the provided shapefile). This map should have the same extent and spatial resolution of the DEM, and should be formatted as a [nominal PCRaster map](https://pcraster.geo.uu.nl/pcraster/4.4.0/documentation/pcraster_manual/sphinx/secdatbase.html#formnominal)')
        
        st.image('images/example_ice_depths.png', caption='Figure 1: raster output with ice-thickness.', width=600)
        st.image('images/example_csv_output.png', caption='Figure 2: csv-file with glacier properties.', width=600)