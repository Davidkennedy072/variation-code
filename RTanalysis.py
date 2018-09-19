# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 14:17:54 2018
@author: David
pyvariationanalysis aimed at RT(reaction time) analysis
"""
import scipy.io as sio
import numpy as np
import os 
import matplotlib.pyplot as plt 
import pandas as pd

filelist = []
subjectinital = 'DY' 
trialtype = 'onePair' # [detection, fixPos, metamerNoise, onePair]
path = 'D:/Summer2018research/replicationvariation'
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.mat'):
            if trialtype+subjectinital in file:
                filelist.append(file)
                    
timeSeq = np.array([-0.01, 0, 0.02, 0.04, 0.06, 0.08, 0.1])
RTtime = pd.DataFrame(columns = ['block', 'mean', 'std']) 
for file in filelist:
    filenumber = filelist.index(file)
    matdata = sio.loadmat(path +'/'+file)
    dataresponse = matdata['response'][0][0]
    responses = dataresponse['Data'][0][0]['Response']
    RT = dataresponse['Data'][0][0]['RT'][0]
    displayT = dataresponse['Data'][0][0]['displayTime'][0]
    RTtime = pd.DataFrame(columns = ['block', 'mean', 'std']) 
    timeSeq = np.unique(dataresponse['fixationDisplayTimeSeq'][0])
    for j in range(len(timeSeq)):
            block = np.where(dataresponse['fixationDisplayTimeSeq'][0] == timeSeq[j])[0][0]
            RTtime.loc[block] = [block, np.mean(RT[block][0] - displayT[block][:, 1]),
                       np.std(RT[block][0] - displayT[block][:, 1])]
            RTtime.set_index('block')
            RTtime.sort_index(inplace = True)
plt.figure()
delayLabel = []
for j in range(len(timeSeq)):
    delayLabel.append(1000*timeSeq[j])
mean = RTtime['mean']
plt.plot(delayLabel, mean, 'b', label = 'mean')
plt.fill_between(delayLabel, mean-RTtime['std'], mean+RTtime['std'],color = [1, 0, 0, 0.1], label = 'std')
plt.title(trialtype+subjectinital+'_RT')
plt.xlabel('delay (msec)')
plt.ylabel('RT (seconds)')
plt.legend()
plt.show()

