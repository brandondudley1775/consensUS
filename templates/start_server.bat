@echo off
set FLASK_APP=app_test.py
echo "Be aware, this web server is available to everyone on your LAN."
flask run --host=0.0.0.0 
