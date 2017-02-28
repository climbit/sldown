#!/usr/bin/python
import argparse
import logging
import os
import csv

parser = argparse.ArgumentParser(description='Download the books, which are specified in the csv file. The file have to be a CSV file downloaded at the link.springer.com page. This works only if access is granted.')
parser.add_argument('csvfil', type=str, metavar='FILE', help='CSV input file')
parser.add_argument('-t', '--ftype', dest='filetype', type=str, metavar='FILETYPE', help='Specify the file type epub or download. For multiple use a comma separated list.')

def sld(argCsvFile, argFiletype):
    if not os.path.exists(argCsvFile):
        logging.error('File does not exist: '+argCsvFile)
        return
    
    with open(argCsvFile, 'rb') as csvFile:
        #csvContent = csv.reader(csvFile, delimiter=',', quotechar='"')
        csvContent = csv.DictReader(csvFile, delimiter=',', quotechar='"')
        for row in csvContent:
            print row['Item Title'] + ", " + row['URL']
    
####################################################################################################
if __name__ == '__main__':
    args = parser.parse_args()
    sld(args.csvfil, args.filetype)
