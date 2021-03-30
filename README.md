
# Background:

This youtube scraper takes a keyword and extracts the youtube URLs related to it. The data point it collects are:

| Column        | Description                                   |
| -------       | -----------                                   |
| video_id      | id of the Youtube video                       |
| video_url     | url of the Youtube video                      |
| published_at  | date when the video was published             |
| channel_id    | id of the channel that posted the video       |
| channel_title | name of the channel                           |
| title         | title of the video                            |
| view_count    | number of views of the Youtube video          |
| like_count    | number of likes of the Youtube video          |
| comment_count | number of comments of the Youtube video       |
| duration      | duration of the video                         |

# File Structure

```
PROJECT: youtube-scraper
|
│   .gitignore
│   README.md
│   requirements.txt
│
└───scraper
        main.py -> script to run to do the scraping
        merger.py -> script the merge the output CSV's and remove duplicate videos
        scraper.py -> contains the YoutubeVideoScraper class
        config.py -> this is where you'll put your YOUTUBE API KEY
```

# Setup
- Open a terminal and clone this repository 
- Once done, `cd` to the folder
- In the terminal, create a Python virtual environment using:

```
Windows
> python -m virtualenv .venv
```

- Activate the environment by typing in your terminal
```
Windows
> .venv\Scripts\activate.bat
```

- Install dependencies by typing in your terminal
```
> python -m pip install -r requirements.txt
```

# Usage

### Scraping 
---
1. cd to `scraper` folder
2. Input your API key in `config.py`
```
YOUTUBE_API_KEY = ''
```
3. Input the **word** that you want to search for in `main.py`, as well as the **export path**
```
from scraper import YoutubeVideoScraper
from config import YOUTUBE_API_KEY

API_KEY = YOUTUBE_API_KEY
KEYWORD = ''
EXPORT_PATH = ''
```
4. Open your terminal, run `python main.py`


### Merge
--- 
If you want to merge all the exported CSVs that you've scraped, you can run the **merge.py** file.

It consolidates everything, and remove videos that are duplicated from similar keywords or search word.

1. Just input the file path where you've exported the data
```
import pandas as pd 
import os 

FILE_PATH = ''
```

2. In your terminal, run `python merger.py`