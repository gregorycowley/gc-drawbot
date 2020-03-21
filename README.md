pip freeze > requirements.txt
python3 -m venv .
source bin/activate 
pip install -r requirements.txt

rm -fr bin 
rm -fr include
rm -fr lib
rm -f pyvenv.cfg
