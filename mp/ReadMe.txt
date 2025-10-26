SecureCheck - Email Breach Detection

SecureCheck is a sleek, modern web application designed to demonstrate the client-side detection of compromised email addresses against a local, massive list of known data breaches. It is built using python, plain JavaScript for the core logic and Tailwind CSS for a responsive, clean user interface.

Technology Stack

HTML5:Core structure.
Tailwind CSS (CDN): Utility-first CSS framework for rapid styling.
JavaScript (Vanilla): Logic for CSV parsing, data lookup, UI state management, and all animations.
Python : For handling backend For API
LeakCheck : Public API used for checking breached emails

Prerequisites

1. Python Libraries
   flask
   pandas
   requests
   io
   time
   json
   os
2. HTML & Tailwind CSS
3. JavaScript
5. Visual Studio

File structure

└── 📁mp
    └── 📁templates
        ├── api.html
    ├── about.html
    ├── app.py
    ├── breached_email.csv
    ├── contact.html
    ├── index.html
    ├── ReadMe.txt
    └── visualisation.html

To run the code

1. Execute the Backend Server

The application must be served via a local HTTP server to ensure proper functionality, particularly for loading the external CSV data file.

Locate the File: Navigate to the directory containing the application files, including index.html, breached_email.csv, and the main Python server script, typically named app.py.
Run the Server: Open your Command Prompt (Windows) or Terminal (macOS/Linux) and execute the server file using the Python interpreter:

	python app.py

The terminal will display output indicating that the server is running and listening on a specific address and port (e.g., http://127.0.0.1:5000/).

2. Access the Application

Once the server is running, the website can be accessed through your web browser.

Open the Link: In the same Command Prompt or Terminal window, you should see the local URL provided by the server (e.g., http://127.0.0.1:5000/).
Launch Browser: Click on the displayed localhost URL, or manually copy and paste it into the address bar of your preferred web browser.
This action will load the main landing page, index.html (SecureCheck - Email Breach Detection).

3. Application Usage

The application is now fully operational and ready for use.

Check for Breaches: Enter a valid email address into the input field on the home page.
View Results: Click the "Check Breaches" button to initiate the client-side data lookup and view the simulated breach results.

Note on CSV Loading: During the initial load, the application fetches the breached_email.csv file. You may observe a loading animation while the data is parsed and stored in memory before the first search is executed.

Contribution

This is a demo project, but feel free to fork it and adapt it for other client-side data lookup demonstrations!