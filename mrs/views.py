from django.shortcuts import render
from django.conf import settings
import urllib
import  os
import pickle as pk
import re
import bs4 as bs
from tmdbv3api import TMDb, Movie
import requests
# Create your views here.
tmdb = TMDb()
tmdb.api_key = settings.TMDB_KEY


movie = Movie()



def search_view(request ) :
    print("hhhhhhhhhh" , settings.TMDB_KEY)



    if request.method == "POST" and request.POST['searched'] != "" :
        searched= request.POST['searched']
        movies = movie.search(str(searched))
        test = True
        if  len(movies) == 0 :
                test = False
                return render(request, 'mrs/movie_search_result.html', {"test": test, 'searched': searched, })
        else :
                loaded_model = pk.load(open('./nlp/sentiment_model.pkl', 'rb'))
                vectorizer = pk.load(open("./nlp/tranform.pkl", 'rb'))

                response = requests.get('https://api.themoviedb.org/3/movie/'+str(movies[0].id)+'/credits?api_key='+settings.TMDB_KEY)
                casts = response.json()['cast']

                response1 = requests.get(
                    'https://api.themoviedb.org/3/movie/'+str(movies[0].id)+'?api_key='+settings.TMDB_KEY)
                movie_result = response1.json()
                imdb_id = movie_result['imdb_id']
                sauce = urllib.request.urlopen(
                    'https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
                soup = bs.BeautifulSoup(sauce, 'lxml')
                soup_result = soup.find_all("div", {"class": "text show-more__control"})
                clf = pk.load(open('./nlp/sentiment_model.pkl', 'rb'))
                vectorizer = pk.load(open("./nlp/tranform.pkl", 'rb'))
                all_reviews = {}

                idx = 0
                for  review in soup_result:
                    if review.string:
                        movie_vect = vectorizer.transform([review.string])
                        pred = clf.predict(movie_vect)[0]

                        all_reviews[idx] = {'text' : review.string , 'pred' : pred}
                        idx += 1

                recommandations = movie.recommendations(movie_result['id'])

                return render(request, 'mrs/movie_search_result.html', {"test" : test , 'searched': searched, 'movie': movie_result
                    , "casts" : {'g1' :casts[:5] , 'g2' : casts[5:10]} , 'all_reviews' : all_reviews , 'semilar' : recommandations[:5]
                                                           } )



    else :
        return render(request , 'mrs/movie_search_result.html' , {} )


def main_view(request ) :
    return render(request, 'mrs/main.html', {})


def api(request):
    response = requests.get('https://api.themoviedb.org/3/movie/3131?api_key='+settings.TMDB_KEY)
    geodata = response.json()
    return render(request, 'mrs/api.html', {'cast' : geodata['imdb_id']
    })




def test(request) :
    return render(request, 'mrs/test.html', {})



def reviews(request) :
    a = 'https://api.themoviedb.org/3/movie/3131?api_key='+settings.TMDB_KEY
    response = requests.get(a)
    response = requests.get(a)
    movie = response.json()
    m = Movie()
    imdb_id = movie['imdb_id']
    sauce = urllib.request.urlopen('https://www.imdb.com/title/{}/reviews?ref_=tt_ov_rt'.format(imdb_id)).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    soup_result = soup.find_all("div", {"class": "text show-more__control"})
    all_reviews = []
    for review in soup_result :
        if review.string :
            all_reviews.append(review.string)


    print(len(soup_result))
    recommandations = m.recommendations(movie_id=movie['id'])
    return render(request , 'mrs/reviews.html' , {'movie' : movie , 'soup' : all_reviews})