import os
import secrets
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from dss_main import MatchingOPTYPE

app = Flask(__name__)


@app.route("/")
def MatchResult():
    # benerin lokasi unit data
    AHP_data = pd.read_csv('static/AHP Dummy.csv').values.tolist()
    TOPSIS_data = np.asarray(pd.read_csv('static/new.csv').values.tolist())
    tes = MatchingOPTYPE(AHP_data, TOPSIS_data)
    tes.run()

    return jsonify(tes.hasilmatch)


@app.route("/operator_unit_rank")
def OperatorUnit():
    AHP_data = pd.read_csv('static/AHP Dummy.csv').values.tolist()
    TOPSIS_data = np.asarray(pd.read_csv('static/new.csv').values.tolist())
    tes = MatchingOPTYPE(AHP_data, TOPSIS_data)
    tes.run()

    return jsonify(tes.operator_unit)


if __name__ == '__main__':
    app.run(debug=True)
