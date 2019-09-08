import csv
import pandas as pd 
import numpy as np



def detect_outlier(data_1):
    outliers = []
    threshold=3
    mean_1 = np.mean(data_1)
    std_1 =np.std(data_1)
    
    
    for y in data_1:
        z_score= (y - mean_1)/std_1 
        
        if np.abs(z_score) > threshold:
            outliers.append(y)
    return outliers


a = pd.read_csv('bank.csv')

to_drop = ['DATE','TRANSACTION DETAILS','CHQ.NO.','VALUE DATE','BALANCE AMT','.',' DEPOSIT AMT ']

a.drop(columns = to_drop,inplace = True)

a.dropna(subset=[' withdrawal amount '], how='all', inplace = True)

grp = a.groupby('Account No')[' withdrawal amount '].apply(lambda x: x.tolist()).to_dict()

print(grp)
'''
for j in grp:

	for t in range(len(grp[j])):
		grp[j][t] = grp[j][t].strip()
		grp[j][t] = grp[j][t].replace(',',"")

	grp[j] = list(map(float,grp[j]))


for i in grp:
	o = detect_outlier(grp[i])
	print(i,o)
	print('\n')

for y in grp:
	if y=="'409000362497'":
		print(len(grp[y]))
'''


