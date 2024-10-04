from flask import Flask, render_template, request, jsonify
from us_visa.constants import APP_HOST, APP_PORT
from us_visa.pipline.prediction_pipeline import USvisaData, USvisaClassifier
from us_visa.pipline.training_pipeline import TrainPipeline

app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["GET","POST"])
def predict():
    if request.method == "GET":
        return render_template("usvisa.html")
    if request.method == "POST":
        try:
            data = request.form
            print(data)
            usvisa_data = USvisaData(
                continent=data["continent"],
                education_of_employee=data["education_of_employee"],
                has_job_experience=data["has_job_experience"],
                requires_job_training=data["requires_job_training"],
                no_of_employees=data["no_of_employees"],
                region_of_employment=data["region_of_employment"],
                prevailing_wage=data["prevailing_wage"],
                unit_of_wage=data["unit_of_wage"],
                full_time_position=data["full_time_position"],
                company_age=data["company_age"],
            )

            usvisa_df = usvisa_data.get_usvisa_input_data_frame()
            model_predictor = USvisaClassifier()
            value = model_predictor.predict(dataframe=usvisa_df)[0]

            # Determine approval status
            status = "Visa Approved" if value == 1 else "Visa Not Approved"
            result = {"status": status}

            return render_template("usvisa.html", context = result)
        



        except Exception as e:
            print(e)
            return render_template("usvisa.html", error=str(e))
        

@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return "Training successful!"
    else:
        return "Training Unsuccessful!"

if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
