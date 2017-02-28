#!/bin/sh

simLoad=false
loadPdf=true
loadEpub=true

IFSTMP=${IFS}
IFS=,
counter=-1
while read it1 it2 it3 it4 it5 it6 it7 it8 it9 it10
do
    counter=$((counter+1))
    # Ignore first line (Header)
    if [ ${counter} -eq 0 ]
    then
        continue
    fi
    echo "${counter}. Fetch: ${it1}"
    
    # Download PDF
    mediaType=PDF
    if ${loadPdf}
    then
        url=$(echo ${it9} | sed 's/book/content\/pdf/g')
        echo "URL for PDF: ${url}"
        if ${simLoad}
        then
           eval wget -q --spider ${url}
           if [ $? != 0 ]
           then
               echo "URL is corrupted."
           else
               echo "URL is valid."
           fi
        else
            eval wget -q --show-progress ${url}
           if [ $? != 0 ]
           then
               echo "URL is corrupted, ${mediaType} download failed."
           else
               echo "Download sucessful"
           fi
        fi
    fi
    # Download EPUB
    mediaType=EPUB
    if ${loadEpub}
    then
        url=$(echo ${it9} | sed 's/book/content\/epub/g')
        echo "URL for EPUB: ${url}"
        if ${simLoad}
        then
           eval wget -q --spider ${url}
           if [ $? != 0 ]
           then
               echo "URL is corrupted."
           else
               echo "URL is valid."
           fi
        else
            eval wget -q --show-progress ${url}
           if [ $? != 0 ]
           then
               echo "URL is corrupted, ${mediaType} download failed."
           else
               echo "Download sucessful"
           fi
        fi
    fi
    echo
    echo
done < $1
IFS=IFSTMP
