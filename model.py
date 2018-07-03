# Libraries
import pandas as pd
from datetime import datetime

class Ratings:
    '''
        Ratings Class to add ratings between given Anime and recommended Animes.
    '''
    def __init__(self):
        '''
            __init__() method to initialize counter and list of ratings.

            Parameters:
                None
            
            :return:
                None
        '''
        self.counter = 0
        self.anime_ratings = list()

    def __reset__(self):
        '''
            Helper Function to reset the counter back to zero.

            Parameters:
                None

            :return:
                None
        '''
        self.counter = 0

    def addRating(self, rating_data):
        '''
            Parameters:
                rating_data (Tuple): A tuple of (main_anime_id, recommended_anime_id, rating)

            :return:
                Current Value of the Counter.
        '''
        self.counter += 1
        self.anime_ratings.append(rating_data)

        return self.counter

    def saveRating(self):
        '''
            Save the Ratings in a CSV File.

            Parameters:
                None

            :return:
                None
        '''
        r = pd.DataFrame(self.anime_ratings, columns = ['Anime_ID', 'Recomm_ID', 'Ratings'])
        r.to_csv(f'ratings - {datetime.now().strftime(("%Y-%m-%d %H|%M"))}.csv', index = False)

if __name__ == "__main__":
    print ("[ERROR] Import the Class.\n")
    exit(-1)