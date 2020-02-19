#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib as plt
import matplotlib.pyplot as plt

#%%
df1 = pd.read_csv('C:\\Users\Lenovo1\Desktop\scaffold\Caps_lel_pull_variants.filtered.csv', sep=";", decimal=',')
df2 = pd.read_csv('C:\\Users\Lenovo1\Desktop\scaffold\Caps_wt_pull_variants.filtere.csv', sep=";", decimal=',')
df = pd.merge(df1, df2, on=['position', 'scaffold'], how='outer')
df.to_excel('C:\\Users\\Lenovo1\\Desktop\\scaffold\\concat.xlsx', index=False)
#%%
df = pd.read_csv('C:\\Users\Lenovo1\Desktop\scaffold\concat.csv', sep=";", decimal=',')
df['rolling_wt'] = df.groupby('scaffold')['rate_wt'].rolling(10).mean().reset_index(0,drop=True)
df['rolling_lel'] = df.groupby('scaffold')['rate_lel'].rolling(10).mean().reset_index(0,drop=True)
res1 = df.assign(mean_lel= df["rolling_lel"].mean(), mean_wt= df["rolling_wt"].mean())

def calculate_chi2_lel(row):
    return (row['mean_lel'] - row['rolling_lel'])**2/row['mean_lel']
def calculate_chi2_wt(row):
    return (row['mean_wt'] - row['rolling_wt'])**2/row['mean_wt']    

res = res1.fillna(0)

res = res[res.rolling_lel != 0]
res = res[res.rolling_wt != 0]
res['chi2_lel'] = res.apply(calculate_chi2_lel, axis=1)
res['chi2_wt'] = res.apply(calculate_chi2_wt, axis=1)
res['chigeneral'] = res['chi2_lel'] + res['chi2_wt']

res.to_excel('C:\\Users\\Lenovo1\\Desktop\\scaffold\\chi2.10no_zero.xlsx', index=False)
#%%
df = pd.read_csv('C:\\Users\Lenovo1\Desktop\scaffold\chi2.10no_zer.csv', sep=";")
for idx, r2 in df.groupby('scaffold'):
    Count_Row = r2.shape[0]
    if Count_Row >= 10:     
        r2.to_csv('C:\\Users\\Lenovo1\\Desktop\\scaffold\\scaff\\scaffold_{}.csv'.format(idx), sep='\t', index=False)  
#%%
directory = 'C:\\Users\\Lenovo1\\Desktop\\scaffold\\scaff'
files = os.listdir(directory)
csv_only = filter(lambda x: x.endswith('csv'), files)

for i in csv_only:
    plt.title(i[13:25])
    df = pd.read_csv('C:\\Users\\Lenovo1\\Desktop\\scaffold\\scaff\\'+i, sep='\t', decimal=',')
    plt.style.use('bmh')
    plt.plot(df['position'], df['rolling_lel'], 'b.', df['position'], df['rolling_wt'], 'r.', df['position'], df['mean_lel'], '-', df['position'], df['mean_wt'], '-')
    plt.xlim (df['position'].min(), df['position'].max())
    plt.ylim (0, 100 )
    plt.xlabel('position')
    plt.ylabel('rolling mean')
    plt.legend(('rolling mean lel', 'rolling mean wt'),
           loc='upper right')

    plt.savefig('C:\\Users\\Lenovo1\\Desktop\\scaffold\\pic20\\{}.png'.format(i))
    plt.show()

