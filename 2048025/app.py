from flask import Flask, request, render_template
from flask_cors import cross_origin
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pyodbc


#connection to database
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-H2PDBDI\MSSQLSERVER01;'
                      'Database=Clinic;'
                      'Trusted_Connection=yes;');

app = Flask(__name__)

@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")

@app.route("/datareport", methods = ["GET", "POST"])
@cross_origin()
def data():
    option = request.form['exampleRadios']
    if option == 'option1':
        data = pd.read_sql("SELECT * FROM INPatient", conn)
        result=data.to_html()
        sns.barplot(x='INPatient_No',y='INPatient_Age',data=data)
        plt.xlabel('Patient Id')
        plt.ylabel('Age')
        plt.title('INPatient ID\'s with their Age')
        plt.savefig('static/INPatient1.jpg')

        sns.kdeplot(data=data['INPatient_Age'])
        plt.xlabel('INPatient Age')
        plt.title('Age Seperation')
        plt.savefig('static/INPatient2.jpg')
        result=append_html(result,['INPatient1.jpg','INPatient2.jpg'])

        

    elif option == 'option2':
        data = pd.read_sql("SELECT * FROM Doctor", conn)
        
        result=data.to_html()
        sns.barplot(x='Doctor_Fname',y='Doctor_Consultation_Fee',data=data)
        plt.xlabel('Doctor Name')
        plt.ylabel('Consultation Fee')
        plt.title('Doctor with their Consultation Fee')
        plt.savefig('static/doc1.jpg')

        sns.barplot(x='Doctor_Fname',y='Doctor_Age',data=data)
        plt.xlabel('Doctor Name')
        plt.ylabel('Age')
        plt.title('Doctor with their Age')
        plt.savefig('static/doc2.png')
        result=append_html(result,['doc1.jpg','doc2.png'])
    elif option == 'option3':
        data = pd.read_sql("SELECT * FROM Bill", conn)
        result=data.to_html()
        sns.barplot(x='INPatient_No',y='Total_Cost',data=data)
        plt.xlabel('Patient Number')
        plt.ylabel('Total Cost')
        plt.title('Patient Number with their Total Cost')
        plt.savefig('static/bill1.jpg')

        sns.barplot(x='Bill_Date',y='Total_Cost',data=data)
        plt.xlabel('Date')
        plt.ylabel('Cost')
        plt.title('Bill Date with their total Cost')
        plt.savefig('static/bill2.png')
        result=append_html(result,['Bill1.jpg','Bill2.jpg'])


    elif option == 'option4':
        data = pd.read_sql("SELECT * FROM Checkup", conn)
        result=data.to_html()
        

    elif option == 'option5':
        data = pd.read_sql("SELECT * FROM OUTPatient", conn)
        result=data.to_html()
        sns.barplot(x='OUTPatient_No',y='OUTPatient_Age',data=data)
        plt.xlabel('Patient Id')
        plt.ylabel('Age')
        plt.title('OUTPatient ID\'s with their Age')
        plt.savefig('static/OUTPatient1.jpg')

        sns.kdeplot(data=data['OUTPatient_Age'])
        plt.xlabel('OUTPatient Age')
        plt.title('Age Seperation')
        plt.savefig('static/OUTPatient2.jpg')
        result=append_html(result,['OUTPatient1.jpg','OUTPatient2.jpg'])

    
    return result


def append_html(result,image_names):
    for i in image_names:
        result=result+" <img src=\"static/"+i+"\" width=\"600\" height=\"500\">"
    return result


if __name__ == "__main__":
    app.run(debug=True)
