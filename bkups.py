from app import app
from db import mysql
import pymysql
from flask import request, jsonify
import pickle

model = pickle.load(open('../pregnancy_model.pkl','rb'))

@app.route("/predict", methods = ["GET"])
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
        cursor.execute("select * from emp")
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



@app.route('/employee/<int:id>')
def getEmployeeById(id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from emp where id=%s", id)
        rows = cursor.fetchall()
        response = jsonify(rows)
        response.status_code = 200
        cursor.close()
        connection.close()
    except Exception as e:
        print(e)
        response = jsonify({"Employee": 'Employee not found on id'+id})
        response.status_code = 400
    finally:
        return response



@app.route('/addEmployee', methods=['POST'])
def addEmployee():
    try:
        _json = request.json
        print(_json)
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']
        if _name and _email and _phone and _address and request.method =='POST':
            sql = "INSERT INTO emp(name,email,phone,address)VALUES(%s, %s, %s, %s)"
            data = (_name, _email, _phone, _address)
            connection = mysql.connect()
            cursor = connection.cursor()
            cursor.execute(sql, data)
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
        cursor.execute("DELETE FROM emp WHERE id=%s",(id))
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
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _phone = _json['phone']
        _address = _json['address']
       
        if _name and _email and _phone and _address and request.method =='PUT':
            
            sql = ("UPDATE emp SET name=%s,email=%s,phone=%s,address=%s WHERE id=%s")
            data = (_name, _email, _phone, _address, id)
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
