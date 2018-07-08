import pandas as pd
import re
import string

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

anime = pd.read_csv('Anime.csv')
anime['Title'] = anime.Title.apply(processTitle)
anime['cSynopsis'] = anime.Synopsis.apply(processSynopsis)
anime['cGenre'] = anime.Genre.str.lower()
anime['cRating'] = anime.Rating.apply(processRatings)
anime['Synopsis'] = anime.Synopsis.apply(processSynopsis_v2)

anime.to_csv('cleaned_anime_data.csv', index = False)
