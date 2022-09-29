import streamlit as st
import pickle
import pandas as pd
import requests

def convert(s):
    str = list(s)
    n = len(str)
    ans=""
    for i in range(n):
        ans = ans+(str[i])

        if not(i==(n-1)):
            ans= ans+('+')

    return ans




def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=2cb616cd768ce5454da0b9421cf5614f&language=en-US'.format(movie_id)
    url2 = "https://streaming-availability.p.rapidapi.com/get/basic"
    headers = {
        "X-RapidAPI-Key": "1fb389707dmshb4f0193a28eb38bp1adb96jsn397fb97f010b",
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    querystring = {"country":"in","tmdb_id": "movie/"+str(movie_id),"output_language":"en"}



    response2 = requests.request("GET",url2,headers=headers,params=querystring)
    data2 = response2.json()
    info = data2['streamingInfo']
    print(info)
    site = list(dict.keys(info))
    if(len(site)!=0):
        region = list(dict.keys(info[site[0]]))
        link = ((info[site[0]][region[0]]['link']))
    else:
        link="https://themoviedb.org/movie/"+str(movie_id)


    path = "https://image.tmdb.org/t/p/w500/"+poster_path
    # overview =
    return path,link

def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_idx])),reverse=True,key=lambda x:x[1])

    recommended_movies = []
    recommended_movies_posters = []
    links = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id

        # fetch poster from API
        poster,link = fetch_poster(movie_id)
        recommended_movies_posters.append(poster)
        recommended_movies.append(movies.iloc[i[0]].title)
        links.append(link)
    return recommended_movies,recommended_movies_posters,links

movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))



st.title('Movie Recommender System')

selected_movie_name = st.selectbox('Select a movie you enjoyed watching.',movies['title'].values)

if st.button('Recommend'):
    names,posters,links = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        html = f"<a href='{links[0]}'><img src='{posters[0]}' width='100%' margin='2%' padding='20' align='centre'></a>"
        st.markdown(html, unsafe_allow_html=True)
    with col2:
        st.text(names[1])
        html = f"<a href='{links[1]}'><img src='{posters[1]}' width='100%' margin='2%' padding='20' align='centre' ></a>"
        st.markdown(html, unsafe_allow_html=True)
    with col3:
        st.text(names[2])
        html = f"<a href='{links[2]}'><img src='{posters[2]}' width='100%' margin='2%' padding='20' align='centre' ></a>"
        st.markdown(html, unsafe_allow_html=True)
    with col4:
        st.text(names[3])
        html = f"<a href='{links[3]}'><img src='{posters[3]}' width='100%' margin='2%' padding='20' align='centre' ></a>"
        st.markdown(html, unsafe_allow_html=True)
    with col5:
        st.text(names[4])
        html = f"<a href='{links[4]}'><img src='{posters[4]}' width='100%' margin='2%' padding='20' align='centre' ></a>"
        st.markdown(html, unsafe_allow_html=True)



