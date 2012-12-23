import time
import os
import commands
import urllib2

from BeautifulSoup import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from django.core.management.base import BaseCommand, CommandError

from quarterback.oge.models import *


class Command(BaseCommand):
    help = 'Check index for new government officials.'

    def handle(self, *args, **options):
         
        #start selenium 
        os.system("java -jar /home/luke/apps/selenium-server-standalone-2.28.0.jar &")
        time.sleep(20)
        
        driver = webdriver.Remote("http://localhost:4444/wd/hub", webdriver.DesiredCapabilities.HTMLUNIT)        
        driver.get("http://www.oge.gov/Open-Government/Access-Records/Current-Executive-Branch-Nominations-and-Appointments/")

        select = Select(driver.find_element_by_tag_name("select"))        
        select.select_by_visible_text("100")

        self.nextpage(driver)

        #stop selenium
        urllib2.urlopen('http://localhost:4444/selenium-server/driver/?cmd=shutDownSeleniumServer')

        """Loop over all individuals to check for their records"""
        o = Official.objects.all().order_by('lastchecked')
        for oo in o:
            oo.check()


    def nextpage(self,driver):

        html = driver.page_source
        soup = BeautifulSoup(html)

        if soup.find('span',{'class': "numberOfRecords"}):
            print soup.find('span',{'class': "numberOfRecords"}).text

        for row in soup.tbody.findAll('tr'):
            cells = row.findAll('td')
            id = cells[0].a['href'].encode('utf')
            name = cells[0].text.encode('utf')
            agency = cells[1].text.encode('utf')
            position = cells[2].text.encode('utf')
         
            o = Official(id=id)
            o.name = name
            o.agency = agency
            o.position = position
            o.save()


        links = driver.find_elements_by_id('ctl00_ctl00_MiddleCPH_CenterContentCPH_next')
        if links and links[0].get_attribute('class')==u'next':
            links[0].click()
            self.nextpage(driver)



