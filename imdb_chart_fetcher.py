import re, textwrap, sys
import requests, bs4 
import numpy as np

def get_soup(link, headers={'User-Agent': 'My User Agent 1.0'}):
    page = requests.get(link, headers=headers)
    page.raise_for_status()
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    return soup

def getMetaDataOfMovies(link,limit):
    imdb_soup = get_soup(link)
    page1data=[]
    titleColumnresults = imdb_soup.find_all("td", {"class": "titleColumn"},limit=int(limit))
    titleColumnresultsText =  [titleColumnresult.getText().replace('\n','') for titleColumnresult in titleColumnresults]
    

    links = []
    for i in titleColumnresults:
        data=i
        url2 = data.find("a").attrs['href']
        links.append(url2)
    
    page2data = []
    for link in links:
        url="https://www.imdb.com/"+link
        #print(url)
        imdb_soup2 = get_soup(url)
        detail = imdb_soup2.find(class_="subtext")
        subtext=detail.getText()
        data2=subtext.split()
        summary = imdb_soup2.find(class_="summary_text")
        #print(summary.getText())
        freshdata = [{
            "duration" : data2[2]+data2[3],
            "genre" : data2[5],
            "summary" : summary.getText().strip()
        }]
        #print(freshdata)
        page2data.append(freshdata)
    #print(page2data)

    ratingColumnresults = imdb_soup.find_all("td", {"class": "ratingColumn imdbRating"},limit=int(limit))
    ratingColumnresultsText =  [ratingColumnresult.getText().replace('\n','') for ratingColumnresult in ratingColumnresults]
    for movieData in zip(titleColumnresultsText,ratingColumnresultsText):
        movieDict = {}
        title = movieData[0]
        movieDict['title'] = title.strip()
        movieDict['year'] = title[title.index('(')+len('('):title.index(')')]
        movieDict['rating'] = movieData[1]
        movie=[movieDict]
        page1data.append(movie)
    
    resultList = np.concatenate((page1data,page2data),axis=1)
    #print(page1data,page2data)
    #resultList =[]
    return resultList

def main(args):
    data=getMetaDataOfMovies(args[1],args[2])
    print(data)

if __name__ == '__main__':
    args = sys.argv
    main(args)
