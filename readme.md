# Remedial for Databases for Cloud Computing

Steps to create a new instance:
1. Create an virtual environment and activate it
`py -m venv venv`
`venv/Scripts/Activate.bat`

2. Create a .gitignore file and add the virtual environment in it
`/venv`
`.env`
`./vscode`

3. Start a git repository and make an initial commit with the gitignore

4. Create a requirements.txt file to store dependencies for the project

5. Run the following commands to install the necessary dependencies:
`pip install Flask`
`pip freeze > requirements.txt` - To put the installed dependencies on the requirements file
`pip install flask-RESTful`
`pip install python-dotenv pymongo`

6. Create a .env file 

7. Create a db_config.py file

8. Create a main.py file

9. Establish the connection between the project and MongoDB
	a. Add necessary variables to .env file

10. Create the necessary requests on Insomnia: CRUD: POST, GET, PUT, DELETE

