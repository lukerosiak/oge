sudo apt-get install pdf2dsc

#install docsplit: http://documentcloud.github.io/docsplit/
sudo gem install docsplit
sudo apt-get install graphicsmagick
sudo apt-get install poppler-utils poppler-data
sudo apt-get install ghostscript
sudo apt-get install tesseract-ocr
sudo apt-get install pdftk

#selenium is a java-based browser automation tool
sudo apt-get install openjdk-7-jre-headless -y
#sudo apt-get install default-jre
cd ~
mkdir depends
cd depends
wget http://selenium-release.storage.googleapis.com/2.41/selenium-server-standalone-2.41.0.jar
#you will need to modify the path in config.py

#if you want to send emails, set the addresses in config.py
sudo apt-get install postfix
