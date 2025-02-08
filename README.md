Hi, you can do this tutorial:
- Clone this repository 
- Create venv in new folder
- Run main.py
- Get output from output folder

These are the commands:
-
mkdir web_scraping

git clone https://github.com/NguyenAnMinhThien/upwork_001.git web_scraping

cd web_scraping

(go to the previous branch, because current branches I'm working on)

git reset --hard fe140f35874afd28d95054d8808899b6818d830c
 
python -m venv venv

Depend on your OS

source venv/Scripts/activate

OR

source venv/bin/activate

pip install -r requirement.txt

python main.py


