# Ui tool to visualize ad recommendations

### Start

The format of the csv files should be this order of fields: 
```ad_id,recommended_ad_id,rank,score```

There are 2 ways to load data into this tool.
You can either upload it using the userinterface to `upload` the csv file (only in online mode).

Or you use the manual approach when the application is not running. 
Fot this put the csv file in the directory `./config/original.csv` and modify the `./config/state_config.ini` file so the right tenant is set.
The name of the tenant should be one of the options mentioned in `./model/tenant_enum.py` since that name is used in the class switch to select the right scrapper.

To start the scrape process you have to run the application. When you click an item in the overview for which no scrapped data is available, the tool will automatically try to retrieve it and reload the page.
You can also start a bulk mode in the config screen under `Pre-load data into the application`.

When preparing for a demo, you might want to select a specific range of id's the system has using the `Pre-load data into the application` and after that shrink the csv file so it only contains the id's you have data for using `Modify original csv file`.
When you want to use the current state (for example for demo) and make sure it has that state when you start the application, you can save it in the config screen. This will adjust the `./config/state_config.ini` for you. 
The `Default selected item` holds no guarantee that on application start this will be the default selected item because that id will have to be availible in the data frame and has to be in the search results if a Default search string is set.

Because we expect that the tool can be used without a connection to the internet the images are downloaded as a part of the scrapping process. 
Another advantage to this is that when the data is onhand, there won't be a dead link when the add is put offline in the meanwhile. 
Those images are stored under `./img/<tenant>`.

### Maintenance

This tool relies on how the tenants website. If they change properties, the scrapper might start failing to find fields. The `./scrapper/enrich_data_<tenant>.py` files need to be adjusted if this happens.

### RUN

Make sure to use Python3 (Python2 is NOT supported). Use the index.py file as the main.
`$python3 index.py`

Open this url in any browser: http://localhost:8084/main

### Install

Extra pip packages needed:
- bottle (ui framework)
- bs4 (beatifulsoup, parse html from tenant)
- certify (fix missing required certificate)
- pandas (the csv file is stored in a dataframe)
- requests (required by bs4 to make a http request)
- lxml (required by bs4 as parsing schema)

### TODO

#### Hard requirements
- fix upload -> redirect to index without reload.
- search box broke

### Medium requirements
- kijiji scrapper https://www.kijiji.ca/v-view-details.html?adId=1369844148
- marktplaats scrapper http://marktplaats.nl/adId
- denmark dba scrapper
- build docker container
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
