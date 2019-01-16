# Ui tool to visualize ad recommendations

### Start

The format of the csv files should be this order of fields: 
```ad_id,recommended_ad_id,rank,score```

There are 4 ways to load data into this tool.
- insert via a the form
- insert via the raw input form
- upload a csv file using the userinterface
- place a csv file manually in a specific directory

The forms to do this are under `Insert data` and are only visible when `Use offline` is disabled.
The fastest way to feed the data is to go for the manual approach when the application is not running. 
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

This tool relies on how the tenants website is made. If they change properties, the scrapper might start failing to find fields. The `./scrapper/enrich_data_<tenant>.py` files need to be adjusted if this happens.
Documentation can be found here: https://www.crummy.com/software/BeautifulSoup/bs4/doc/

### Extending

If you want to extend this tool with another tenant, you have to make a scrapper class and make it have a public function def `def start_for_id(ad_id, tenant):` (see examples of 2dehands/marktplaats/kijiji), import it in `./model/tenant_enum.py` and add it to the enumeration there.

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
- √ last page bug
- √ show if the add is expired
- √ also show the categories
- √ update button on page
- √ share a specific id
- add item manual (single and multi) (save the csv)
- √ combine insert + upload
- √ store insert preference in config

### Medium requirements
- build docker container
- modify original csv
- index stateless

#### Soft requirements
- progress bars for scrappers?
- make filters
- filters/ranges in upload window
- busybox when uploading
- More verb Ui
- search for string in title?
- enriched_data also in pandas?

#### Improvements
- make modify original csv faster

#### Maintenance
- categories marktplaats
- expired marktplaats
- categories kijiji
- expired kijiji

### Imposible requirements
- denmark dba scrapper
