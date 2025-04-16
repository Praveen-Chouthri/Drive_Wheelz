# Vehicle Rental Management System

This repository contains the code for a Vehicle Rental Management System, a web application developed as a project for a Database Management Systems (DBMS) course.

## Overview

The Vehicle Rental Management System aims to provide a user-friendly platform for individuals to browse, book, and manage vehicle rentals online. It offers a range of features to simplify the rental process for users and provides a backend for managing vehicle availability and rental records.

## Key Features

* **User Authentication:** Secure user registration and login functionality.
* **Vehicle Browse:** Ability to view a catalog of available vehicles, including cars, bikes, cycles, and trucks.
* **Availability Checking:** Users can check the availability of vehicles for specific date ranges.
* **Booking System:** Enables users to book their desired vehicles for selected periods.
* **User Profile Management:** Users can view and update their personal details.
* **Rental History:** Users can view their current and past rental records.
* **Rental Cancellation:** Functionality for users to cancel their existing rentals.
* **Receipt Generation:** Option for users to download rental receipts in PDF format.
* **FAQ Chatbot:** A simple chatbot to answer frequently asked questions.

## Technologies Used

* **Python:** The primary programming language used for the backend logic.
* **Flask:** A micro web framework for building the web application.
* **SQLAlchemy (Implicit):** Likely used as the ORM (Object-Relational Mapper) to interact with the database (based on the `create_engine` import).
* **ReportLab:** Used for generating PDF receipts.
* **Flask-Mail:** Integrated for sending booking confirmation emails.
* **QR Code Generator:** Used to generate QR codes for rental information.
* **dotenv:** For managing environment variables.

## Setup Instructions (Basic)

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You might need to create a `requirements.txt` file listing all the Python packages used, including Flask, SQLAlchemy, python-dotenv, Flask-Mail, reportlab, qrcode)*
3.  **Set up environment variables:**
    * Create a `.env` file in the project root.
    * Define the necessary environment variables, such as the database connection string (`DB_CONNECTION_STRING`), Flask secret key (`FLASK_SECRET_KEY`), and email configuration (mail server, port, username, password, default sender).
4.  **Database Configuration:**
    * Ensure you have a compatible database set up (e.g., MySQL, PostgreSQL).
    * Update the `DB_CONNECTION_STRING` in your `.env` file with your database credentials.
    * *(Note: You might need to include instructions on how to create the necessary database tables if that's part of your project demonstration.)*
5.  **Run the application:**
    ```bash
    python app.py
    ```

## Database

The application utilizes a relational database to store information about users, vehicles, and rental transactions. The `database.py` file contains the logic for interacting with the database.

## Purpose

This project was developed as a course requirement for a Database Management Systems (DBMS) course to demonstrate understanding of database design, implementation, and application development.

## Video Demonstration

A video demonstration showcasing the features and functionality of this Vehicle Rental Management System is available [Link to your YouTube video here].
