from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)
model = pickle.load(open('pregnancy_model.pkl','rb'))


@app.route('/')
def home():
    return 'Welcome to my first Application Programming interface'

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










if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')