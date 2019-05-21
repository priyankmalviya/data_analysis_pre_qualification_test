#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
import random


# In[2]:


'''
This function is used to 
read the three files given
'''
def read_files():
    prices = pd.read_csv('prices.csv')
    audit = pd.read_csv('auditors.csv')
    stores = pd.read_json('stores.json')
    return prices,audit,stores


# In[62]:


def write_csv(df):
    df.to_csv('crsstab.csv', sep = '\t')
    


# In[3]:


'''
This function takes in as input the dataframe, oldname of the column 
and new name of the column and rename the old column to new column 
and returns the updated dataframe
'''
def rename_column(df,oldname,newname):
    df = df.rename(columns ={oldname: newname})
    return df


# In[4]:


'''
This function is used to join two tables.
It takes as input the two tables to be joined, method of join 
and the column id on which join is to be performed.
Returns the merged table
'''

def join_table(table1, table2, method, column_id):
    table = table1.merge(table2, how = method, on = column_id)
    return table


# In[8]:


'''
This function forms the cross tabulation table.
It takes in as input the table, list of values as index, columns which would be 
added and the values that the columns will hold.
Returns the cross tabulated table.
'''
def create_crss_tab(table,index_values,columns,values):
    crss_tab_df = table.pivot_table(index = index_values, columns = columns, values = values).reset_index()
    return crss_tab_df
    


# In[24]:


'''
This function randomly selects 'p' different products from the 
fully merged table and store them in a list and returns the list.
'''
def select_random_products(p):
    product = []
    for x in range(p):
        y =random.randint(0,1000)
        product.append(full_mrg.loc[(full_mrg['index'] == y)].iloc[0][7])
    return product


# In[29]:


'''
This function takes as input the dataframe
calculate the interquatile range of the prices per product 
and find the maximum and minimum price per product to identify the
outliers. Any outlier data lies outside the 3* Interquatile range.

Returns the dataframe with maximum and minimum prices within which
the prices should lie per product.
'''
def find_max_min_price(df):
    #finding the third quartile 
    iqr = df.groupby('UPC').quantile(0.75).drop(columns = ['Store ID'], axis = 1).reset_index()
    iqr = iqr.rename(columns = {'Price':'Third_quartile'})
    
    #finding the first quartile
    iqr1 = df.groupby('UPC').quantile(0.25).drop(columns = ['Store ID'], axis = 1).reset_index()
    iqr1 = iqr1.rename(columns = {'Price':'First_quartile'})
    
    #merging the first quartile and the third quatile data frame
    iqr = iqr.merge(iqr1, on = 'UPC')
    
    # finding the interquartile range
    iqr['IQR'] = iqr['Third_quartile'] - iqr['First_quartile']
    #3 times the interquartile range
    iqr['IQR'] = 3*iqr['IQR']
    
    #finding the maximum and minimum prices per product 
    iqr['Maximum_Price'] = iqr['Third_quartile'] + iqr['IQR']
    iqr['Minimum_Price'] = iqr['First_quartile'] - iqr['IQR']
    
    #dropping the columns not required
    iqr = iqr.drop(columns = ['Third_quartile','First_quartile','IQR'])
    return iqr


# In[46]:


'''
This function calculates in percent the occurence of 
each of the minimum outlier values.
Returns the result as a list
'''

def calc_percent():
    percent_prices = []
    sum_total = minimum_price_df.Price.value_counts().sum()
    for values in minimum_price_df.Price.value_counts():
        percent_prices.append(values/sum_total)
    return percent_prices


# In[35]:


'''
This function returns a list of all the unique values 
in a given column of the dataframe.

It takes as input the dataframe and the column whose unique
values are to be found.
''' 

def get_labels(df,field):
    labels = []
    for x in df[field]:
        if str(x) not in labels:
            x = str(x)
            labels.append(x)
    return labels


# In[42]:


'''
This function plot the pie chart given the labels and values.
'''

def pie_chart(labels,values):
    colors = ['r', 'g']
    plt.pie(values, labels=labels, startangle=50, autopct='%1.1f%%')
    plt.show()
    


# In[53]:


'''
This function calculates the mean price per region of previously selected random 
products and store it in a list.
Returns the list as a tuple.
'''
def mean_price_per_region():
    north_california = []
    kansas = []
    new_york = []
    texas = []
    for i in range (0,len(product)):
        nc_prc = full_mrg[(full_mrg['UPC'] == product[i]) & (full_mrg['Region'] == 'Northern California') & (full_mrg['Price'] != 1.99) ].agg('mean').Price
        kansas_prc = full_mrg[(full_mrg['UPC'] == product[i]) & (full_mrg['Region'] == 'Kansas') & (full_mrg['Price'] != 1.99) ].agg('mean').Price
        ny_prc = full_mrg[(full_mrg['UPC'] == product[i]) & (full_mrg['Region'] == 'New York') & (full_mrg['Price'] != 1.99)].agg('mean').Price
        texas_prc = full_mrg[(full_mrg['UPC'] == product[i]) & (full_mrg['Region'] == 'Texas') & (full_mrg['Price'] != 1.99)].agg('mean').Price
        nc_prc = nc_prc.item()
        kansas_prc = kansas_prc.item()
        ny_prc = ny_prc.item()
        texas_prc = texas_prc.item()
        north_california.append(nc_prc)
        kansas.append(kansas_prc)
        new_york.append(ny_prc)
        texas.append(texas_prc)
    nc = tuple(north_california)
    tx = tuple(texas)
    kn = tuple(kansas)
    ny = tuple(new_york)
    return nc,tx,kn,ny


# In[54]:


def bplt_price_per_region():
    n_groups = len(product)
    north_california = nc
    kansas = kn
    new_york = ny
    texas = tx

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.15
    opacity = 0.8

    rects1 = plt.bar(index, north_california, bar_width,
    alpha=opacity,
    color='b',
    label='north_california')

    rects2 = plt.bar(index + bar_width, kansas, bar_width,
    alpha=opacity,
    color='g',
    label='kansas')

    rects3 = plt.bar(index + 2*bar_width, new_york, bar_width,
    alpha=opacity,
    color='r',
    label='new_york')

    rects4 = plt.bar(index + 3*bar_width, texas, bar_width,
    alpha=opacity,
    color='y',
    label='texas')

    plt.xlabel('Products')
    plt.ylabel('Price')
    plt.title('Price by Region')
    plt.xticks(index + 3*bar_width, ('P1', 'P2', 'P3', 'P4','P5','P6','P7','P8','P9','P10','P11','P12','P13','P14','P15'))
    plt.legend()

    plt.tight_layout()
    plt.show()


# In[56]:


'''
This function calculates the mean price per store of previously selected random 
products and store it in a list.
Returns the list as a tuple.
'''

def mean_price_per_store():
    Walmart = []
    Trader_Joes = []
    Safeway = []
    Whole_Foods = []
    Wegmans = []

    for i in range (0,len(product)):
        walmrt_prc = full_mrg[(full_mrg['UPC'] == product[i]) & (full_mrg['Banner'] == 'Walmart') & (full_mrg['Price'] != 1.99)].agg('mean').Price
        trader_joes_prc = full_mrg[(full_mrg['UPC'] == product[i]) & (full_mrg['Banner'] == 'Trader Joes') & (full_mrg['Price'] != 1.99)].agg('mean').Price
        safeway_prc = full_mrg[(full_mrg['UPC'] == product[i]) & (full_mrg['Banner'] == 'Safeway') & (full_mrg['Price'] != 1.99)].agg('mean').Price
        wholefood_prc = full_mrg[(full_mrg['UPC'] == product[i]) & (full_mrg['Banner'] == 'Whole Foods') & (full_mrg['Price'] != 1.99)].agg('mean').Price
        wegmans_prc = full_mrg[(full_mrg['UPC'] == product[i]) & (full_mrg['Banner'] == 'Wegmans') & (full_mrg['Price'] != 1.99)].agg('mean').Price

        walmart_prc = walmrt_prc.item()
        trader_joes_prc = trader_joes_prc.item()
        safeway_prc = safeway_prc.item()
        wholefood_prc = wholefood_prc.item()
        wegmans_prc = wegmans_prc.item()

        Walmart.append(walmart_prc)
        Trader_Joes.append(trader_joes_prc)
        Safeway.append(safeway_prc)
        Whole_Foods.append(wholefood_prc)
        Wegmans.append(wegmans_prc)
    
    wlmt = tuple(Walmart)
    tjoes = tuple(Trader_Joes)
    safway = tuple(Safeway)
    wholefood = tuple(Whole_Foods)
    wgmns = tuple(Wegmans)
    
    return wlmt,tjoes,safway,wholefood,wgmns


# In[58]:


def bplt_price_per_store():
    # data to plot
    n_groups = len(product)
    walmart  = wlmt
    trader_joes = tjoes
    safeway = safway
    whole_food = wholefood
    wegmans = wgmns

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.15
    opacity = 0.8

    rects1 = plt.bar(index, walmart, bar_width,
    alpha=opacity,
    color='b',
    label='walmart')

    rects2 = plt.bar(index + bar_width, trader_joes, bar_width,
    alpha=opacity,
    color='g',
    label='trader_joes')

    rects3 = plt.bar(index + 2*bar_width, safeway, bar_width,
    alpha=opacity,
    color='r',
    label='safeway')

    rects4 = plt.bar(index + 3*bar_width, whole_food, bar_width,
    alpha=opacity,
    color='y',
    label='whole_food')

    rects5 = plt.bar(index + 4*bar_width, wegmans, bar_width,
    alpha=opacity,
    color='black',
    label='wegmans')

    plt.xlabel('Stores')
    plt.ylabel('Price')
    plt.title('Price by Stores')
    plt.xticks(index + 3*bar_width, ('P1', 'P2', 'P3', 'P4','P5','P6','P7','P8','P9','P10','P11','P12','P13','P14','P15'))
    plt.legend()

    plt.tight_layout()
    plt.show()


# In[ ]:





# In[63]:


if __name__ == '__main__':
    #calling the function to read the files
    prices,audit,stores = read_files()
    
    #calling the function to rename the column 'Region' in the audit table to 'Auditor Region'
    audit = rename_column(audit,'Region','Auditor Region')
    
    # calling the function to merge the tables stores and price
    str_prc_mrg = join_table(stores,prices,'left','Store ID')
    
    #calling the function to form the pivot table 
    crss_tab = create_crss_tab(str_prc_mrg,['Banner','UPC'],'Region','Price')
    
    #replacing nan values with hyphon as given in the example
    values = {'Kansas':'-','New York':'-','Northern California':'-','Texas':'-'}
    crss_tab = crss_tab.fillna(value = values)
    
    #writing the file
    write_csv(crss_tab)
    
    #joining all the three tables
    full_mrg = join_table(str_prc_mrg,audit,'inner','Auditor ID')
    
    #calling the function to get the maximum and minimum possible price of each product
    iqr_df = find_max_min_price(full_mrg)
    
    #calling the function to merge the table having min and max val to the fully merged table
    full_mrg = join_table(full_mrg, iqr_df,'inner','UPC')
    
    #separtating the outlier values in new df
    minimum_price_df = full_mrg[(full_mrg['Price'] < full_mrg['Minimum_Price']) ]
    #checking how many outlier data has been given by each auditor
    print(minimum_price_df.First.value_counts())
    
    #checking the different outlier values
    print(minimum_price_df.Price.value_counts())
    
    #checking how many times different auditors have given the price 1.99
    print(minimum_price_df[minimum_price_df['Price'] == 1.99].First.value_counts())
    
    #calling the function to calculate in percent each of the minimum outlier value
    percent_prices = calc_percent()
    
    #calling the function to get labels for the pie chart of minimum values
    labels = get_labels(minimum_price_df,'Price')
    
    #calling the function to plot the pie chart of the minimum values
    pie_chart(labels,percent_prices)
    
    #adding index to the fully merged table
    full_mrg = full_mrg.reset_index()
    
    #calling the function to select random products from the table
    product = select_random_products(15)
    
    #calling the function to get mean price per regions
    nc,tx,kn,ny = mean_price_per_region()
    
    #creating the bar plot of prices per region
    bplt_price_per_region()
    
    #calling the function to get mean price per stores
    wlmt,tjoes,safway,wholefood,wgmns = mean_price_per_store()
    
    bplt_price_per_store()
    
    


# In[ ]:




