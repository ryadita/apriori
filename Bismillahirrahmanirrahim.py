#!/usr/bin/env python
# coding: utf-8

# In[104]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
df = pd.read_excel(r'E:\UNHAS\Skripsweet\Data\DataFatimah.xlsx', header = None)


# Preprocessing Data

# In[78]:


transactions = []
   
for i in range(0, len(df)):
    transactions.append([str(item) for item in df.values[i,:] if str(item)!='nan'])
    


# In[79]:


transactions


# In[80]:


from itertools import chain
from collections import Counter, OrderedDict

set_t = [set(x) for x in transactions]
new_t = map(tuple, set_t)

pivot = Counter(new_t)
pivot = OrderedDict(pivot.most_common())

pivot


# In[81]:


def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
                
    C1.sort()
    return list(map(frozenset, C1))


# Fungsi untuk menghasilkan L1 dari C1

# In[82]:


def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt: ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData


# In[83]:


dataSet = transactions


# In[84]:


C1 = createC1(dataSet)
C1


# In[85]:


#D is a dataset in the setform.

D = list(map(set,dataSet))
D


# Iterasi 1

# In[86]:


L1,suppDat0 = scanD(D,C1,0.04)
L1


# Membuat Kandidat Item (Ck)
# #Fungsi aprioriGen () akan mengambil daftar frequent itemsets, Lk, dan ukuran itemsets, k, untuk menghasilkan Ck

# In[87]:


def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): 
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2: #if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j]) #set union
    return retList


# In[88]:


#give a dataset and a support number then generate a list of candidate itemsets
def apriori(dataSet, minSupport = 0.04):
    C1 = createC1(dataSet)
    D = list(map(set,dataSet))
    L1, supportData = scanD(D,C1,minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):#to find L2,L3,...
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D,Ck,minSupport)#get Lk from Ck
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


# In[89]:


L,suppData = apriori(dataSet, minSupport = 0.04)
L


# In[90]:


L[0] #l1


# In[91]:


C2 = aprioriGen(L[0],0)
C2


# In[92]:


L[1] #l2


# In[97]:


C3 = aprioriGen(L[1],1)
C3


# In[62]:


L[2] #l3


# In[64]:


C4 = aprioriGen(L[2],0)


# ## Proses Association Rules

# In[98]:


def generateRules(L, supportData, minConf=1): #supportData is a dict coming from scanD
    bigRuleList = []
    for i in range(1, len(L)):#only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 2):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


# In[99]:


#menghitung keyakinan aturan dan kemudian mencari tahu aturan mana yang memenuhi keyakinan minimum.
def calcConf(freqSet, H, supportData, brl, minConf=1):
    prunedH = [] #create new list to return
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
        if conf >= minConf: 
            print (freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


# In[100]:


#menghasilkan lebih banyak aturan asosiasi dari dataset awal kita. Ini membutuhkan frequent itemset dan H, yang merupakan daftar item yang mungkin berada di sisi kanan aturan.
def rulesFromConseq(freqSet, H, supportData, brl, minConf=1):
    m = len(H[0])
    if (len(freqSet) > (m + 1)): #try further merging
        Hmp1 = aprioriGen(H, m+1)#create Hm+1 new candidates
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):    #need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)


# In[101]:


L,suppData= apriori(dataSet,minSupport=0.04)
rules= generateRules(L,suppData, minConf=1)


# In[102]:


L


# In[103]:


suppData


# In[ ]:




