import pandas as pd
import re
import string
import os

def processSynopsis(X):
    # Convert the Synopsis to all lower characters
    X = X.lower()
    # Replace [Written by MAL Rewrite] wiht ``
    cleaned = X.replace("[written by mal rewrite]", "")
    # Remove all the puncation
    cleaned = re.sub(r'[,\.!"?-]', '', cleaned)
    # Remove extra characters
    cleaned = re.sub(r'[&#039;]', '', cleaned)
    # Remove extra white spaces
    cleaned = cleaned.strip()
    # Replace newline with ``
    cleaned = cleaned.replace("\n", " ")

    # return the Cleaned Version
    return cleaned

def processSynopsis_v2(X):
    # Replace [Written by MAL Rewrite] wiht ``
    cleaned = X.replace("[Written by MAL Rewrite]", "")
    # Remove extra characters
    cleaned = re.sub(r'[&#039;]', '', cleaned)
    # Remove extra white spaces
    cleaned = cleaned.strip()

    # return the Cleaned Version
    return cleaned

def processRatings(X):
    # Convert the Synopsis to all lower characters
    X = X.lower()
    # Remove all the puncation
    cleaned = re.sub(r'[,\.!"()?-]', '', X)
    # Remove extra white spaces
    cleaned = cleaned.strip()

    # return the Cleaned Version
    return cleaned

def processTitle(X):
    # Remove extra characters
    cleaned = re.sub(r'[&#039;]', '', X)
    # Remove extra characters
    cleaned = cleaned.replace(";", ":")
    # Remove extra white spaces
    cleaned = cleaned.strip()

    # return the Cleaned Version
    return cleaned

# open the csv file
anime = pd.read_csv('anime.csv')

# Apply Pre-Processing Steps
anime['Title'] = anime.Title.apply(processTitle)
anime['Synopsis'] = anime.Synopsis.apply(processSynopsis_v2)

# New Columns 'c' stands for cleaned
anime['cSynopsis'] = anime.Synopsis.apply(processSynopsis)
anime['cGenre'] = anime.Genre.str.lower()
anime['cRating'] = anime.Rating.apply(processRatings)

# Check dataset already exists on the disk
if os.path.isfile('cleaned_anime_data.csv'):
    # open the dataset
    df = pd.read_csv('cleaned_anime_data.csv')
    # append the new dataset to the old one
    df = df.append(anime)
    # for safety check remove all duplicates
    df.drop_duplicates(subset = ["Anime_ID"], inplace = True)
    # save the dataset back to the disk
    df.to_csv('cleaned_anime_data.csv', index = False)

# else save the new dataset
else:
    anime.to_csv('cleaned_anime_data.csv', index = False)
