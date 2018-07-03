# Libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel
from collections import OrderedDict

class AnimeRecommendation:
    '''
        AnimeRecommendation Class to
            - GET Similarity Matrix,
            - GET Recommendations,

        Helper Functions:
            # getID - GET the corresponding ID for a Anime Name.
            # getTitle - GET Title of the Anime for a given Anime ID
            # getSynopsis - GET Short Summary of the Anime.
            # getGenre - GET Genre of the Anime
    '''

    def __init__(self, dataframe):
        '''
            __init__() method of the class AnimeRecommendation.

            Initialize TF-IDF & Count Vectorizer to be used for getting Similarity Matrix.

            Parameters:
                dataframe: Complete Dataset (in pandas dataframe format) of Anime.

            :return:
                None
        '''

        self.dataframe = dataframe

        # Initialize Tf-IDF and Count Vectorizer
        self.tfidf_vect = TfidfVectorizer(stop_words = "english", ngram_range = (1, 2))
        self.tfidf_vect_ = TfidfVectorizer(stop_words = "english")
        self.count_vect = CountVectorizer(stop_words = "english")

    def getSimilartiyMatrix(self):
        '''
            GET Similarity Matrix for Anime Dataset based on Synopsis, Genre & Rating.
            Similariity Matrix are obtained using TfidfVectorize on Synopsis & Genre and 
            CountVectorizer on Ratings followed by a linear_kernel().

            Cleaned Version of Synopsis, Genre and Rating are passed to the Vectorizers.

            Parameters:
                None

            :return:
                A list of 3 Similarity Metrices 
                    - Synopsis
                    - Genre
                    - Rating
        '''

        syn_mat = self.tfidf_vect.fit_transform(self. dataframe['cSynopsis'])
        genre_mat = self.tfidf_vect_.fit_transform(self. dataframe['cGenre'])
        rating_mat = self.count_vect.fit_transform(self. dataframe['cRating'])


        synopsis_similarity = linear_kernel(syn_mat, syn_mat)
        genre_similarity = linear_kernel(genre_mat, genre_mat)
        rating_similarity = linear_kernel(rating_mat, rating_mat)

        return [synopsis_similarity, genre_similarity, rating_similarity]

    def getID(self, anime_name):
        '''
            GET the ID of the Anime given Name of the Anime.
            
            getID() uses Anime Dataset to get the mapping of Anime Name to Anime ID.
            Function can return one or more ID's.

            Parameters:
                anime_name: Name of the Anime to get a ID.

            :return:
                ID or list of ID's.
        '''
        if self.dataframe['Title'][self.dataframe.Title.str.lower() == anime_name].any() != False:
            return self.dataframe[['Anime_ID', 'Title']][self.dataframe.Title.str.lower() == anime_name].iloc[0]['Anime_ID']

        return self.dataframe[['Anime_ID', 'Title']][self.dataframe.Title.str.lower().str.contains(anime_name)].iloc[0]['Anime_ID']

    def getTitle(self, anime_id):
        '''
            GET the Title of the Anime given the ID.

            Parameters:
                anime_id: ID of the Anime.

            :return:
                Title (or Name) of the Anime.
        '''
        return self.dataframe[['Anime_ID', 'Title']][self.dataframe['Anime_ID'] == anime_id].iloc[0]['Title']

    def getSynopsis(self, anime_id):
        '''
            GET Synopsis (or short summary) of the Anime.

            Parameters:
                anime_id: ID of the Anime.

            :return:
                Full Synopsis of the Anime.
        '''
        return self.dataframe[['Anime_ID', 'Synopsis']][self.dataframe['Anime_ID'] == anime_id].iloc[0]['Synopsis']

    def getGenre(self, anime_id):
        '''
            GET the Genre of the Anime.

            Parameters:
                anime_id: ID of the Anime.

            :return:
                All the Genre for the given Anime.
        '''
        return self.dataframe[['Anime_ID', 'Genre']][self.dataframe['Anime_ID'] == anime_id].iloc[0]['Genre']

    def getMapping(self):
        '''
            Mapping of Anime Dataset Index to Anime ID.

            Parameters:
                None

            :return:
                pandas Series Object.
        '''
        return pd.Series(self.dataframe.index, index = self.dataframe['Anime_ID'])

    def getRecommendation(self, anime_id, similarity_matrix, indices):
        '''
            Recommend Similar Anime based on the given anime and the similarity matrix.

            Score of each similarity matrix are combined by taking a mean() and sorted in
            non-descreasing order to get the most similar animes.

            Parameters:
                anime_id: ID of the Anime.
                similarity_matrix: Similarity Matrix to use for recommendation.
                indices: Mapping of Index to Anime ID.

            :return:
                List of ID's that are most similar.
        '''

        # Get the Index of the Anime.
        idx = indices[anime_id]
        
        # We have 3 Similarity Metrics
        ## 1. Synopsis Similarity
        ## 2. Genre Similarity
        ## 3. Rating Similarity
        
        score_1 = list(enumerate(similarity_matrix[0][idx]))
        score_2 = list(enumerate(similarity_matrix[0][idx]))
        score_3 = list(enumerate(similarity_matrix[0][idx]))
        
        # Sort the scores in reverse order
        score_1 = sorted(score_1, key = lambda x: x[0], reverse = False)
        score_2 = sorted(score_2, key = lambda x: x[0], reverse = False)    
        score_3 = sorted(score_3, key = lambda x: x[0], reverse = False)
        
        # Combining the Similarity Matrix
        combined_score = [(idx, np.mean([sc_1, sc_2, sc_3])) for (idx, sc_1), (_, sc_2), (_, sc_3) in zip(score_1, score_2, score_3)]
        
        # Sorting the Combined Score.
        combined_score = sorted(combined_score, key = lambda x: x[1], reverse = True)
        
        # Get ID of Top 10 Similar Animes
        anime_ids = [i[0] for i in combined_score[:10]]
        
        # Returning the Top Anime Names.
        return self.dataframe['Anime_ID'].iloc[anime_ids].values

    def build_AnimeDict(self, anime_id):
        '''
            Create a Ordered Dictionary of Anime Name, Synopsis andd Genres.

            Parameters:
                anime_id: Name of the Anime

            :return:
                Ordered Dictionary
        '''

        anime_dict = OrderedDict([
            ("name", self.getTitle(anime_id)),
            ("synopsis", self.getSynopsis(anime_id)),
            ("genre", self.getGenre(anime_id))
        ])

        return anime_dict

if __name__ == "__main__":
    print ("[ERROR] Import the Class.\n")
    exit(-1)