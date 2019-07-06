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
__version__ = '2.0.1'
__date__ ='July 2019'
#################################################################################################################################################

import math, time, sys, getopt, os
try:
    import pcraster as pcr
except:
    print('Could not import pcraster, make sure it is installed including the python extensions.')
    print('GlabTop2-py uses pcraster version 4.2.1')
    print('See http://pcraster.geo.uu.nl/downloads/latest-release/')
    sys.exit()

import pandas as pd
import numpy as np
import configparser
from scipy.interpolate import griddata
from simpledbf import Dbf5

class GlabTop2():
    def __init__(self, cfgfile):
        
        # Read the configuration file
        self.config = configparser.RawConfigParser()
        self.config.read(cfgfile)
        
        #-Define missing values (demMV should be a scalar value)
        self.mv = False
        self.demMV = -9999.
        
        #-Input path and output path
        self.input_path = self.config.get('FOLDERS', 'input_path')
        self.results_path = self.config.get('FOLDERS', 'results_path')
        
        #-Read the RGI dbf as a pandas dataframe and add columns for dH, dH_dem, hmin, and Tau
        rgi = Dbf5(os.path.join(self.input_path, self.config.get('INPUT_FILES', 'rgiDBF')))
        rgi = rgi.to_dataframe()
        #-unique glacier ids
        self.uIDs = pd.unique(rgi['GLACID'])
        rgi.set_index('GLACID', inplace=True)
        rgi = rgi[['Area','Zmin','Zmax','Slope','Lmax']]
        rgi['dH'] = rgi['Zmax']-rgi['Zmin']
        rgi['dH_dem'] = np.nan
        rgi['hmin'] = np.nan
        rgi['Tau'] = np.nan
        self.rgi = rgi
        
        #-Read dem
        self.dem = pcr.readmap(os.path.join(self.input_path, self.config.get('INPUT_FILES', 'demMap')))
        self.dem = pcr.pcr2numpy(self.dem, self.demMV)
        #-Read GlacIDs
        self.glacID = pcr.readmap(os.path.join(self.input_path, self.config.get('INPUT_FILES', 'glacidMap')))
        self.glacID = pcr.pcr2numpy(self.glacID, self.mv)
        
        #-Parameters
        self.eIntervals = self.config.getint('PARAMETERS', 'eIntervals')
        self.rho = self.config.getfloat('PARAMETERS', 'rho')
        self.g = self.config.getfloat('PARAMETERS', 'g')
        self.n = self.config.getint('PARAMETERS', 'n')
        self.r = self.config.getfloat('PARAMETERS', 'r')
        self.f = self.config.getfloat('PARAMETERS', 'f')
        self.hga = self.config.getfloat('PARAMETERS', 'hga')
        
    
    #-find glacmask, marginal, inner and glacier adjecent cells for specific glacier ID
    def identifyCells(self, ID):
        #-Find the glacier cells
        mask = np.where(self.glacID==ID)
        #-Mask with true for glacier
        glacMask = np.ones(self.glacID.shape) * self.mv
        glacMask[mask] = True
        #-indices pairs of row,col where glacmask is true
        mask = np.argwhere(glacMask==True)
        #-empty array with missing values for margin cells
        mcells = np.copy(glacMask) * self.mv
        #-loop over each cell in the mask for which glacID is match and check if it has at least one surrounding non-glacier cell
        for m in mask:
            r = m[0]
            c = m[1]
            if glacMask[r+1,c+1] == self.mv:
                mcells[r,c] = True
            elif glacMask[r,c+1] == self.mv:
                mcells[r,c] = True
            elif glacMask[r-1,c+1] == self.mv:
                mcells[r,c] = True
            elif glacMask[r-1,c] == self.mv:
                mcells[r,c] = True
            elif glacMask[r-1,c-1] == self.mv:
                mcells[r,c] = True
            elif glacMask[r,c-1] == self.mv:
                mcells[r,c] = True
            elif glacMask[r+1,c-1] == self.mv:
                mcells[r,c] = True
            elif glacMask[r+1,c] == self.mv:
                mcells[r,c] = True
        #-Determine the glacier innercells
        innerCells = np.copy(glacMask) 
        mask = np.where(mcells==True)
        innerCells[mask] = self.mv
        return glacMask, mcells, innerCells
    
    #-function that returns elevation and slope values for glacier cells. It also returns the maximum elevation difference
    def assignDemSlope(self, glacmask):
        mask = np.where(glacmask==self.mv)
        #-copy of entire dem
        glacdem = np.copy(self.dem)
        #-calculate max and min dem values of selected glacier
        z = np.copy(glacdem)
        z[mask] = np.nan
        z = z.flatten()
        dH = np.nanmax(z) - np.nanmin(z)
        z = None; del z
        #-assign missing values where glacier is not true
        glacdem[mask] = self.demMV
        #-convert dem to pcraster map to calculate slope
        glacdem = pcr.numpy2pcr(pcr.Scalar, glacdem, self.demMV)
        glacSlope = pcr.slope(glacdem); #m = None; del m
        glacSlope = pcr.pcr2numpy(glacSlope, self.demMV)
        glacSlope = np.arctan(glacSlope) / math.pi * 180
        glacSlope[mask] = np.nan
        glacdem = pcr.pcr2numpy(glacdem, np.nan)
        return glacdem, glacSlope, dH
    
    #-calculate shear stress (kPa) using dH (m)
    def shearStress(self, dH):
        dH = dH/1000 #-convert to km
        if dH > 1600:
            Tau = 150
        else:
            Tau = 0.5 + (159.8 * dH) - (43.5 * dH**2) 
        #-cannot be smaller than 0.005
        Tau = max(Tau, 0.005)
        return Tau
    
    #-function that return glacier heights
    def glacHeights(self, glacmask, glacdem, glacSlope, innercells, hmin, tau):
        p = np.where(innercells==True)
        nrInnerCells = np.size(p,1)
        nrRandCells = int(math.ceil(self.r * nrInnerCells))
        #-mask where glacier is true
        glacTrue = np.where(glacmask==True)
        #-define the boundary rows and columns for sub-setting when the interpolation is done later on
        rmin = min(glacTrue[0])
        rmax = max(glacTrue[0])
        cmin = min(glacTrue[1])
        cmax = max(glacTrue[1])
    
        #-mask for innercells. Randomly points are selected from these indices
        innerTrue = np.argwhere(innercells==True)
        #-Create an empty array for the final heights of the particular glacier
        finalHeights = np.ones(glacmask.shape) * 0. #hga
        #-do-the interpolation n times
        for N in range(self.n):
            print('\tInterpolation run %d' %(N+1))
            # indices for innercells. Randomly points are selected from these indices
            indices = np.arange(nrInnerCells)
        
            #-Create array with missing values and fill with h calculated at randomly chosen locations
            glacHeightPoints = np.ones(glacmask.shape) * self.demMV
            for i in range(nrRandCells):
                #-sample a random index
                randPointIndex = int(np.random.choice(indices))
                #-row and columns in matrix
                r = innerTrue[randPointIndex][0]
                c = innerTrue[randPointIndex][1]
                #-start increasing window size until hmin is reached 
                w = 0
                flag = True
                while flag:
                    r_min = r - 1 - w
                    r_max = r + 1 + w
                    c_min = c - 1 - w
                    c_max = c + 1 + w
                    tempDem = glacdem[r_min:r_max, c_min:c_max].flatten()
                    dH = np.nanmax(tempDem) - np.nanmin(tempDem)
                    if dH>=hmin:
                        flag = False
                    else:
                        w+=1
                tempSlope = glacSlope[r_min:r_max, c_min:c_max].flatten()
                meanSlope = np.nanmean(tempSlope)
                #-calculate the ice thickness for the random point
                h = self.iceThickness(tau, meanSlope)
                #-assign the calculated glacier height to the gridcell
                glacHeightPoints[r,c] = h
                #-convert to list (for strange reasons np.delete doesn't work, so....)
                indices = indices.tolist()
                #-remove the sampled point to make sure it isn't sampled another time
                indices.remove(randPointIndex)
                #-convert back to np array
                indices = np.asarray(indices)
    
            #-sub-set of matrix to make interpolation quicker 
            gh = glacHeightPoints[rmin:rmax+1, cmin:cmax+1]
            glacHeightPoints = None; del glacHeightPoints
            #-shape and rows and columns
            shp = gh.shape
            rows = shp[0]
            cols = shp[1]
            #-create an array with 4 additional rows and 4 additional columns and fill those rows and columns with values of hga (elevation of adjecent cells)
            tempArray = np.ones((rows+4,cols+4)) * self.hga
            tempArray[2:2+rows,2:2+cols]=gh
            points = np.where(tempArray != self.demMV)
            xi = np.ones(tempArray.shape)
            xi = np.where(xi==1)
            h = griddata(points, tempArray[points], xi, method='cubic').reshape(tempArray.shape)
            h = np.maximum(0.,h)
            tempArray = None; gh = None; points = None; xi = None; del tempArray, gh, points, xi
            glacIntHeightPoints = np.ones(glacmask.shape) * 0.
            glacIntHeightPoints[rmin:rmax+1, cmin:cmax+1] = h[2:2+rows,2:2+cols]
            h = None; del h
            finalHeights = finalHeights + glacIntHeightPoints
            glacIntHeightPoints = None; del glacIntHeightPoints
            
        #-calculate average height over the n interpolation runs
        finalHeights = finalHeights / self.n
        finalHeights[np.where(glacmask==False)] = self.demMV
        return finalHeights
    
    #-calculate ice thickness at random point using average slope
    def iceThickness(self, tau, alpha):
        sinAlpha = math.sin(alpha / 180 * math.pi)
        h = tau*1000 / (self.f * self.rho * self.g * sinAlpha)
        return h
        
    def run(self):
        #-emtpy glacier height map that is filled with all the elevations when looping over the glacier IDs
        IceDepths = np.ones(self.glacID.shape) * self.demMV
        for gID in self.uIDs:
            #-obtain masks for glaciers, margin, adjecent and inner cells with True for ID of the specific glacier. Also number of inner cells are returned.
            [glacmask, mCells, innerCells] = self.identifyCells(gID)
            #-check if glacier is gridded. Some really small glaciers on the edge of the basin may not have been gridded, and should therefore be cancelled.
            s = np.size(np.where(glacmask==True),1)
            if s>0:
                #-assign dem and slope values to margin and inner cells (non-marginal) and calculate the maximum elevation difference (dH)
                [glacdem, glacSlope, dH] = self.assignDemSlope(glacmask)
                #-Calculate shear stress
                tau = self.shearStress(dH)
                #-Assign dH and shear stress to the rgi dataframe
                self.rgi.loc[self.rgi.index==gID, 'dH_dem'] = dH
                self.rgi.loc[self.rgi.index==gID, 'Tau'] = tau
                hmin = dH / self.eIntervals
                self.rgi.loc[self.rgi.index==gID, 'hmin'] = hmin
                 
                print('Processing glacier: %d with Tau: %.2f and hmin: %.2f' %(gID, tau, hmin))
                h = self.glacHeights(glacmask, glacdem, glacSlope, innerCells, hmin, tau)
                #h = glacHeights(glacmask, glacdem, glacSlope, innerCells, r, tau, hmin, hga, f, rho, g, n)
                IceDepths[np.where(self.glacID==gID)] = h[np.where(self.glacID==gID)]
            else:
                print('Glacier: %d is not gridded and will therefore not be processed!' %gID)
         
        #-Write map to pcraster file
        IceDepths = pcr.numpy2pcr(pcr.Scalar, IceDepths, self.demMV)
        pcr.report(IceDepths, os.path.join(self.results_path, self.config.get('OUTPUT_FILES', 'iceDepthMap')))
        #-Write csv file of the modified rgi
        self.rgi.to_csv(os.path.join(self.results_path, self.config.get('OUTPUT_FILES','csvRGI')))


def main(argv=None):
    
    cfgfile = None
    try:
        opts, args = getopt.getopt(argv, 'hi:')
    except getopt.GetoptError:
        print('python -m GlabTop2.main -i <config file>')
        sys.exit()
    else:
        for opt, arg in opts:
            if opt == '-h':
                print('python -m GlabTop2.main -i <config file>')
                sys.exit()
            elif opt in "-i":
                cfgfile = arg
    if cfgfile is None:
        print('python -m GlabTop2.main -i <config file>')
        sys.exit()
    
    tic = time.clock()
    print('\nGlabTop2-py is developed by Wilco Terink\n')
    print('Version 2.0.1\n')
    glabtop = GlabTop2(cfgfile)
    glabtop.run()

    toc = time.clock()
    
    print('\nGlabTop2-py finished in %.2f minutes' %((toc-tic)/60.))



if __name__ == '__main__':
    main(sys.argv[1:])
    
    