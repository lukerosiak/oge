import os
import commands 

from django.core.management.base import BaseCommand, CommandError

from quarterback.oge.models import *


class Command(BaseCommand):
    help = 'Check index for new government officials.'

    def handle(self, *args, **options):
         
        done = False

        while not done:
            docs = Document.objects.exclude(url='').filter(triedocr='')
            if docs.count()>1:
                doc = docs[0]
                        
                doc.triedocr = 'Y'
                doc.save()
    
                        
                os.chdir('/dev/shm')
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
                

            else:
                done = True
