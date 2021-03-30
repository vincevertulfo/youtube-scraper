from googleapiclient.discovery import build
import pandas as pd 


class YoutubeVideoScraper:
    '''
    Initializes the YoutubeVideoScraper object

    Parameters
    ----------
    api_key : str
        Youtube API Key
    minutes_limit : int (default : 90)
        Max length/duration of the videos you want to scrape
    search_limit : int (default : 200)
        Sets the limit of the number of videos returned. Limitation still depends on the quota set by the API
    '''

    def __init__(self, api_key, minutes_limit=90, search_limit=200):
        self.api_key = api_key
        self.list_of_dict = []
        self.minutes_limit = minutes_limit
        self.search_limit = search_limit
        try:
            self.yt = build('youtube', 'v3', developerKey=self.api_key)
        except:
            raise Exception("Authentication failed!")


    def search_word(self, search_word, export_path, max_results=50, order='viewCount'):
        '''
        Function that searches for the videos related to the keyword and exports to a CSV

        Parameters
        ----------
        search_word : str
            The keyword you want to search videos for
        export_path : str
            File path where you want to export the .csv file
        max_results : int (default : 50)
            Max number of results you want to get from each response. As per documentation, the max is already 50.
        order : str (default : 'viewCount') 
            Options: {'date', 'rating', 'relevance', 'title', 'viewCount', 'videCount'}
            The metric to be used to order the results in the API response. Default from the API is Relevance

        Return
        ----------
        output_df : DataFrame
            Dataframe containing the results of the scraping
        '''
        print(f"Scraping for {search_word}...")
        self.search_word = search_word

        response = self.yt.search().list(
            part='id, snippet',
            q=search_word,
            maxResults=max_results,
            type='video',
            order=order 
        ).execute()

        self.nextPageToken = response.get('nextPageToken')
        self.process_query_results(response=response, minutes_limit=self.minutes_limit)
        self.process_next_pages()

        output_df = pd.json_normalize(self.list_of_dict)
        output_df.to_csv(f"{export_path}/{search_word}.csv", index=False)

        print(f"Successfully exported {search_word} to "{export_path}"!")

        return output_df

    def process_query_results(self, response):
        '''
        Function that processes the API response, stores it to a dictionary, and appends to a list of dictionaries
        
        Parameters
        ------------
        response : dict
            JSON response from the API search() output
        ------------
        '''
        for item in response['items']:
            main_dict = {}
            video_url = 'https://www.youtube.com/watch?v={}'.format(item['id']['videoId'])

            response = self.yt.videos().list(
                part='contentDetails, statistics',
                id=item['id']['videoId']
            ).execute()

            for video_item in response['items']:
                duration = video_item['contentDetails'].get('duration', 0)
                video_duration = duration.lstrip('PT')
                hours, minutes = self.process_time_duration(duration)
                total_duration = (hours * 60)  + minutes

                if total_duration <= self.minutes_limit:
                    main_dict['video_id'] = item['id'].get('videoId',0)
                    main_dict['video_url'] = video_url
                    main_dict['hyperlink'] = '=HYPERLINK("{video_url}",)'.format(video_url=video_url)
                    main_dict['publishedAt'] = item['snippet'].get('publishedAt',0)
                    main_dict['channelId'] = item['snippet'].get('channelId',0)
                    main_dict['channelTitle'] = item['snippet'].get('channelTitle',0)
                    main_dict['title'] = item['snippet'].get('title',0)

                    # Video metrics
                    main_dict['viewCount'] = video_item['statistics'].get('viewCount',0)
                    main_dict['likeCount'] = video_item['statistics'].get('likeCount',0)
                    main_dict['commentCount'] = video_item['statistics'].get('commentCount',0)
                    main_dict['duration'] = video_duration

                    self.list_of_dict.append(main_dict)

                else:
                    continue

    def process_time_duration(self, duration : str):
        '''
        Function that extracts hours and minutes from the duration value that the API returns

        Parameters
        ------------
        duration : str
            Duration value from the API

        Returns
        ------------
        hours : int
            Extracted hours from the duration string
        minutes: int 
            Extracted hours from the duration string          
        '''
        if "D" in duration: 
            return None

        if "H" in duration:
            hour =  int(duration[2:].split('H')[0])
            if hour > 9:
                if "M" in duration:
                    minutes = int(duration[5:].split('M')[0])
                else:
                    minutes = 0
            else:
                if "M" in duration:
                    minutes = int(duration[4:].split('M')[0])
                else:
                    minutes = 0
        else:
            hour = 0
            if "M" in duration:
                minutes = int(duration[2:].split('M')[0])
            else:
                minutes = 0

        return hour, minutes

    def process_next_pages(self):
        '''
        Function that handles the pagination of the response results
        '''

        while self.nextPageToken:
            if len(self.list_of_dict) > self.search_limit:
                break

            response = self.yt.search().list(
                part='id, snippet',
                q=self.search_word,
                maxResults=50,
                type='video',
                pageToken=self.nextPageToken,
                order='viewCount' # Default: Relevance
            ).execute()

            self.nextPageToken = response.get('nextPageToken')
            self.process_query_results(response=response, minutes_limit=self.minutes_limit)

