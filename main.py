import urllib.request
import gzip
import os

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
        

def main():
    if (not os.path.exists("data/imdb")):
        os.makedirs("data/imdb")
        
    if (not os.path.exists("data/imdb/title.ratings.tsv") or not os.path.exists("data/imdb/title.basics.tsv")):
        print("Downloading and unzipping IMDB data...")
        download_and_unzip_imdb()

main()