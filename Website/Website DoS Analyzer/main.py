from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
from keras.models import load_model
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler


# Flask main library untuk API Flask
# Render Template untuk merender html file
# Request untuk menerima request yang diberikan oleh sistem


def split_x_y(df):
    x = df[df.columns[:4]]
    y = df[:-1]
    return x, y


def convert_to_pandas(csv_file):
    df = pd.read_csv(csv_file, sep=",")
    df_akhir = pd.DataFrame()
    # Feature Selection
    df_akhir["src"] = df["src"]
    df_akhir["dst"] = df["dst"]
    df_akhir["length"] = df["pktperflow"]
    df_akhir["protocol"] = df["Protocol"]
    df_akhir["label"] = df["label"]
    return df_akhir


def preprocessing_data(df):
    # Label Encoding
    le = LabelEncoder()
    le.fit(df["protocol"])
    df["protocol"] = le.transform(df["protocol"])

    le.fit(df["src"])
    df["src"] = le.transform(df["src"])

    le.fit(df["dst"])
    df["dst"] = le.transform(df["dst"])

    # Normalize
    norm_scaler = MinMaxScaler()
    df = pd.DataFrame(norm_scaler.fit_transform(df), columns=df.columns)
    return df


def lstm_module(lstm_model, df):
    x = df.to_numpy()
    x = np.reshape(x, (x.shape[0], x.shape[1], 1))

    y_pred = lstm_model.predict(x)
    y_pred_1 = [x[0] for x in y_pred]
    y_pred_2 = [x[1] for x in y_pred]
    df["lstm_result_1"] = y_pred_1
    df["lstm_result_2"] = y_pred_2

    return df


def naive_bayes_module(nb_model, df):
    df = df[["protocol", "lstm_result_1", "lstm_result_2"]]
    predict = nb_model.predict(df)
    df["label"] = predict
    df["label"] = df["label"].replace(0, "Normal")
    df["label"] = df["label"].replace(1, "Intrusi")
    return df


def main():
    app = Flask(__name__)

    @app.route("/", methods=["GET", "POST"])
    def index():
        if request.method == "GET":
            return render_template("form.html")
        elif request.method == "POST":
            return "Hi Data Form"

    @app.route("/form_handler", methods=["POST"])
    def form_handler():
        nama = request.form.get("name")
        gender = request.form.get("gender")
        return f"Hi {nama}, dengan jenis kelamin{gender}"

    @app.route("/upload_file", methods=["GET", "POST"])
    def upload_file():
        if request.method == "GET":
            return render_template("upload.html")
        elif request.method == "POST":
            lstm_model = load_model("model/lstm_slice.h5")
            nb_model = joblib.load("model/naive_bayes_final.pkl")
            data_csv = request.files.get("file")
            df = convert_to_pandas(data_csv)
            x, y = split_x_y(df)
            x_processed = preprocessing_data(x)
            x_lstm = lstm_module(lstm_model, x)
            prediction = naive_bayes_module(nb_model, x_lstm)
            df["Classification"] = prediction["label"]
            return render_template(
                "table.html",
                column_names=df.columns.values,
                row_data=list(df.values.tolist()),
                zip=zip,
            )

    @app.route("/nama")
    def test():
        # mendapatkan parameter dari url, karena sifatnya collections
        r = request.args.get("nama")
        return r

    app.run(host="localhost", port="5000")


if __name__ == "__main__":
    main()
