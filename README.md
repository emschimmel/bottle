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
You can also start a bulk mode in by using `Enrich data` screen. When you use the `use whole file` set to on, it will try to scrape data it doesn't already have for the whole csv file. This process will take a lot of time!
When preparing for a demo, you might want to select a specific range of id's the system has using the `Enrich data` screen to configure the range and or amount the application should retrieve. 
The enrich data process uses a Python multiprocess pool and can only be interrupted by ctr+c twice. 
But be carefull. Since this proceess is also writing to disc, the `./config/dump-<tenant>.json` file might contain zero bites when killing the application when the new data is not written, than the scrapped data is gone. 
To increase the time between the file saves, you can increase the `save_interval`. This number means the amount of ads processed (not counting it's recommendations) before the process saves to file. Increasing reduces the io and makes the process faster, but when interupting, more data will be lost.

When you set the application to `use offline` in the `Config` screen, you will only see adds in the overview it has data for.
When you want to use the current state (for example for demo) and make sure it has that state when you start the application, you can save it in the `config` screen. This will adjust the `./config/state_config.ini` for you (or create it if it is not present). 
The `Default selected item` holds no guarantee that on application start this will be the default selected item because that id will have to be availible in the data frame and has to be in the search results if a Default search string is set.

Because we expect that the tool can be used without a connection to the internet the images are downloaded as a part of the scrapping process. 
Another advantage to this is that when the data is onhand, there won't be a dead link when the add is put offline in the meanwhile. 
Those images are stored under `./img/<tenant>`.

The `overview` has a list of all the ad id's the csv file contains (however, if the `offline mode` is active, it will show only those it has data for). 
The colomn next to it is the ad that is selected and the colomn to the right contains the recommendations for that item. 
For each block it also states when it got the data from the website.
If for example this data is too old and you are not in `offline mode`, you can forse it to reload it by clicking the `Reload` button at the selected ad. It will than try to get new data for the ad and all of it's recommenders.
You can also `Share` a selected ad by clicking the `Share` button of the selected add. It will than open the application with an url containing that specific ad id so you can share that url. 

If the ad if expired at the time it retrieved the data or the page returned a 404, an error is displayed at that ad.

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
- certifi (fix missing required certificate)
- pandas (the csv file is stored in a dataframe)
- requests (required by bs4 to make a http request)
- lxml (required by bs4 as parsing schema)

You can install them with `$pip3 install -r requirements.txt`. Pycharm will also pick them up from the requirements file.

### TODO

#### Hard requirements
- √ processes don't start/save anymore
- no image found bug

### Medium requirements
- index stateless?
- progress bars for scrappers?
- make filters
- √ enriched_data also in pandas?

### Imposible requirements
- denmark dba scrapper
