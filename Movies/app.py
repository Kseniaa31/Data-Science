import streamlit as st
import pandas as pd
import joblib
import warnings
from warnings import filterwarnings
filterwarnings("ignore")

def load_data():
    data=pd.read_csv("movie_data.csv")
    dataframe=pd.read_csv("movie_dataframe.csv")
    return data, dataframe

def load_models():
    sig=joblib.load("sigmoid_kernel.pkl")
    tfv=joblib.load("tfidf_vectorizer.pkl")
    return tfv, sig

def give_recommendation(movie_title, model, data, dataframe):
  indices = pd.Series(data.index, index=data['original_title'])
  index = indices[movie_title]
  model_score = list(enumerate(model[index]))
  model_score_sorted= sorted(model_score, key=lambda x: x[1], reverse=True)
  model_score_10= model_score_sorted[1:11]
  movie_indices_10= [i[0] for i in model_score_10]
  return dataframe['original_title'][movie_indices_10]


data, dataframe = load_data()
tfv, sig = load_models()

st.set_page_config(page_title="Movie Recommendation", layout="centered")
st.title("🎬 Movie Recommendation")
st.write("Find movies similar to your favourite ")
movie_list= data["original_title"].sort_values().tolist()
selected_movie=st.selectbox("Select a movie: ", movie_list)

if st.button("Get Recommendations"):
    if selected_movie:
        recommendations=give_recommendation(selected_movie, sig, data, dataframe)
        st.subheader("Movies similar to : " + selected_movie)
        for index, movie in enumerate((recommendations)):
            st.write(str(index+1)+". "+ movie)

st.markdown("_ _ _")
st.markdown("This app uses Content based filtering")