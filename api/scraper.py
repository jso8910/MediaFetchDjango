# Example search https://news.google.com/search?q=CNN&hl=en-US&gl=US&ceid=US:en

# Classes:
# Article
# Title and link are in this: ipQwMb ekueJc gEATFF RD0gLb
# Link in this: VDXfz
# Beginning of article: xBbh9
# Image: tvs3Id QwxBBf
# Publisher: wEwyrc AVN2gc uQIVzc Sksgp
# Time (in a datetime element): WW6dff uQIVzc Sksgp


import requests
from bs4 import BeautifulSoup

def newsSearch(query, timeRange='', excluding='', requiring=''):
    if excluding != '':
        excluding = ' '.join(['-' + excludeWord for excludeWord in excluding.split()])
    elif timeRange != '':
        timeRange = 'when:' + timeRange
    elif requiring != '':
        timeRange = '"' + requiring + '"'
    
    if not query:
        return {'status': 'error', 'code': 400, 'error': 'missing query', 'articlesFound': 0, 'articles': []}
    url = f'https://news.google.com/search?q={str(query)} {requiring} {timeRange} {excluding}&hl=en-US&gl=US&ceid=US:en'
    print(url)
    try:
        page = requests.get(url)
    except:
        data = {}
        data['status'] = 'error'
        data['code'] = 500
        data['error'] = 'network error server side.' \
                        'contact us on our support page to let' \
                        'us know about the issue'
        data['articlesFound'] = 0
        data['articles'] = []
        return data
    try:
        soup = BeautifulSoup(page.text, 'lxml')
        articles = soup.find_all('div', class_='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc')
    except:
        data = {}
        data['status'] = 'error'
        data['code'] = 500
        data['error'] = 'error collecting data'
        data['articlesFound'] = 0
        data['articles'] = []
        return data

    data = {}
    data['status'] = 'searching'
    data['error'] = None
    data['code'] = 200
    data['articlesFound'] = len(articles)
    numArticles = 0
    data['articles'] = []
    if len(articles) < 1:
        data['status'] = 'error'
        data['error'] = 'no articles found'
        return data
    for article in articles:
        numArticles += 1

        title_elem = article.find('h3', class_='ipQwMb ekueJc RD0gLb')
        article_link = article.find('a', class_='DY5T1d')
        article_snippet = article.find('span', class_='xBbh9')
        image_url = article.find('img', class_='tvs3Id QwxBBf')

        publisher = article.find('a', class_='wEwyrc AVN2gc uQIVzc Sksgp')
        time = article.find('time', class_='WW6dff uQIVzc Sksgp')

        url = article_link['href'].replace('./', 'https://news.google.com/', 1)
        if time == None:
            data['articles'].append({
                "source": publisher.text,
                "title": title_elem.text,
                "articlePreview": article_snippet.text,
                "url": url,
                "urlToImage": image_url['src'].replace('-h100-w100', ''),
                "timePublished": "Not found"})
        else:
            data['articles'].append({
                "source": publisher.text,
                "title": title_elem.text,
                "articlePreview": article_snippet.text,
                "url": url,
                "urlToImage": image_url['src'].replace('-h100-w100', ''),
                "timePublished": time['datetime']})

    data['status'] = 'success'
    return data
