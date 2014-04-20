import datetime
import urllib2 
       
from BeautifulSoup import BeautifulSoup        

from django.db import models

from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField


        
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)        
        
class Official(models.Model):
    id = models.TextField(primary_key=True)
    name = models.TextField(max_length=1200)
    agency = models.TextField(max_length=1200)
    position = models.TextField(max_length=1200)
    lastchecked = models.DateTimeField()
    removed = models.CharField(max_length=1)

    def __unicode__(self):
        return "%s" % self.name 

    def check(self):

        existing = [(x.name,x.date) for x in self.document_set.all()]
        existing_urls = [x.url for x in self.document_set.all()]

        url = "http://www.oge.gov%s" % self.id
        html = urllib2.urlopen(url).read()
        
        if 'TKs Dog Training Season' in removeNonAscii(html):
            #this may be a 404--the official may have been deleted
            print self.id, self.name, 'appears to be deleted!'
            self.removed = 'Y'
            self.lastchecked = datetime.datetime.now()
            self.save()
            return
        
        soup = BeautifulSoup(html)
        
        tables = soup.findAll('table',{'class':"accessRecords inCart"})
        for table in tables:
            rows = table.tbody.findAll('tr')
            for row in rows:
                cells = row.findAll('td')
                name = row.th.text
                date = cells[0].text
                try:
                    date = datetime.datetime.strptime(date,'%m/%d/%Y').date()
                except:
                    print 'couldnt format date', date
                    date = datetime.date.today()
                if cells[1].a:
                    url = cells[1].a['href']
                else:
                    url = ''
                
                if ((name,date) not in existing and url=='') or url not in existing_urls:
                    d = self.document_set.create(name=name,url=url,date=date)
                    print 'creating %s %s %s' % (name, url, date)

        self.lastchecked = datetime.datetime.now()                    
        self.save()

                    
                    
    

class Document(models.Model):

    official = models.ForeignKey(Official)
    name = models.CharField(max_length=1200)
    url = models.CharField(max_length=1200,blank=True)
    date = models.DateField()
    firstfound = models.DateTimeField(auto_now_add=True, null=True)
    header = models.TextField(blank=True) #denormalize official stuff to help with search
    text = models.TextField(blank=True)
    pages = models.IntegerField(null=True)
    triedocr = models.CharField(max_length=1,blank=True)
    
    search_index = VectorField()

    objects = SearchManager(
        fields = ('header', 'text'),
        config = 'pg_catalog.english', # this is default
        search_field = 'search_index', # this is default
        auto_update_search_field = False
    )
    
    def __unicode__(self):
        return "%s | %s | %s" % (self.header, self.name, self.link()) 

    def setheader(self):
        return "%s | %s | %s" % (self.official.name, self.official.agency, self.official.position) 

    def save(self, *args, **kwargs):
        self.header = self.setheader()
        super(Document, self).save(*args, **kwargs)

    def official_name(self):
        return self.header.split(' | ')[0]
    def official_agency(self):
        return self.header.split(' | ')[1]
    def official_position(self):
        return self.header.split(' | ')[2]

    #def official_name(self):
    #    s = self.official.name
    #    if self.official.removed=='Y':
    #        s += ' [APPEARS TO HAVE BEEN REMOVED BY WH]'
    #    return s

    def link(self):
        if self.url and self.url!='':
            if self.triedocr=='Y':
                return '<a href="http://www.oge.gov%s">PDF</a> | <a href="/oge/%s/#%s">Text</a>' % (self.url, self.official_id, self.id)            
            else:
                return '<a href="http://www.oge.gov%s">PDF</a>' % self.url
        else:
            return '<a href="http://www.oge.gov/DisplayTemplates/201_Form/FilerDetail.aspx?id=%s">Download</a>' % self.official_id


