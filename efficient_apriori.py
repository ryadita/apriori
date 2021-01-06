#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install efficient-apriori


# In[1]:


from efficient_apriori import apriori
import pandas as pd


# In[2]:


df = pd.read_excel(r'E:\UNHAS\Skripsweet\Data\DataFatimah.xlsx', header = None)


# In[3]:


transactions = []
   
for i in range(0, len(df)):
    transactions.append([str(item) for item in df.values[i,:] if str(item)!='nan'])
    


# In[4]:


transactions


# In[8]:


itemsets, rules = apriori(transactions, min_support=0.04, min_confidence=0.95)
result = list(rules)


# Hubungan antar itemsets (Kiri > Kanan)

# In[9]:


rules_rhs = filter(lambda rule: len(rule.lhs) == 2 and len(rule.rhs) == 1, rules)
for rule in sorted(rules_rhs, key=lambda rule: rule.lift):
    print(rule) 


# In[10]:


rules


# In[61]:


itemsets #hasil setelah penyortiran


# In[ ]:





# In[ ]:




