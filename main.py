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
    if url.lower().startswith('http'):
        req = urllib.Request.request(url)
    else:
        raise ValueError from None

    with urllib.request.urlopen(req) as response:
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
def unzip_zip(file_name,path):
    print("Unzipping file: " + file_name)
    # Open the file
    with zipfile.ZipFile(file_name, 'r') as zip_ref:
        # Extract the file
        zip_ref.extractall(path)
        
# Unzip a file
def unzip_file(file_name, path):
    if(file_name.endswith(".gz")):
        unzip_gz(file_name)
    elif(file_name.endswith(".zip")):
        unzip_zip(file_name, path)
            
def download_and_unzip_imdb():
    # Download the file
    download_file("https://datasets.imdbws.com/title.ratings.tsv.gz", "data/imdb/title.ratings.tsv.gz")
    download_file("https://datasets.imdbws.com/title.basics.tsv.gz", "data/imdb/title.basics.tsv.gz")
    # Unzip the file
    unzip_file("data/imdb/title.ratings.tsv.gz","")
    unzip_file("data/imdb/title.basics.tsv.gz","")

# Download and unzip Rotten Tomatoes data
def download_and_unzip_rotten_tomatoes():
    download_file("https://drive.google.com/uc?id=1O7Xl3imQ_tWgdhkf6QBuUMMCMCET8bpj&export=download", "data/rotten_tomatoes/rotten_tomatoes_movies.zip")

    unzip_file("data/rotten_tomatoes/rotten_tomatoes_movies.zip", "data/rotten_tomatoes")

# Download and unzip Film TV data
def download_and_unzip_filmTv():
    download_file("https://drive.google.com/u/0/uc?id=1Tekj0y8v1AanxWkImyT4pbyXiDDzzgwS&export=download", "data/filmtv/filmtv.zip")

    unzip_file("data/filmtv/filmtv.zip", "data/filmtv")
    

def parse_rotten_tomatoes():
    # Open the files
    rt = pd.read_csv('data/rotten_tomatoes/rotten_tomatoes_movies.csv', sep=',', header=0, dtype={'rotten_tomatoes_link' : str, 'movie_title' : str, 'audience_rating' : "Int64", 'audience_count' : "Int64", 'original_release_date' : str})
    
    rt = rt[['rotten_tomatoes_link', 'movie_title', 'audience_rating', 'audience_count', 'original_release_date']]
    
    # Remove lines where numVotes is less than 1000
    rt = rt[rt['audience_count'] >= 1000]
    
    # Change the release date format like "2019-07-31" to a uear like "2019"
    rt['original_release_date'] = pd.DatetimeIndex(rt['original_release_date']).year.astype("Int64")
    
    # Sort the dataframe by rating
    rt = rt.sort_values(by=["audience_rating"], ascending=False)
    
    # write the data to a tsv file
    rt.to_csv('data/rotten_tomatoes/rotten_tomatoes.tsv', sep='\t', index=False)

def parse_filmTv():
    # Open the files
    ftv = pd.read_csv('data/filmtv/filmtv_movies - ENG.csv', sep=',', header=0, dtype={'filmtv_id' : str, 'title' : str, 'directors' : str, 'avg_vote' : float, 'critics_vote' : float, 'public_vote' : float})
    
    # write the data to a tsv file
    ftv.to_csv('data/filmtv/filmtv.tsv', sep='\t', index=False)
    


# Matches the tconst from the title tsv with the tconst from the ratings tsv.
def parse_imdb():
    # Open the files
    basics = pd.read_csv('data/imdb/title.basics.tsv', sep='\t', header=0, dtype={'tconst': str, 'titleType': str, 'primaryTitle': str, 'originalTitle': str, 'isAdult': str, 'startYear': str, 'endYear': str, 'runtimeMinutes': str, 'genres': str})
    ratings = pd.read_csv('data/imdb/title.ratings.tsv', sep='\t', header=0, dtype={'tconst': str, 'averageRating': float, 'numVotes': int})

    imdb = basics.merge(ratings, on="tconst", how="inner")
    
    # Remove lines where titleType is not "movie"
    imdb = imdb[imdb['titleType'] == 'movie']
    
    imdb = imdb[['tconst', 'primaryTitle', 'startYear', 'runtimeMinutes', 'averageRating', 'numVotes', 'genres']]
    
    # Remove lines where numVotes is less than 1000
    imdb = imdb[imdb['numVotes'] >= 1000]
    
    # Sort the dataframe by rating
    imdb = imdb.sort_values(by=["averageRating"], ascending=False)
    
    # write the data to a tsv file
    imdb.to_csv('data/imdb/imdb.tsv', sep='\t', index=False)

def match_rt_imdb_ftv():
    imdb = pd.read_csv('data/imdb/imdb.tsv', sep='\t', header=0, dtype={'tconst': str, 'primaryTitle': str, 'startYear': str, 'runtimeMinutes': str, 'averageRating': float, 'numVotes': int, 'genres': str})
    rt = pd.read_csv('data/rotten_tomatoes/rotten_tomatoes.tsv', sep='\t', header=0, dtype={'rotten_tomatoes_link' : str, 'movie_title' : str, 'audience_rating' : float, 'audience_count' : float, 'original_release_date' : str})
    ftv = pd.read_csv('data/filmtv/filmtv.tsv', sep='\t', header=0, dtype={'filmtv_id' : str, 'title' : str, 'director' : str, 'avg_vote' : float, 'critics_vote' : float, 'public_vote' : float, "year" : str})
    
    merge = imdb.merge(rt, left_on=["primaryTitle","startYear"], right_on=["movie_title","original_release_date"], how="inner")
    
    merge = merge.merge(ftv, left_on=["primaryTitle","startYear"], right_on=["title","year"], how="inner")
    
    # Calculate the average rating with 2 decimal places
    merge["averageRating"] = round(( (merge["averageRating"].astype("float")*merge["numVotes"])  + ((merge["audience_rating"] / 10) * merge["audience_count"].astype("Int64")) + (merge["avg_vote"].astype("float") * merge["total_votes"].astype("Int64")) ) / ( (merge["numVotes"] + merge["audience_count"].astype("Int64") + merge["total_votes"].astype("Int64")) ), 2)
    
    merge["numVotes"] = merge["numVotes"] + merge["audience_count"].astype("Int64") + merge["total_votes"].astype("Int64")
    
    # Sort the dataframe by rating
    merge = merge.sort_values(by=["averageRating"], ascending=False)
    
    merge = merge[['primaryTitle', 'original_release_date', 'directors','genres', 'runtimeMinutes', 'averageRating', 'numVotes', 'tconst', 'rotten_tomatoes_link', 'filmtv_id']]
    
    merge.to_csv('data/merge/imdb_rt_ftv.tsv', sep='\t', index=False)

# Reads the config.ini file and runs the main function.
def read_config():
    # Open the config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    imdb(config['IMDB'].getboolean('force_download'), config['IMDB'].getboolean('force_merge'))
    rotten_tomatoes(config['ROTTEN_TOMATOES'].getboolean('force_download'), config['ROTTEN_TOMATOES'].getboolean('force_merge'))
    filmTv(config['FILM_TV'].getboolean('force_download'), config['FILM_TV'].getboolean('force_merge'))
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

def filmTv(force_download, force_merge):
    if (not os.path.exists("data/filmtv")):
        os.makedirs("data/filmtv")
        
    # Download and unzip the imdb data if force_download is True in the config.
    if (not os.path.exists("data/filmtv/filmtv_movies - ENG.csv") or force_download):
        print("Downloading and unzipping FilmTV data...")
        download_and_unzip_filmTv()
    
    if (not os.path.exists("data/filmtv/filmtv.tsv") or force_merge):
        print("Parsing FilmTV files...")
        parse_filmTv()
        
def merge(force_merge):
    if (not os.path.exists("data/merge")):
        os.makedirs("data/merge")
        
    if (not os.path.exists("data/merge/imdb_rt_ftv.tsv") or force_merge):
        print("Merging files...")
        match_rt_imdb_ftv()

read_config()
