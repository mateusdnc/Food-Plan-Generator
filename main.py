from flask import Flask, render_template, jsonify,request
from service import *
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', patient_file=read_patient_file('bruno peres carvalho de moura'), patients=get_all_patients())


@app.route('/patient/<patient>')
def patient_table(patient):
    patient_file = read_patient_file(patient)
    # Convertendo DataFrame para uma lista de dicionários
    patient_data = patient_file.to_dict(orient='records')
    return jsonify(patient_data)


@app.route('/patient/<patient>/dietplan')
def diet_plan(patient):
    diet_type = request.args.get('dietType')
    diet_plan = generate_diet_plan(patient,diet_type)
    # Convertendo DataFrame para uma lista de dicionários
    diet_plan = diet_plan.to_dict(orient='records')
    return jsonify(diet_plan)


if __name__ == '__main__':
    app.run(debug=True)
