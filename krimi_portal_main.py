from flask import Flask, render_template, request
import tkinter
from tkinter import *
import pandas as pd
import numpy
from sklearn.metrics import r2_score
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
import time
import base64
from io import BytesIO

tmpfile = BytesIO()
df = pd.read_csv('prisoner.csv')
#Turkey
Jahr = df['Year']
mannernzahl = df['Male']
frauenzahl = df['Female']
#USA
dfusa = pd.read_csv('prisoneusa.csv')
JahrUSA = dfusa['Year']
mannernzahlusa = dfusa['Male']
frauenzahluusa = dfusa['Female']
#UK and Wales
dfuk = pd.read_csv('prisonerukandwales.csv')
JahrUK = dfuk['Year']
mannernzahluk=dfuk['Male']
frauenzahluk = dfuk['Female']
#Belgium
dfbelgium = pd.read_csv('prisonerbelgium.csv')
JahrBelgium = dfbelgium['Year']
mannernzahlbelgium = dfbelgium['Male']
frauenzahlbelgium = dfbelgium['Female']

#Creating Model for each country
mymodelmann = numpy.poly1d(numpy.polyfit(Jahr, mannernzahl, 3))
mymodelfrau = numpy.poly1d(numpy.polyfit(Jahr, frauenzahl, 3))

mymodelmannusa = numpy.poly1d(numpy.polyfit(JahrUSA, mannernzahlusa, 3))
mymodelfrauusa = numpy.poly1d(numpy.polyfit(JahrUSA, frauenzahluusa, 3))

mymodelmannuk = numpy.poly1d(numpy.polyfit(JahrUK, mannernzahluk, 3))
mymodelfrauuk = numpy.poly1d(numpy.polyfit(JahrUK, frauenzahluk, 3))

mymodelmannbelgium = numpy.poly1d(numpy.polyfit(JahrBelgium, mannernzahlbelgium, 3))
mymodelfraubelgium = numpy.poly1d(numpy.polyfit(JahrBelgium, frauenzahlbelgium, 3))

plt.plot(JahrUSA, mannernzahlusa, label="Männlich", color='red', marker='o', linestyle='dashed')
plt.plot(JahrUSA, frauenzahluusa, label="Weiblich", color='green', marker='o', linestyle='dashed')
plt.title('USA')
plt.xlabel('Jahr')
plt.ylabel('Zahl der Menschen')
plt.savefig('templates/png/usa.jpeg')
encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
time.sleep(2)

app = Flask(__name__,static_folder='templates/png')

@app.route('/')
def my_graph():
    return render_template('index.html')


@app.route('/graphs')
def my_form():
    return render_template('graph.html',name_of_country="Türkei")

@app.route('/', methods=['POST'])
def my_form_post():
    country = request.form['Country']
    year = int(request.form['year'])

    if country == 'TR':
        return render_template('index.html', valuefrau=str(int(mymodelfrau(year))),valuemann=str(int(mymodelmann(year))))
    elif country == 'USA':
        return render_template('index.html', valuefrau=str(int(mymodelfrauusa(year))),valuemann=str(int(mymodelmannusa(year))))
    elif country == 'UK':
        return render_template('index.html', valuefrau=str(int(mymodelfrauuk(year))),valuemann=str(int(mymodelmannuk(year))))
    elif country == 'BEL':
        return render_template('index.html', valuefrau=str(int(mymodelfraubelgium(year))),valuemann=str(int(mymodelmannbelgium(year))))



app.run(port=80)
