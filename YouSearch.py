"""Simple module to search Youtube. ~ Lore"""

from requests import Session
from re       import findall

# CONSTANTS
USERAGENT: dict = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Chrome/W.X.Y.Z Safari/537.36'}

class YouSearch(Session):
    def __init__(self, query: str = 'Youtube') -> None:
        super().__init__()
        
        self.results: list = []
        self._query:  str  = query


    @property
    def query(self) -> str:
        # NOTE: Return self._query to the query setter.
        return self._query
    
    @query.setter
    def query(self, query: str) -> None:    
        # NOTE: Setting self._query.
        if not isinstance(query, str):
            raise TypeError
        self._query: str = query


    def search(self) -> None:
        # NOTE: If present // Clear the results for the next query.
        self.results.clear()

        resp: str = self.get(
            url     = f'https://www.youtube.com/results?search_query={self.query}',
            headers = USERAGENT
        ).text
        
        # NOTE: Search for all data for each video (title, views, author/channel, etc...)
        for video in findall(r'"title":{"runs":(.*?),"params":"', resp):
            # NOTE: If title and author not found skip.
            if len(info := findall(r'{"text":"(.*?)"', video)) == 2:
                
                # NOTE: Cache these 2 values.
                video_id:    str = ''.join(findall(r'{"videoId":"(.*?)"', video))
                channel_tag: str = ''.join(findall(r'"canonicalBaseUrl":"/(.*?)"', video))

                self.results.append({
                    'title'      : info[0],
                    'author'     : info[1],
                    'video_url'  : f'https://www.youtube.com/watch?v={video_id}',
                    'length'     : ''.join(findall(r'"lengthText":{"accessibility":{"accessibilityData":{"label":"(.*?)"', video)),
                    'views'      : ''.join(findall(r'"viewCountText":{"simpleText":"(.*?)"', video)),
                    'channel_url': f'https://www.youtube.com/{channel_tag}'
                })


'''
EXAMPLE OF USAGE BELOW
------------------------
'''
session: YouSearch = YouSearch()
while True:
    session.query: str = input('Query: ')
    session.search()

    for video in session.results:
        print(f'''Title:   {video['title']}
Author:  {video['author']}
URL:     {video['video_url']}
Length:  {video['length']}
Views:   {video['views']}
Channel: {video['channel_url']}
''')
