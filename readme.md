cd --- change directory
cd .. ------ back to the main directory

cd project ---
cd flask_app
cd fast_api

pip install flask flask-cors mysql-connector-python

python -m uvicorn app:app --reload


pip install pyodbc -- for sql server connection 


python -c "import secrets; print(secrets.token_hex(32))"  --- secret key
pip install authlib --- for gmail login 