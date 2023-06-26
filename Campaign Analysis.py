#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


with open('bank.csv', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    data = list(reader)

data = data[1:]
df = []
# Define the desired format (e.g., comma-separated values)
for row in data:
    output_format = row[0].split(',') 
    df.append(output_format)


# In[3]:


df = pd.DataFrame(df, columns=['age','job','marital','education','default','balance','housing','loan',
                                   'contact','day','month','duration','campaign','pdays','previous','poutcome','y'])


# In[4]:


df


# In[5]:


df.replace('unknown', pd.NA, inplace=True)


# In[6]:


df['y'].value_counts().plot(kind='pie', labels=['No', 'Yes'], autopct='%1.1f%%')

# axs[i].pie([no_count, yes_count], labels=['No', 'Yes'], autopct='%1.1f%%')

# Set the plot title and labels
plt.title('Class distribution')
plt.xlabel('Unique Values')
plt.ylabel('Count')

# Show the plot
plt.show()


# In[7]:


df.isnull().sum()


# In[8]:


df = df.drop(columns=['poutcome','contact'], axis=1)


# In[9]:


df.dropna(subset=['education','job'], inplace=True)


# In[10]:


df.shape


# In[11]:


df.head()


# In[12]:


features = df.iloc[:,:14]
outcome = df.iloc[:,14]


# ### Label Distribution

# In[13]:


df['y'].value_counts().plot(kind='pie', labels=['No', 'Yes'], autopct='%1.1f%%')

# axs[i].pie([no_count, yes_count], labels=['No', 'Yes'], autopct='%1.1f%%')

# Set the plot title and labels
plt.title('Class distribution')
plt.xlabel('Unique Values')
plt.ylabel('Count')

# Show the plot
plt.show()


# ### Hypothesis 1:    "Examining the impact of campaigns on different marital statuses"

# In[14]:


crosstb = pd.crosstab(features.marital,outcome)
ax = crosstb.plot(kind='bar', figsize=(10, 5), title='Time taken by Brands to resell')
ax.set_xticklabels(crosstb.index, rotation=0)
plt.show()


# ### Hypothesis 2: Impact of Campaign on educated people 

# In[15]:


group = df.groupby(['education','y']).agg({
    'y':'count'}).rename(columns={'y': 'value_count'}).reset_index()
print(group)


# In[16]:


education_categories = group['education'].unique()
fig, axs = plt.subplots(1, len(education_categories), figsize=(10, 5))

for i, edu_category in enumerate(education_categories):
    edu_data = group[group['education'] == edu_category]
    
    no_count = edu_data[edu_data['y'] == 'no']['value_count'].iloc[0]
    yes_count = edu_data[edu_data['y'] == 'yes']['value_count'].iloc[0]
    
    axs[i].set_title(edu_category)
    axs[i].pie([no_count, yes_count], labels=['No', 'Yes'], autopct='%1.1f%%')
    axs[i].axis('equal')

plt.tight_layout()
plt.show()


# In[17]:


data = df.groupby(['housing','loan','y']).agg({
    'y':'count'}).rename(columns={'y': 'value_count'}).reset_index()
Nhouse_Yloan = data[((data['housing'] == 'yes') & (data['loan'] == 'no') | 
                    (data['housing'] == 'no') & (data['loan'] == 'yes'))].groupby('y').agg({
    'value_count':'sum'}).reset_index()
Nhouse_Nloan = data[((data['housing'] == 'no') & (data['loan'] == 'no'))].drop(columns=['housing','loan'], axis=1)
Yhouse_Yloan = data[((data['housing'] == 'yes') & (data['loan'] == 'yes'))].drop(columns=['housing','loan'], axis=1)
result = pd.concat([Nhouse_Yloan, Nhouse_Nloan, Yhouse_Yloan], axis=0)
result['Label'] = ['House_or_loan', 'House_or_loan', 'None_of_it', 'None_of_it', 'House_and_loan', 'House_and_loan']


# In[18]:


# Pivot the dataframe to rearrange the data for plotting
pivoted_data = result.pivot(index='Label', columns='y', values='value_count')

# Plot the stacked bar chart
ax = pivoted_data.plot(kind='bar', stacked=True)

# Set the plot title and labels
plt.title('Stacked Bar Plot')
plt.xlabel('Label')
plt.ylabel('Value Count')

ax.set_xticklabels(ax.get_xticklabels(), rotation=0)

# Show the plot
plt.show()


# In[ ]:




