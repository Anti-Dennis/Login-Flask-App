Multi-Factor Authentication & User Management System

Installing Required Dependencies to run the project
pip install flask argon2-cffi

How to initiate running the system
python app.py (or) execute app.py

File Overview

HTML files
- register.html: User Account Registration Form
- login.html: User Account Login Form
- otp.html: OTP Multifactor Authentication Form
- index.html: Main Page/ Welcome Page after logging in successfully

CSS And JavaScript
- main.css: Style definitions for the user forms and pages
- password-validation.js, pwcheck.js: Scripts for password strength validation and real-time password requirements checking

Python Files
- app.py: Main Application logic, including routes for registration, logging in, OTP Verification and other core necessary functions
- create.database.py : Script to set up the SQLite Database and users table.

What Languages are used in this system
Python, Flask, HTML, CSS, and JavaScript

Core Functions and features
## User Registration - Users can register with their username, email, and password via the register.html file
		     - Password Validation is implemented using JavaScript to ensure strong password compliance 

## User Login	     - Registered users can log in with their credentials via the login.html file

## OTP verification  - OTP Verification is implemented for secure access. Upon login, an OTP Code is being sent to user's registered email address

## Password Strength Validation - Real-time password strength feedback during registration using password-validation.js and pwcheck.js
				- Password requirements are shown to help and force users to create strong passwords

## Log out - A secure logout feature that clears the user session.

System Requirements

Python 3.x
Flask
SQLite3
SMTP Server Access (for OTP emails)
Web Browser for accessing HTML pages.


