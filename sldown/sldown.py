#!/usr/bin/python
import argparse
import logging
import os
import io
import csv
import requests
import urllib


class sldown:
    def __init__(self, url):
        self.searchUrl = url
        self.itemList = []
        self.numItems = len(self.itemList)
        self.urlParsed = urllib.parse.urlparse(self.searchUrl)
        self.query = urllib.parse.parse_qs(self.urlParsed.query)
        self.yearStart = int(self.query['facet-start-year'][0])
        self.yearEnd = int(self.query['facet-end-year'][0])
    
    def DownloadItemList(self):
        pdf_base = 'https://link.springer.com/content/pdf/'
        epub_base = 'https://link.springer.com/download/epub/'
        ref_base = 'https://citation-needed.springer.com/v2/references/'
        ref_params = [{'flavour':'citation', 'format':'refman'}, {'flavour':'citation', 'format':'bibtex'}]
        for item in self.itemList:
            print(self.itemList.index(item)+1, '/', self.numItems)
            fn = item.replace('/', '_')
            response = requests.get(pdf_base+item+'.pdf')
            print(response.url)
            if response.ok and response.headers['Content-Type'] == 'application/pdf':
              with open(fn+'.pdf', 'wb') as fh:
                  fh.write(response.content)
            response = requests.get(epub_base+item+'.epub')
            print(response.url)
            if response.ok and response.headers['Content-Type'] == 'application/xml':
                with open(fn+'.epub', 'wb') as fh:
                    fh.write(response.content)
            for ref in ref_params:
                response = requests.get(ref_base+item+'_1', ref)
                print(response.url)
                if response.ok:
                    with open(fn+'.epub', 'wb') as fh:
                        fh.write(response.content)
            break
    
    def CreateItemList(self):
        fn_tmp = 'tmp.csv'
        for year in range(self.yearStart, self.yearEnd+1):
            self.query['facet-start-year'] = str(year)
            self.query['facet-end-year'] = str(year)
            csvUrl = self.urlParsed._replace(path=self.urlParsed.path+'/csv', query=urllib.parse.urlencode(self.query, doseq=True)).geturl()
            response = requests.get(csvUrl)
            if response.ok:
                with open(fn_tmp, "wb") as tmp:
                    tmp.write(response.content)
                # with io.StringIO(response.content.decode('utf-8')) as hcsv:
                with open(fn_tmp, "r", encoding='utf8') as hcsv:
                    csv_iter = csv.reader(hcsv)
                    for row in csv_iter:
                        if row[5].lower() == 'item doi':
                            continue
                        self.itemList.append(row[5])
        if os.path.isfile(fn_tmp):
            os.remove(fn_tmp)
        self.numItems = len(self.itemList)
    
    
    def sld(argCsvFile, argFiletype):
        # Set up logger
        logging.basicConfig(level=logging.INFO)
        
        # Check if file exist
        if not os.path.exists(argCsvFile):
            logging.error('File does not exist: '+argCsvFile)
            return
        
        # Read file type in
        filTypeList = argFiletype.replace(' ','').lower().split(',')
        
        # Read input file
        with open(argCsvFile, 'rb') as csvFile:
            csvContent = csv.DictReader(csvFile, delimiter=',', quotechar='"')
    #        numOfBooks = len(list(csvContent))
            numCurBook = 0
            for row in csvContent:
                numCurBook = numCurBook+1
                for filtype in filTypeList:
                    # Determine download url
                    if filtype == 'pdf':
                        url = row['URL'].replace('book', 'content/pdf')+'.pdf'
                    elif filtype == 'epub':
                        url = row['URL'].replace('book', 'download/epub')+'.epub'
                    else:
                        logging.error('Filytype not supported: '+filtype)
                        continue
                    
                    # Download file
                    # r = requests.get('url')
                    # fh = open('filename', "wb")
                    # fh.write(r.content)
                    # fh.close()
                    filnam = row['Item Title']+'.'+filtype
                    logging.info('Downloading "'+row['Item Title']+'", '+filnam+', '+url)
    #                logging.info(numCurBook+'/'+numOfBooks+' Downloading "'+row['Item Title']+'", '+filnam+', '+url)
                    data = requests.get(url)
                    if 'html' in data.headers['content-type']:
                        logging.info('It seems that you dont have access to this file.')
                        continue
                    with open(filnam, 'w') as outfil:
                        outfil.write(data.content)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download the books, which are specified in the csv file. The file have to be a CSV file downloaded at the link.springer.com page. This works only if access is granted.')
    parser.add_argument('input', type=str, metavar='INPUT', help='The input can ether be a csv file formated like the one you can download from springer link search result page or a url to a springer link search result page.')
    parser.add_argument('-t', '--type',  type=str, metavar='FILETYPE', help='Specify the file type to download. For multiple use a comma separated list. Accepted types are pdf and epub')
    args = parser.parse_args()
    new  = sldown(args.input)
    new.CreateItemList()
    new.DownloadItemList()