cd .apivenv\Scripts
call activate.bat
cd..
cd..
cd apibackend
flask --app app --debug run --host=0.0.0.0 -p 4001