import urllib.request
import gzip
import os
import pandas as pd
import configparser


# Downloads a file from an URL and saves it to a local file.
def download_file(url, file_name):
    print("Downloading file from URL: " + url)
    # Open the url
    with urllib.request.urlopen(url) as response:
        # Read the response
        data = response.read()
        # Open the file
        with open(file_name, "wb") as file:
            # Write the data to the file
            file.write(data)

# Unzips a gzip file.
def unzip_gz(file_name):
    print("Unzipping file: " + file_name)
    # Open the file
    with gzip.open(file_name, "rb") as file:
        # Read the file
        data = file.read()
        # Open the file
        with open(file_name[:-3], "wb") as out_file:
            # Write the data to the file
            out_file.write(data)
            
def download_and_unzip_imdb():
    # Download the file
    download_file("https://datasets.imdbws.com/title.ratings.tsv.gz", "data/imdb/title.ratings.tsv.gz")
    download_file("https://datasets.imdbws.com/title.basics.tsv.gz", "data/imdb/title.basics.tsv.gz")
    # Unzip the file
    unzip_gz("data/imdb/title.ratings.tsv.gz")
    unzip_gz("data/imdb/title.basics.tsv.gz")
        

# Matches the tconst from the title tsv with the tconst from the ratings tsv.
def match_tconst():
    # Open the files
    basics = pd.read_csv('data/imdb/title.basics.tsv', sep='\t', header=0, dtype={'tconst': str, 'titleType': str, 'primaryTitle': str, 'originalTitle': str, 'isAdult': str, 'startYear': str, 'endYear': str, 'runtimeMinutes': str, 'genres': str})
    ratings = pd.read_csv('data/imdb/title.ratings.tsv', sep='\t', header=0, dtype={'tconst': str, 'averageRating': float, 'numVotes': int})

    imdb = basics.merge(ratings, on="tconst", how="inner")
    
    # Remove lines where titleType is not "movie"
    imdb = imdb[imdb['titleType'] == 'movie']
    
    # Remove lines where numVotes is less than 10000
    imdb = imdb[imdb['numVotes'] >= 10000]
    
    # Sort the dataframe by rating
    imdb = imdb.sort_values(by=["averageRating"], ascending=False)
    
    # write the data to a tsv file
    imdb.to_csv('data/imdb/imdb.tsv', sep='\t', index=False)
    

# Reads the config.ini file and runs the main function.
def read_config():
    # Open the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    main(config['IMDB'].getboolean('force_download'), config['IMDB'].getboolean('force_merge'))

def main(force_download, force_merge):
    if (not os.path.exists("data/imdb")):
        os.makedirs("data/imdb")
        
    # Download and unzip the imdb data if force_download is True in the config.
    if (not os.path.exists("data/imdb/title.ratings.tsv") or not os.path.exists("data/imdb/title.basics.tsv") or force_download):
        print("Downloading and unzipping IMDB data...")
        download_and_unzip_imdb()
    
    if (not os.path.exists("data/imdb/imdb.tsv") or force_merge):
        print("Matching tconst...")
        match_tconst()

read_config()