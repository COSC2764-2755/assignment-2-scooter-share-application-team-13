# Flask main
from flask import Flask, Blueprint, render_template, make_response, redirect, request, jsonify, session, flash
from records import Customer
from db import DatabaseConnector
import os
import requests
import json

site = Blueprint("site", __name__)
# You can change the session type as needed
db = DatabaseConnector()

# Frontend Routes


@site.route("/", methods=['GET'])
def landing_view():
    return render_template("landing.html")


@site.route('/register', methods=["GET", "POST"])
def register_view():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "PUT":
        return "Success"


@site.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        return "Success"


@site.route('/booking', methods=['GET'])
def booking_view():
    # Fetch all scooters from the database
    all_scooters = db.get_scooters_from_db()
    # Filter the scooters to only include those with status 'available' (case-insensitive)
    available_scooters = [
        scooter for scooter in all_scooters if scooter.status.lower() == 'available']

    return render_template("booking.html", available_scooters=available_scooters)


@site.route('/dashboard', methods=['GET', 'POST'])
def dashboard_view():
    return render_template("dashboard.html")


@site.route('/engineer_dashboard', methods=['GET', 'POST'])
def engineer_dashboard_view():
    return render_template("engineer_dashboard.html")


@site.route('/report_issue')
def report_issue():
    return render_template('report_issue.html')


@site.route('/submit_issue', methods=['POST'])
def submit_issue():

    return redirect(url_for('dashboard'))
