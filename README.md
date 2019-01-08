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
√ cold start error. Handle exception in tenant enum?
√ make search box working in the DF
- dump enriched data to file
- restore dumped data
- fix order in which adds are scraped
- make default 2de hands restorable

### Medium requirements
- kijiji scrapper
- marktplaats scrapper
- denmark dba scrapper
- build docker container
- update README
- dev guide
√ remove main

#### Soft requirements
√ pagination
- progress bars for scrappers
- make filters
- filters in upload window
- busybox when uploading
- More verb Ui

#### Improvements
√ split index.tpl in partials
- make index.py stateless
- make search faster
