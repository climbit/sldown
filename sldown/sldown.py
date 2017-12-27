#!/usr/bin/python
import argparse
import logging
import os
import csv
import requests


class sldown:
    urlList = []
    csvList = []
    
    def __init__(self):
        pass
    
    def getItemList(self):
        pass
    
    
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
    sld(args.input, args.type)
