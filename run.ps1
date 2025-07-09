# For Windows PowerShell
$env:FLASK_APP = "backend.app:create_app"
$env:FLASK_ENV = "development" 
flask run --host=0.0.0.0 --port=8000
