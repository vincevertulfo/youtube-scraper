from scraper import YoutubeVideoScraper
from config import YOUTUBE_API_KEY

API_KEY = YOUTUBE_API_KEY
KEYWORD = ''
EXPORT_PATH = ''
# MINUTES_LIMIT = 
# SEARCH_LIMIT = 

def main():

    yt = YoutubeVideoScraper(api_key=API_KEY, 
                            minutes_limit=MINUTES_LIMIT, 
                            search_limit=SEARCH_LIMIT)
    df = yt.search_word(search_word=KEYWORD, export_path=EXPORT_PATH)
    print(df)


if __name__ == '__main__':
    main()