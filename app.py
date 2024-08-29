from flask import Flask, render_template, request
from pypmml import Model

app = Flask(__name__)

# Carregar o modelo PMML
model = Model.load('PMM_SVML.pmml')

# Valores de normalização para tenure e MonthlyCharges
min_values = {
    'tenure': 0,
    'MonthlyCharges': 18.3
}

max_values = {
    'tenure': 72,
    'MonthlyCharges': 119
}

def normalize(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Coletar e normalizar os dados
        data = {
            'gender_ajustado': int(request.form['gender_ajustado']),
            'Partner_ajustado': int(request.form['Partner_ajustado']),
            'tenure': normalize(float(request.form['tenure']),
                                min_values['tenure'],
                                max_values['tenure']),
            'MultipleLine_ajustado': int(request.form['MultipleLine_ajustado']),
            'InternetServ_ajustado': int(request.form['InternetServ_ajustado']),
            'OnlineSecurity_ajustado': int(request.form['OnlineSecurity_ajustado']),
            'OnlineBackup_ajustado': int(request.form['OnlineBackup_ajustado']),
            'DeviceProtection_ajustado': int(request.form['DeviceProtection_ajustado']),
            'TechSupport_ajustado': int(request.form['TechSupport_ajustado']),
            'StreamingTV_ajustado': int(request.form['StreamingTV_ajustado']),
            'StreamingMovies_ajustado': int(request.form['StreamingMovies_ajustado']),
            'Contract_ajustado': int(request.form['Contract_ajustado']),
            'PaymentMethod_ajustado': int(request.form['PaymentMethod_ajustado']),
            'MonthlyCharges': normalize(float(request.form['MonthlyCharges']),
                                         min_values['MonthlyCharges'],
                                         max_values['MonthlyCharges'])
        }

        # Fazer a predição
        prediction = model.predict(data)
        churn = prediction.get('Churn', 'No')

        return render_template('form_result.html', churn=prediction)

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
