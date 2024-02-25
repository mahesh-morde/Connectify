<h2> Connectify - Your Remote Contact Management Hub </h2>

Connectify is a Django-based web application that empowers you to manage your contacts seamlessly from anywhere. It offers a centralized and user-friendly platform to not only store contact details but also perform various operations for efficient contact interaction.

<h4>Key Features:</h4>

Comprehensive Contact Management: Create, Read, Update, and Delete (CRUD) contact information with ease.
Remote Accessibility: Access and manage your contacts from any device with internet access, offering flexibility and convenience.
Login Functionality: Secure your contact data with a robust login system that validates user credentials for authorized access.
SQLite Database: Leverages a lightweight and efficient database (SQLite) for reliable data storage.
Getting Started:

This guide outlines the steps to set up and run Connectify on your local machine.

<h4>Prerequisites:</h4>

Python installed on your machine.
pip (Python package installer) installed.
Installation:

<h4>Clone the Repository:</h4>
git clone https://mahesh-morde/Connectify.git
cd Connectify

<h4>Create a Virtual Environment (Optional but recommended):</h4>
python -m venv venv
source venv/bin/activate  # For MacOS/Linux
venv\Scripts\activate     # For Windows

<h4>Install Dependencies:</h4>
pip install -r requirements.txt

<h4>Apply Database Migrations:</h4>
python manage.py migrate

<h4>Create Superuser:</h4>
python manage.py createsuperuser

Follow the prompts to create a superuser account for initial administrative access.

Run the Development Server:
python manage.py runserver
Use code with caution.

Access the Application:

Open http://127.0.0.1:8000/ in your web browser to start using Connectify!

Further Information:
<h3>You can take a quick walkthrough of the project here --> https://youtu.be/R6wQ9r31Q9o</h3>
