python -m venv venv_name
cd venv_name/scripts
activate
pip install -r requirements.txt
cd ../../indpro
uvicorn main:app --reload
http://127.0.0.1:8000/docs
