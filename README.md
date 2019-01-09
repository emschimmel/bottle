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
- √ cold start error. Handle exception in tenant enum?
- √ make search box working in the DF
- √ dump enriched data to file
- √ dump upload variables + state variables to file
- √ restore dumped data
- √ restore state from file
- √ fix order in which adds are scraped
- fix upload -> redirect to index without reload.
- √ fix 2dehands scrapper
- search box broke
- √ add config screen

### Medium requirements
- kijiji scrapper
- marktplaats scrapper
- denmark dba scrapper
- build docker container
- update README
- dev guide
- √ remove main
- modify original csv

#### Soft requirements
- √ pagination
- progress bars for scrappers
- make filters
- filters in upload window
- busybox when uploading
- More verb Ui
- √ handle config nicer
- √ selected item set? -> adjust page number
- drag tenant less through data_frame
- naming data_frame class

#### Improvements
- √ split index.tpl in partials
- make search faster
- make modify original csv faster
