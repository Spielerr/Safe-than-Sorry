from firebase import firebase
import firebase_admin
import pandas as pd
import json
import csv
import datetime
import requests
#import wget
from firebase_admin import credentials
from firebase_admin import storage


firebase = firebase.FirebaseApplication('https://aesthetic-petal-251606.firebaseio.com/')

result = firebase.get('',None)

# Fetch the service account key JSON file contents
cred = credentials.Certificate("credentials.json")

# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'aesthetic-petal-251606.appspot.com',
}, name='storage')

bucket = storage.bucket(app=app)
#0/0_0

#print(blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET'))


#wget.download(url,"img1.jpeg")

row = ['acc_no','relation','name','email_id','ph_no','password','photo']
with open('f5.csv','a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(row)
    for i in result:
    	a = []
    	
    	a.append(i)
    	for j in result[i]:
    		t = j.split('_')
    		b = []
    		if(t[0]=='Acquaintance Details'):
    			b.append(i)
    			b.append(result[i][j]['relation'])
    			b.append(result[i][j]['name'])
    			b.append('')
    			b.append(result[i][j]['ph_no'])
    			b.append('')
    			#print(t[1])
    			blob = bucket.blob(i + '/' + i + '_' + str(t[1]))
    			url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    			myfile = requests.get(url)

    			open('pics_firebase/' + i + '_' + str(t[1]) + '.jpeg', 'wb').write(myfile.content)
    			b.append('pics_firebase/' + i + '_' + str(t[1]) + '.jpeg')
    			writer.writerow(b)

    		else:
    			a.append('main')
    			a.append(result[i][j]['name'])
    			a.append(result[i][j]['email_id'])
    			a.append(result[i][j]['ph_no'])
    			a.append(result[i][j]['password'])

    			blob = bucket.blob(i + '/' + i + '_0')
    			url = blob.generate_signed_url(datetime.timedelta(seconds=300), method='GET')
    			myfile = requests.get(url)
    			open('pics_firebase/' + i + '_0' + '.jpeg', 'wb').write(myfile.content)
    			a.append('pics_firebase/' + i + '_0' + '.jpeg')
    			writer.writerow(a)
    			




#pd.read_json(json.dumps(result)).to_csv('f1.csv')
#for i in result:
#	print(i,result[i])
#print(result)