[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=8874501&assignment_repo_type=AssignmentRepo)
# Web Application Exercise

A little exercise to build a web application following an agile development process. See the [instructions](instructions.md) for more detail.
## Launching the App
Our app is using MongoDB Atlas as its database. So there's no need to setup local database.

To launch the app:

1. Setup a Python virtual environment
   ```
   python3 -m venv .venv
   ```
2. Activate the virtual environment
   ```
   .venv\Scripts\activate.bat
   ```
3. Install dependencies into the virtual environment
    ```
    pip3 install -r requirements.txt
    ```
4. Go to MainApp folder
   ```
   cd MainApp
   ```
5. Run the App
   ```
   set FLASK_APP=app.py
   set FLASK_ENV=development
   ```
   Then

   ```
   flask run
   ```
   or
   ```
   python3 -m flask run --host=127.0.0.1 --port=10000
   ```

## How to Login as an Admin
To use the App for the Admin version:
1. Go to Login Page
2. Login with username "admin" and password "admin"

## Product vision statement

To create a web application for amusement park riders, employees, and directors, so that riders can understand the layout of the park, rides that have soared in popularity, rides that need maintenance work, and adapt their amusement park schedules to accommodate their personal desires, as well as providing valuable feedback to employees and directors for ways to improve the park itself.

## User stories

[Link to user stories](https://github.com/software-students-fall2022/web-app-exercise-team-9-1/issues)

## Task boards

[Link to task boards](https://github.com/software-students-fall2022/web-app-exercise-team-9-1/projects?query=is%3Aopen)
