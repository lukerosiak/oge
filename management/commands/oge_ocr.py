import os
import commands 
import datetime

import smtplib
from email.MIMEText import MIMEText

from django.core.management.base import BaseCommand, CommandError

from oge.models import *
from oge.config import *


class Command(BaseCommand):
    help = 'OCR recently downloaded PDFs and store their text.'

    def handle(self, *args, **options):
         
        os.chdir('/dev/shm')
         
        done = False

        while not done:
            docs = Document.objects.exclude(url='').filter(triedocr='')
            count = docs.count()
            if count==0:
                done = True
                break
                
            print "%s docs to OCR" % count
            doc = docs[0]            
            doc.triedocr = 'Y'
            doc.save()
    
                        
            filename = "oge_%s" % doc.id
            os.system('wget "http://www.oge.gov%s" -O %s.pdf' % (doc.url,filename))
                
            pages = commands.getstatusoutput('pdf2dsc %s.pdf /dev/stdout | grep %%Pages' % filename) 
            if len(pages)==2 and pages[1].startswith('%%Pages: '):
                doc.pages = pages[1].split(': ')[1] 
                
            os.system("docsplit text %s.pdf" % filename)
            os.system("rm %s.pdf" % filename)
                
            try:            
                fin = open('%s.txt' % filename,'r').read()
                os.system("rm %s.txt" %filename)
                            
                doc.text = fin
                print fin

            except:
                print 'ocr error'
                pass
                    
            doc.save()
                



        if EMAILS:
            """email new documents"""
            
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            docs = Document.objects.filter(firstfound__gte=yesterday)
            
            if len(docs):
            
                text = 'http://lukerosiak.info/oge<br/><br/>' + '<br/>-----------<br/>'.join([doc.__unicode__() + '<br/><br/>' + doc.text.replace('\n','<br/>') for doc in docs])
                text = text.encode('utf')
                
                msg = MIMEText(text,'html')
                msg['From'] = 'fecquarterback@lukerosiak.info'
                msg['To'] = ', '.join( emails )
                msg['Subject'] = '[Efiling:] %s New White House ethics letter(s)' % docs.count()
                s = smtplib.SMTP('localhost')
                s.sendmail('fecquarterback@lukerosiak.info', emails, msg.as_string())
            
    
