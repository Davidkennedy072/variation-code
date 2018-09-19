# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 11:09:46 2018
@author: David
Improvd pyanalyzereplication.py aimd at variation analysis
"""
import scipy.io as sio
import numpy as np
import os 
import matplotlib.pyplot as plt 
import pandas as pd

def variationanalysis(subjectinital, trialtype, path = None):
    '''
    subjectinital = [DY, KE]
    trialtype = [detection, fixPos, metamerNoise, onePair]
    '''
    filelist = []
    if path == None:
        path = 'D:/Summer2018research/replicationvariation'
    elif trialtype == 'replication':
        path = 'D:/Summer2018research/ReplicationData'
    else:
        os.chdir(path)
        
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.mat'):
                if trialtype+subjectinital in file:
                    filelist.append(file)
    if len(filelist) == 0:
        return 'No file found'
    timeSeq = [-0.01, 0 , 0.02, 0.04, 0.06, 0.08, 0.1]
    accuracyframe = pd.DataFrame(index = timeSeq)
    nDistfinal = pd.DataFrame(index = timeSeq)
    for file in filelist:
        filenumber = filelist.index(file)
        matdata = sio.loadmat(path +'/'+file)
        dataresponse = matdata['response'][0][0]
        responses = dataresponse['Data'][0][0]['Response']
        distrators = dataresponse['Data'][0][0]['numDistractors']
        blocksdata = dataresponse['currentBlock'][0][0] - 1 # 7
        responseframe = pd.DataFrame()
        for block in range(blocksdata):
            if responseframe.empty == True:
                responseframe = pd.DataFrame(responses[0][block], index = ['Block'+str(block)])
            else:
                responseframe = responseframe.append(pd.DataFrame(responses[0][block],
                                                              index = ['Block'+str(block)]))
        timeSeq = np.unique(dataresponse['fixationDisplayTimeSeq'][0])
        accuracy = []
        nDist = []
#        nDistavg = []
        for j in range(len(timeSeq)):
            blocks = np.where(dataresponse['fixationDisplayTimeSeq'][0] == timeSeq[j])[0]
            for b in range(len(blocks)): # 1 in the case of DY
                gt = dataresponse['imageObjectFlagSeq'][0][blocks[b]][0]
                resp = responseframe.iloc[blocks[b]]
                correct = np.equal(gt, resp)
                correct = np.mean(correct)
                accuracy.append(correct)
                QUESTdist = pd.Series(distrators[0][blocks[b]][0])
                finaldist = QUESTdist.iloc[-1]
                nDist.append(finaldist)
#                averagedist = QUESTdist.mean() 
#                nDistavg.append(averagedist)
        accuracyframe['Trial'+str(filenumber)] = pd.Series(accuracy, index = timeSeq)
        nDistfinal['Trial'+str(filenumber)] = pd.Series(nDist, index = timeSeq)
#        nDistaverage['Trial'+str(filenumber)] = pd.Series(nDistavg, index = timeSeq)
        accuracyframe['mean'] = np.array(accuracyframe).mean(axis=1)
        nDistfinal['mean'] = np.array(nDistfinal).mean(axis=1)
#        nDistaverage['mean'] = np.array(nDistaverage).mean(axis=1)
    return nDistfinal, timeSeq, accuracyframe # nDistaverage
