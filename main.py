import urllib.request
import gzip
import os
import pandas as pd
import configparser
import zipfile


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
            
# Unzip a zip file.
def unzip_zip(file_name):
    print("Unzipping file: " + file_name)
    # Open the file
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        # Extract the file
        zip_ref.extractall('data/rotten_tomatoes')
        
# Unzip a file
def unzip_file(file_name):
    if(file_name.endswith(".gz")):
        unzip_gz(file_name)
    elif(file_name.endswith(".zip")):
        unzip_zip(file_name)
            
def download_and_unzip_imdb():
    # Download the file
    download_file("https://datasets.imdbws.com/title.ratings.tsv.gz", "data/imdb/title.ratings.tsv.gz")
    download_file("https://datasets.imdbws.com/title.basics.tsv.gz", "data/imdb/title.basics.tsv.gz")
    # Unzip the file
    unzip_file("data/imdb/title.ratings.tsv.gz")
    unzip_file("data/imdb/title.basics.tsv.gz")

# Download and unzip Rotten Tomatoes data
def download_and_unzip_rotten_tomatoes():
    download_file("https://drive.google.com/uc?id=1O7Xl3imQ_tWgdhkf6QBuUMMCMCET8bpj&export=download", "data/rotten_tomatoes/rotten_tomatoes_movies.zip")

    unzip_file("data/rotten_tomatoes/rotten_tomatoes_movies.zip")
    

def parse_rotten_tomatoes():
    # Open the files
    rt = pd.read_csv('data/rotten_tomatoes/rotten_tomatoes_movies.csv', sep=',', header=0, dtype={'rotten_tomatoes_link' : str, 'movie_title' : str, 'audience_rating' : float, 'audience_count' : float})
    
    # Remove lines where numVotes is less than 1000
    rt = rt[rt['audience_count'] >= 1000]
    
    # Sort the dataframe by rating
    rt = rt.sort_values(by=["audience_rating"], ascending=False)
    
    # write the data to a tsv file
    rt.to_csv('data/rotten_tomatoes/rotten_tomatoes.tsv', sep='\t', index=False)
    
# Matches the tconst from the title tsv with the tconst from the ratings tsv.
def parse_imdb():
    # Open the files
    basics = pd.read_csv('data/imdb/title.basics.tsv', sep='\t', header=0, dtype={'tconst': str, 'titleType': str, 'primaryTitle': str, 'originalTitle': str, 'isAdult': str, 'startYear': str, 'endYear': str, 'runtimeMinutes': str, 'genres': str})
    ratings = pd.read_csv('data/imdb/title.ratings.tsv', sep='\t', header=0, dtype={'tconst': str, 'averageRating': float, 'numVotes': int})

    imdb = basics.merge(ratings, on="tconst", how="inner")
    
    # Remove lines where titleType is not "movie"
    imdb = imdb[imdb['titleType'] == 'movie']
    
    # Remove lines where numVotes is less than 1000
    imdb = imdb[imdb['numVotes'] >= 1000]
    
    # Sort the dataframe by rating
    imdb = imdb.sort_values(by=["averageRating"], ascending=False)
    
    # write the data to a tsv file
    imdb.to_csv('data/imdb/imdb.tsv', sep='\t', index=False)

def match_rt_imdb():
    imdb = pd.read_csv('data/imdb/imdb.tsv', sep='\t', header=0, dtype={'tconst': str, 'titleType': str, 'primaryTitle': str, 'originalTitle': str, 'isAdult': str, 'startYear': str, 'endYear': str, 'runtimeMinutes': str, 'genres': str, 'averageRating': float, 'numVotes': int})
    rt = pd.read_csv('data/rotten_tomatoes/rotten_tomatoes.tsv', sep='\t', header=0, dtype={'rotten_tomatoes_link' : str, 'movie_title' : str, 'audience_rating' : float, 'audience_count' : float})
    
    merge = imdb.merge(rt, left_on="primaryTitle", right_on="movie_title", how="inner")
    
    merge.to_csv('data/merge/imdb_rt.tsv', sep='\t', index=False)

# Reads the config.ini file and runs the main function.
def read_config():
    # Open the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    imdb(config['IMDB'].getboolean('force_download'), config['IMDB'].getboolean('force_merge'))
    rotten_tomatoes(config['ROTTEN_TOMATOES'].getboolean('force_download'), config['ROTTEN_TOMATOES'].getboolean('force_merge'))
    merge(config['MERGE'].getboolean('force_merge'))

def imdb(force_download, force_merge):
    if (not os.path.exists("data/imdb")):
        os.makedirs("data/imdb")
        
    # Download and unzip the imdb data if force_download is True in the config.
    if (not os.path.exists("data/imdb/title.ratings.tsv") or not os.path.exists("data/imdb/title.basics.tsv") or force_download):
        print("Downloading and unzipping IMDB data...")
        download_and_unzip_imdb()
    
    if (not os.path.exists("data/imdb/imdb.tsv") or force_merge):
        print("Matching IMDB files...")
        parse_imdb()
        
def rotten_tomatoes(force_download, force_merge):
    if (not os.path.exists("data/rotten_tomatoes")):
        os.makedirs("data/rotten_tomatoes")
        
    # Download and unzip the imdb data if force_download is True in the config.
    if (not os.path.exists("data/rotten_tomatoes/rotten_tomatoes_movies.csv") or force_download):
        print("Downloading and unzipping Rotten Tomatoes data...")
        download_and_unzip_rotten_tomatoes()
    
    if (not os.path.exists("data/rotten_tomatoes/rotten_tomatoes.tsv") or force_merge):
        print("Parsing Rotten Tomatoes files...")
        parse_rotten_tomatoes()
        
def merge(force_merge):
    if (not os.path.exists("data/merge/merge.tsv") or force_merge):
        print("Merging files...")
        match_rt_imdb()

read_config()