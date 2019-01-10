### RUN

$python3 index.py

url: http://localhost:8084/main

https://www.kijiji.ca/v-view-details.html?adId=1369844148

http://marktplaats.nl/adId

https://www.2dehands.be/autos/renault/captur/renault-captur-1200-benzine-automaat-479618316.html

### Install

Extra pip packages needed:
- bottle
- bs4
- certify
- pandas
- requests
- lxml

### TODO

#### Hard requirements
- fix upload -> redirect to index without reload.
- search box broke

### Medium requirements
- kijiji scrapper
- marktplaats scrapper
- denmark dba scrapper
- build docker container
- update README
- dev guide
- modify original csv

#### Soft requirements
- progress bars for scrappers
- make filters
- filters in upload window
- busybox when uploading
- More verb Ui

#### Improvements
- make search faster
- make modify original csv faster
