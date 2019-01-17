import re

def cleanSynopsis(synopsis):
    # Replace [Written by MAL Rewrite] wiht ``
    cleaned = synopsis.replace("[Written by MAL Rewrite]", "")
    # Remove extra characters
    cleaned = re.sub(r'[&#039;]', '', cleaned)
    # Remove extra white spaces
    cleaned = cleaned.strip()

    # return the Cleaned Version
    return cleaned

def cleanTitle(title):
    # Remove extra characters
    cleaned = re.sub(r'[&#039;]', '', title)
    # Remove extra characters
    cleaned = cleaned.replace(";", ":")
    # Remove extra white spaces
    cleaned = cleaned.strip()

    # return the Cleaned Version
    return cleaned

def processSynopsis(synopsis):
    # Convert the Synopsis to all lower characters
    synopsis = synopsis.lower()
    # Replace [Written by MAL Rewrite] wiht ``
    cleaned = synopsis.replace("[written by mal rewrite]", "")
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

def processRatings(rating):
    # Convert the Synopsis to all lower characters
    rating = rating.lower()
    # Remove all the puncation
    cleaned = re.sub(r'[,\.!"()?-]', '', rating)
    # Remove extra white spaces
    cleaned = cleaned.strip()

    # return the Cleaned Version
    return cleaned