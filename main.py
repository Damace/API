from db import mysql
from db import app
import pymysql
from flask import request, jsonify
import pickle
import json

model = pickle.load(open('../pregnancy_model.pkl','rb'))

@app.route('/')
def hello_world():
    return 'Alexs the Developer'


@app.route("/predict", methods = ["GET","POST"])
def predict():
    age = request.args.get('age')
    bmi = request.args.get('bmi')
    age_of_pregnancy = request.args.get('age_of_pregnancy')
    miscarriage = request.args.get('miscarriage')
    diabetes = request.args.get('diabetes')
    bp= request.args.get('bp')
    std = request.args.get('std')
    fp = request.args.get('fp')

    makeprediction = model.predict([[age,bmi,age_of_pregnancy,miscarriage,diabetes,bp,std,fp]])

    return jsonify({'prediction':int(makeprediction[0])})

@app.route("/employees")
def Employees():
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from pregnancyclient")
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        response = jsonify('Failed to fetch emp')
        response.status_code = 400
    finally:
        return response



@app.route('/employee/<int:Personid>')
def getEmployeeById(Personid):
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from pregnancyclient where Personid=%s", Personid)
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        response = jsonify({"Employee": 'Employee not found on Personid'+Personid})
        response.status_code = 400
    finally:
        return response



@app.route('/addEmployee', methods=['POST','GET'])
def addEmployee():
    try:
       
        firstname = request.args['firstname']
        lastname = request.args['lastname']
        age = request.args['age']
        gender = request.args['gender']
        phone_number = request.args['phone_number']
        address = request.args['address']
        email = request.args['email']
        password = request.args['password']

        if request.method =='GET' or request.method =='POST':

            sql = "INSERT INTO pregnancyclient(firstname,lastname,age,gender,phone_number,address,email,password)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (firstname, lastname, age, gender, phone_number, address, email, password)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql,data)
            connection.commit()
            response = jsonify('Employee has been added in db Successfully')
            response.status_code = 200
            cursor.close()
            connection.close()
        else:
            response = jsonify('Body not fouond')
            response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify('Failed to Add Employee')
        response.status_code = 400

    finally:
        return response

@app.route('/delete/<int:id>', methods=['DELETE'])
def deleteEmployeebyId(id):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pregnancyclient WHERE id=%s",(id))
        conn.commit()
        response = jsonify('Employee deleted successfully!')
        response.status_code = 200
        cursor.close()
        conn.close()
    except Exception as e:
        print(e)
        response = jsonify('Failed to Delete Employee')
        response.status_code = 400
    finally:
        return response


@app.route('/updateEmployee/<int:id>', methods=['PUT'])
def updateEmployee(id):
    try:
        firstname = request.args['firstname']
        lastname = request.args['lastname']
        age = request.args['age']
        gender = request.args['gender']
        phone_number = request.args['phone_number']
        address = request.args['address']
        email = request.args['email']
        password = request.args['password']

        if request.method =='PUT':
            sql = ("UPDATE pregnancyclient SET firstname=%s,lastname=%s,age=%s,gender=%s,phone_number=%s,address=%s,email=%s,password=%s WHERE id=%s")
            data = (firstname,lastname,age,gender,phone_number,address,email,password,id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            response = jsonify('Employee has been updated successfully!')
            response.status_code = 200
            cursor.close()
            conn.close()
        else:
            response = jsonify('Body not found for update')
            response.status_code = 400
    except Exception as e:
        print(e)
        response = jsonify('Faild to Update')
        response.status_code = 400
    finally:

        return response




@app.errorhandler(404)
def otherRoutes(error=None):
    response = jsonify({'message': 'No data found' })
    response.status_code = 404
    return response





if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
