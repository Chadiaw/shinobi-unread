Script to log into shinobi.fr and delete all unread messages

**Requirements**
- Python 3.7 
- Windows + Chrome version 81 (use a different [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) otherwise)


#### [Install Python](https://www.python.org/downloads/release/python-377/)

#### Install selenium

```
pip install selenium
```

## Usage

Example: Stop at 10 pages (start at page 3)
```
$ python main.py username password 10 --start=3
```


#### Help
```
$ python main.py --help
usage: main.py [-h] [--start START] username password max

Delete unread messages on shinobi.fr

positional arguments:
  username       Username
  password       Password
  max            How many pages to go through (default 10)

optional arguments:
  -h, --help     show this help message and exit
  --start START  Specify a starting page


```
