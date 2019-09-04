from django.shortcuts import render
import pandas as pd

def fun_bank(search_topic):
    df=pd.read_csv(r"./buckets/Ranking1.csv", sep="|")
    df_temp=df[df['Bank name']==search_topic]

    buckets={'Account_and_Cheque':[],'Branch_Issues':[],'Customer_Service':[],'Hidden_Charges':[],'Investment_and_Loan':[],'name':search_topic}
    for bucket in buckets:
    #print(bucket)
        df_bucket=df_temp[df_temp['Category']==bucket]
    #print(len(df_bucket))
        ctr=1
        for index,row in df_bucket.iterrows():
            if len(buckets[bucket])>4:
                break
            buckets[bucket].append((ctr,row['Review'],row['Recency'],row['Customer name'],row['Place'],row['Issue type']))
            ctr+=1
    
    #buckets={'name':search_topic,'ambience':[ambience,amb_date], 'food':[food,food_date], 'staff':[staff,staff_date], 'amenities':[amenities,amen_date], 'cleanliness':[cleanliness,clean_date], 'facility':[facility,fac_date], 'price':[price, price_date]}
    return buckets	


def categories_banks(request, bank):
    context_bank = dict()
    context_bank = {
        'buc_banks' : fun_bank(str(bank))
        }
    return render(request, 'buckets/index_banks.html', context_bank)
