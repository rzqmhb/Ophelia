from flask import Flask, render_template, request
import numpy as np
app = Flask(__name__)

def transformasiBenefit(data):
    for i in range(len(data)):
        min = np.min(data[i])
        data[i] = (data[i]/min) * 100
    return data

def transformasiCost(data):
    for i in range(len(data)):
        min = np.min(data[i])
        data[i] = (min/data[i]) * 100
    return data

def pembobotan(data, weight = np.array([0.25,0.15,0.1,0.1,0.1,0.1,0.05,0.05,0.05,0.05])):
    weighted = []

    for i in data:
        weighted.append(np.round((i*weight), 4))

    return np.array(weighted).T

def penjumlahan(data):
    terjumlah = []
    for i in data:
        terjumlah.append(np.round(np.sum(i), 4))

    return np.array(terjumlah)

def perankingan(data):
    teranking = np.argsort((np.argsort(-data)))+1
    return teranking

default_data = [
        np.array([4,3,5,5,1,1,4,1,4,2]),
        np.array([4,3,1,1,3,1,1,1,1,2]),
        np.array([4,4,5,5,3,1,1,1,4,1]),
        np.array([4,2,1,1,2,1,4,1,4,2]),
        np.array([4,3,5,5,3,2,4,1,1,2]),
        np.array([4,4,1,1,5,1,4,1,4,2]),
        np.array([4,3,1,1,1,1,4,1,2,2]),
        np.array([3,3,5,5,5,1,3,1,3,3]),
        np.array([4,3,1,5,3,1,4,1,4,2]),
        np.array([4,3,1,1,2,1,1,1,4,2]),
        np.array([4,2,1,1,2,1,4,1,1,2]),
        np.array([4,2,5,5,3,3,4,1,1,2]),
        np.array([4,2,1,1,3,1,4,1,3,2]),
        np.array([4,5,5,5,1,2,4,1,5,2]),
        np.array([4,3,1,1,3,3,4,1,3,2]),
        np.array([4,4,1,1,5,1,1,1,3,3]),
        np.array([4,5,1,1,1,3,4,2,3,2]),
        np.array([4,4,1,1,3,1,4,2,4,2]),
        np.array([4,3,1,1,5,1,4,1,1,2]),
        np.array([4,4,1,1,3,4,4,1,5,2]),
    ]

@app.route("/")
def main():
    data = np.array(default_data)
    
    data_perKriteria = data.copy().T
    data_perKriteria[0:4] = transformasiBenefit(data_perKriteria[0:4])
    data_perKriteria[4:10] = transformasiCost(data_perKriteria[4:10])
    data_terbobot = pembobotan(data_perKriteria.T)
    data_terjumlah = penjumlahan(data_terbobot.T)
    data_ranking = perankingan(data_terjumlah)

    map = {
        "default" : data,
        "matrix" : data,
        "data_tertransformasi" : data_perKriteria.T,
        "data_terbobot" : data_terbobot.T,
        "data_terjumlah" : data_terjumlah,
        "data_ranking" : data_ranking,
    }
    return render_template('index.html', data=map)

@app.route("/cpi", methods=["POST"])
def cpi():
    default = np.array(default_data)

    data_perAlternatif = np.array([
        np.array([int(x) for x in request.form.getlist(f'A{i+1}[]')]) for i in range(20)
    ])

    data_perKriteria = data_perAlternatif.copy().T
    data_perKriteria[0:4] = transformasiBenefit(data_perKriteria[0:4])
    data_perKriteria[4:10] = transformasiCost(data_perKriteria[4:10])
    data_terbobot = pembobotan(data_perKriteria.T)
    data_terjumlah = penjumlahan(data_terbobot.T)
    data_ranking = perankingan(data_terjumlah)

    map = {
        "default" : default,
        "matrix" : data_perAlternatif,
        "data_tertransformasi" : data_perKriteria.T,
        "data_terbobot" : data_terbobot.T,
        "data_terjumlah" : data_terjumlah,
        "data_ranking" : data_ranking,
    }

    return render_template('index.html', data=map)

@app.route("/kalkulator/submit", methods=["POST"])
def kalkulatorSubmit():
    data_perAlternatif = np.array([
        np.array([int(x) for x in request.form.getlist(f'input[{i+1}][]')]) for i in range(int(request.form.get('alternatif')))
    ])
    jenis = np.array(request.form.getlist('jenis[]'))
    bobot = np.array(request.form.getlist('bobot[]'))
    bobot = np.array([float(x) for x in bobot])

    data_perKriteria = data_perAlternatif.copy().T
    benefit = []
    cost = []
    for i, x in enumerate(jenis):
        if(x == 'Benefit'):
            benefit.append(i)
            print(i)
        if(x == 'Cost'):
            cost.append(i)
            print(i)
    data_perKriteria[benefit] = transformasiBenefit(data_perKriteria[benefit])
    data_perKriteria[cost] = transformasiCost(data_perKriteria[cost])
    data_terbobot = pembobotan(data_perKriteria.T, weight=bobot)
    data_terjumlah = penjumlahan(data_terbobot.T)
    data_ranking = perankingan(data_terjumlah)

    map = {
        "matrix" : data_perAlternatif,
        "alternatif" : int(request.form.get('alternatif')),
        "kriteria" : int(request.form.get('kriteria')),
        "jenis" : jenis,
        "bobot" : bobot,
        "data_tertransformasi" : data_perKriteria.T,
        "data_terbobot" : data_terbobot.T,
        "data_terjumlah" : data_terjumlah,
        "data_ranking" : data_ranking,
    }

    return render_template('kalkulator.html', data=map)

@app.route("/teori")
def teori():
    return render_template('teori.html')

@app.route("/kalkulator")
def kalkulator():
    return render_template('kalkulator.html')

if __name__ == "__main__":
    app.run(debug=True)
