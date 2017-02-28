#!/usr/bin/python
import argparse
import logging
import os
import csv
import requests

parser = argparse.ArgumentParser(description='Download the books, which are specified in the csv file. The file have to be a CSV file downloaded at the link.springer.com page. This works only if access is granted.')
parser.add_argument('csvfil', type=str, metavar='FILE', help='CSV input file')
parser.add_argument('ftype',  type=str, metavar='FILETYPE', help='Specify the file type (pdf or epub) to download. For multiple use a comma separated list.')

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
                filnam = row['Item Title']+'.'+filtype
                logging.info('Downloading "'+row['Item Title']+'", '+filnam+', '+url)
#                logging.info(numCurBook+'/'+numOfBooks+' Downloading "'+row['Item Title']+'", '+filnam+', '+url)
                data = requests.get(url)
                if 'html' in data.headers['content-type']:
                    logging.info('It seems that you dont have access to this file.')
                    continue
                with open(filnam, 'w') as outfil:
                    outfil.write(data.content)
    
####################################################################################################
if __name__ == '__main__':
    args = parser.parse_args()
    sld(args.csvfil, args.ftype)
