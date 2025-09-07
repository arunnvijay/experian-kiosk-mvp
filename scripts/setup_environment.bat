@echo off 
echo Setting up Python virtual environment... 
python -m venv venv 
call venv\Scripts\activate 
pip install -r requirements.txt 
python setup_mvp.py 
echo. 
echo Setup complete! Run 'start_server.bat' to start the application. 
pause 
