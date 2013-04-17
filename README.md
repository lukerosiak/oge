Process White House ethics statements for presidential nominees from this web site: http://www.oge.gov/Open-Government/Access-Records/Current-Executive-Branch-Nominations-and-Appointments/

A Django app that uses Selenium to scrape an ASP.NET site and Docsplit to do some OCRing

By Luke Rosiak 

A working instance is at www.lukerosiak.info/oge/


To set up:

You need to either install and run Selenium Server, a Java app, or change it to driver.Firefox() in management/commands/ogr_scrape.py after installing Python bindings for Selenium. You also need to install Docsplit, from the makers of DocumentCloud.

It is also set up to bake the index to Amazon S3, so unless you remove that, you need to put your settings in aws_local.py and rename it to aws.py.

Also remove the quarterback. in the import statements, which is my personal namespacing.

TO RUN:

python manage.py syncdb

Daily via a cronjob:

python manage.py oge_scrape

python manage.py oge_ocr 

To view:

yourserver/oge
