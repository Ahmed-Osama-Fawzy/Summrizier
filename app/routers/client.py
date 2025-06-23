from flask import render_template, request, redirect, url_for, flash
from app import app, db

@app.route('/ContactUs')
def ContactUs():
    return render_template('clientside/ContactUs.html', Title = "Contact Us")

@app.route('/AboutUs')
def AboutUs():
    return render_template('clientside/AboutUs.html', Title = "About Us")

@app.route('/Partners')
def Partners():
    return render_template('clientside/Partners.html', Title = "Partners")

@app.route('/FQAs')
def FQAs():
    return render_template('clientside/FQAs.html', Title = "FQAs")

@app.route('/Booking')
def Booking():
    return render_template('clientside/Booking.html', Title = "Booking")

@app.route('/Services')
def Services():
    return render_template('clientside/Services/AllServices.html', Title = "Services")

@app.route('/Kitchens')
def Kitchens():
    return render_template('clientside/Services/Kitchens.html', Title = "Kitchens")


@app.route('/Doors')
def Doors():
    return render_template('clientside/Services/Doors.html', Title = "Doors")

@app.route('/Shutters')
def Shutters():
    return render_template('clientside/Services/Shutters.html', Title = "Shutters")

@app.route('/Covers')
def Covers():
    return render_template('clientside/Services/Covers.html', Title = "Covers")

@app.route('/Windows')
def Windows():
    return render_template('clientside/Services/Windows.html', Title = "Windows")

@app.route('/Other')
def Other():
    return render_template('clientside/Services/Other.html', Title = "Other")