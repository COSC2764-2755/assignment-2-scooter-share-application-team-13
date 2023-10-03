# Flask main
from flask import Flask, Blueprint, render_template, make_response, redirect, request
from records import Customer
from db import DatabaseConnector
import os, requests, json

site = Blueprint("site", __name__)

# Frontend Routes
@site.route("/", methods=['GET'])
def landing_view():
    return render_template("landing.html")

@site.route('/api/register', methods=['GET', 'POST'])
def register_view(): 
    return render_template("register.html")

@site.route('/api/login', methods=['GET', 'POST'])
def login_view(): 
    return render_template("login.html")

@site.route('/booking', methods=['GET', 'POST'])
def booking_view():
    return render_template("booking.html")