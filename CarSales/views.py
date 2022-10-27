from django.shortcuts import render, redirect
from django.apps import apps
import pymysql

from .forms import CarForm

def connection():
    s = 'localhost' #Your server(host) name 
    d = 'carsales' 
    u = 'root' #Your login user
    p = 'ztech@44' #Your login password
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn

def carslist(request):
    cars = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TblCars")
    for row in cursor.fetchall():
        cars.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
    conn.close()
    return render(request, 'carslist.html', {'cars':cars})
def addcar(request):
    if request.method == 'GET':
        return render(request, 'addcar.html', {'car':{}})
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data.get("id")
            name = form.cleaned_data.get("name")
            year = form.cleaned_data.get("year")
            price = form.cleaned_data.get("price")
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO TblCars (id, name, year, price) VALUES (%s, %s, %s, %s)", (id, name, year, price))
        conn.commit()
        conn.close()
        return redirect('carslist')
def updatecar(request, id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM TblCars WHERE id = %s", (id))
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1], "year": row[2], "price": row[3]})
        conn.close()
        return render(request, 'addcar.html', {'car':cr[0]})
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            name = str(form.cleaned_data.get("name"))
            year = int(form.cleaned_data.get("year"))
            price = float(form.cleaned_data.get("price"))
            cursor.execute("UPDATE TblCars SET name = %s, year = %s, price = %s WHERE id = %s", (name, year, price, id))
            conn.commit()
        conn.close()
        return redirect('carslist')

def deletecar(request, id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM TblCars WHERE id = %s", (id))
    conn.commit()
    conn.close()
    return redirect('carslist')