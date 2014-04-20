Process White House ethics statements for presidential nominees from this web site: http://www.oge.gov/Open-Government/Access-Records/Current-Executive-Branch-Nominations-and-Appointments/

A Django app that uses Selenium to scrape a tricky ASP.NET site and Docsplit to OCR PDFs

By Luke Rosiak 

Working instance is at www.lukerosiak.info/oge/


To set up:

You need to either install and run Selenium Server, a Java app, or change it to driver.Firefox() in management/commands/ogr_scrape.py after installing Python bindings for Selenium. You also need to install Docsplit, from the makers of DocumentCloud.


TO RUN:

go thru setup.sh to install dependencies

pip install -r requirements.txt

change settings in config.py

python manage.py syncdb

then run sql/document.sql to set up full text search in postgres


Daily via a cronjob:

python manage.py oge_scrape

python manage.py oge_ocr 


To view:

127.0.0.1:8000/oge/
