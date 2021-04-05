import re, textwrap, sys
import requests, bs4 

def get_soup(link, headers={'User-Agent': 'My User Agent 1.0'}):
    page = requests.get(link, headers=headers)
    page.raise_for_status()
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    return soup

def getMetaDataOfMovies(link,limit):
    imdb_soup = get_soup(link)
    resulList=[]
    titleColumnresults = imdb_soup.find_all("td", {"class": "titleColumn"},limit=int(limit))
    titleColumnresultsText =  [titleColumnresult.getText().replace('\n','') for titleColumnresult in titleColumnresults]
    

    links = []
    for i in titleColumnresults:
        data=i
        url2 = data.find("a").attrs['href']
        links.append(url2)
    

    for link in links:
        imdb_soup2 = get_soup("https://www.imdb.com/"+link)
        year = imdb_soup.find({"class":"ipc-html-content ipc-html-content--base"})
        

    ratingColumnresults = imdb_soup.find_all("td", {"class": "ratingColumn imdbRating"},limit=int(limit))
    ratingColumnresultsText =  [ratingColumnresult.getText().replace('\n','') for ratingColumnresult in ratingColumnresults]
    for movieData in zip(titleColumnresultsText,ratingColumnresultsText):
        movieDict = {}
        title = movieData[0]
        movieDict['title'] = title
        movieDict['year'] = title[title.index('(')+len('('):title.index(')')]
        movieDict['rating'] = movieData[1]
        resulList.append(movieDict)

    return resulList

def main(args):
    data=getMetaDataOfMovies(args[1],args[2])
    print(data)

if __name__ == '__main__':
    args = sys.argv
    main(args)
