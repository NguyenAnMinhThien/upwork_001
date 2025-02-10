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

python -m venv venv

Depend on your OS

source venv/Scripts/activate

OR

source venv/bin/activate

pip install -r requirement.txt


+++ To allow to scrape only some pages from the browser, it is suggested not using proxy servers. This is for speed.

python main.py -pages 30 -start 0 -end 2 -proxy no

+++ To allow to scrape with a large number of pages, use proxy servers to mask our IP.

python main.py -con no -pages 1200  -proxy yes

++ To continue with the previous running

python main.py -pages 30 -proxy no -con yes

+++ Finally, to see help from this script:

python main.py -h
