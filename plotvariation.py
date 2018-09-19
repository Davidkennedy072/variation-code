# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 11:26:44 2018
@author: David
import pyvariationanalysis
"""
import numpy as np
import pandas as pd
import scipy.optimize as opt
from pyvariationanalysis import variationanalysis
import matplotlib.pyplot as plt 

# Obtain data
subjectinital = 'KAE'
trialtype = 'fixPos'
path = 'D:/Summer2018research/replicationvariation'
bracketdata = variationanalysis(subjectinital,trialtype, path = path)
nDistfinal = bracketdata[0]
timeSeq = bracketdata[1]
delayLabel = []
for j in range(len(timeSeq)):
    delayLabel.append(1000*timeSeq[j])
delayLabel = delayLabel[1:]
averages = np.array(nDistfinal['mean'])[1:] # Data point averages 
# Build Guassian module 
def guassian(delay, a, b, c, d): # f(x) = a*exp(-(x-b)**2/c)+d. c = 2*sigma**2
    return a*np.exp(-(delay-b)**2/c) + d

# Standard Deviation: 
std = np.array(nDistfinal.loc[:, nDistfinal.columns != 'mean'].std(axis = 1))[1:]
# Fit Guassian
plt.figure()
mean = 50
sigma = 20
offset = np.average(np.array(nDistfinal['mean'])[1:])
init_vals = [3, mean, sigma, offset]
bound = ([-np.inf, 0, 10, -np.inf],[np.inf, 100, 200, np.inf]) # Default
#bound = ([-np.inf, -np.inf, -np.inf, -np.inf],[np.inf, np.inf, np.inf, np.inf]) # Overwrite
popt, pcov = opt.curve_fit(guassian, delayLabel, averages, p0=init_vals,
                                      bounds = bound, sigma = std)
plt.plot(delayLabel, averages, 'b', label = 'data')
x = np.arange(0, 100)
#x = delayLabel
y = guassian(x, popt[0], popt[1], popt[2], popt[3])
plt.plot(x, y, 'r', label = 'fit')
plt.fill_between(delayLabel, averages-std/2, averages+std/2 ,color = [1, 0, 0, 0.1])

singlepresentation = nDistfinal.loc[-0.01]['mean']
plt.plot(x, np.full(len(x),singlepresentation ), 'k', label = 'single presentation')
#plt.fill_between(x, np.full(len(x), singlepresentation) - nDistfinal.loc[-0.01].drop(labels = 'mean').std()/2,
#                 np.full(len(x), singlepresentation) + nDistfinal.loc[-0.01].drop(labels = 'mean')std()/2, 
#                 color = [0, 0, 0, 0.25])
plt.title('a: {:0.4f} b: {:0.4f} c:{:0.4f} d:{:0.4f}'.format(*popt))
plt.suptitle(subjectinital+trialtype)
plt.xlabel('delay')
plt.ylabel('# of distractors')
plt.xticks([x+10 for x in delayLabel])
plt.legend()
plt.show()