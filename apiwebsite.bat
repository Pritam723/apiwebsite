cd venv\Scripts
call activate.bat
cd..
cd..
cd apibackend
python app.py
celery -A app.celery worker --loglevel=debug
