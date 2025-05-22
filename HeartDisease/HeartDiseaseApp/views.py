from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
import pandas as pd

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def Predict(request):
    if request.method == 'GET':
       return render(request, 'Predict.html', {})


def PredictHeartCondition(request):
    if request.method == 'POST':
        age = request.POST.get('age', False)
        gender = request.POST.get('gender', False)
        cp = request.POST.get('cp', False)
        bps = request.POST.get('trestbps', False)
        chol = request.POST.get('chol', False)
        fbs = request.POST.get('fbs', False)
        ecg = request.POST.get('restecg', False)
        thalach = request.POST.get('thalach', False)
        exang = request.POST.get('exang', False)
        oldpeak = request.POST.get('oldpeak', False)
        slope = request.POST.get('slope', False)
        ca = request.POST.get('ca', False)
        thal = request.POST.get('thal', False)

        data = 'age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal\n'
        data+=age+","+gender+","+cp+","+bps+","+chol+","+fbs+","+ecg+","+thalach+","+exang+","+oldpeak+","+slope+","+ca+","+thal

        file = open('testdata.txt','w')
        file.write(data)
        file.close()

        train = pd.read_csv('dataset')
        X = train.values[:, 0:13] 
        Y = train.values[:, 13]
        #X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state = 0)

        cls = GaussianNB()
        cls.fit(X, Y)

        test = pd.read_csv('testdata.txt')
        test = test.values[:, 0:13]
        y_pred = cls.predict(test)

        result = ''
        print(y_pred)
        for i in range(len(test)):
            if str(y_pred[i]) == '0.0':
                result = str(test[i])+"<br/>Result =  No Heart Disease Detected"
            if str(y_pred[i]) == '1.0':
                result = str(test[i])+"<br/>Result =  Heart Disease Detected"
            
        context= {'data':result}
        return render(request, 'Result.html', context)  

        

def Signup(request):
    if request.method == 'POST':
      #user_ip = getClientIP(request)
      #reader = geoip2.database.Reader('C:/Python/PlantDisease/GeoLite2-City.mmdb')
      #response = reader.city('103.48.68.11')
      #print(user_ip)
      #print(response.location.latitude)
      #print(response.location.longitude)
      username = request.POST.get('username', False)
      password = request.POST.get('password', False)
      contact = request.POST.get('contact', False)
      email = request.POST.get('email', False)
      address = request.POST.get('address', False)
      
      db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'HeartDisease',charset='utf8')
      db_cursor = db_connection.cursor()
      student_sql_query = "INSERT INTO register(username,password,contact,email,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
      db_cursor.execute(student_sql_query)
      db_connection.commit()
      print(db_cursor.rowcount, "Record Inserted")
      if db_cursor.rowcount == 1:
       context= {'data':'Signup Process Completed'}
       return render(request, 'Register.html', context)
      else:
       context= {'data':'Error in signup process'}
       return render(request, 'Register.html', context)    
        
def UserLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        utype = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = '', database = 'HeartDisease',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM register")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    utype = 'success'
                    break
        if utype == 'success':
            file = open('session.txt','w')
            file.write(username)
            file.close()
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        if utype == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'Login.html', context)
    
