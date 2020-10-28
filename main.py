#!/usr/bin/env python
from flask import Flask, jsonify

app=Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
 

import mysql.connector

#mysql coneection
conn = mysql.connector.connect(database = "health_db", user = "root", password = "Rahul@1629", host = "localhost", port = "3306")
cur = conn.cursor()

'''
Instead of using three queries we can use this single query using join

select * from PatientDetails p inner join Carddetails c on
p.PatientID = c.PatientID inner join address a on 
p.PatientID = a.patientID where p.phone='1234567890';
'''

#flask app for fetching details of patient on the basis of phone number
@app.route('/res/<int:n>', methods=['GET'])
def res(n):
    
    global cur
    cur.execute("SELECT * from PatientDetails where Phone='%d'" %n)
    row = cur.fetchone()
    if not row:
        return jsonify("Invalid Input")
    #fetching patient details  
    PatientID = str(row[0])
    Phone= str(row[1])
    FirstName= str(row[2])
    LastName=str(row[3])
    Gender=str(row[4])
    DOB=str(row[5])
    ID=int('0'+PatientID)

    #fetching addressdetails of a particular patient
    cur.execute("SELECT * from Address where PatientID='%d'" %ID)
    add=cur.fetchone()
    Add_Det={}

    AddressType=str(add[6])
    Address=str(add[1])
    District=str(add[2])
    State=str(add[3])
    Pin=str(add[4])
    Country=str(add[5])
    Add_Det=[{'AddressType':AddressType,'Address':Address,'District':District,'State':State,'PinCode':Pin,'Country':Country}]
    
    #fetching card details of a particular patient
    cur.execute("SELECT * from CardDetails where PatientID='%d'" %ID)
    card=cur.fetchone()
    Card_Det={}
    
    CardNumber=str(card[1])
    CardDesc=str(card[2])
    crd=str(card[3])
    csd=str(card[4])
    Card_Det={'CardNumber':CardNumber,'CardDesc':CardDesc,'CardRegDate':crd,'CardStartDate':csd}

    #compiling data
    data={'Mobno':n,'CardDetails':Card_Det,'PatientDetails':[
    {'PatientID':PatientID,'Phone':Phone,'FirstName':FirstName,'LastName':LastName,'Gender':Gender,'DOB':DOB,'AddressDetails':Add_Det}]}

    #return jasonified data
    return jsonify(data)

#driver function
if __name__ == '__main__':
    app.run(debug=True)
