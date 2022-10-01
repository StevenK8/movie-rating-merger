import csv



res = []
titleFilmtv = []
fh = open('../filmTVDataset/filmtv_movies.csv',encoding='utf-8')
reader = csv.reader(fh, delimiter = ',')
#skip 1st line
next(reader)
for ligne in reader:
    film_title      = ligne[1]
    film_director   = ligne[6]

    if ligne[8] != '' and ligne[9] != '' and ligne[10] != '' and ligne[11] != '':
        film_avgVote    = float(ligne[8])
        film_publicVote = float(ligne[10])
        film_criticsVote= float(ligne[9])
        film_totalVote  = int(ligne[11])
        temp = [film_title,film_director,film_avgVote,film_publicVote,film_criticsVote]
        res.append(temp)
        titleFilmtv.append(film_title)
"""
res[i][0] = id
res[i][1] = original title
res[i][2] = director
res[i][3] = average vote
res[i][4] = public vote
res[i][5] = critics vote
"""




resImdb = []
titleImdb = []
fh = open('data/imdb/imdb.tsv',encoding='utf-8')
reader = csv.reader(fh, delimiter = '\t')
for ligne in reader:
    title = ligne[3]
    avgVote = ligne[9]
    year = ligne[5]
    duration = ligne[7]
    resImdb.append([title, avgVote, year, duration])
    titleImdb.append(title)

matchingTitle = list(set(titleFilmtv).intersection(titleImdb))

print('imdb : ', len(resImdb), '\t filmsTv : ', len(res), ' final : ', len(matchingTitle))



resFinal = []
for i in range(len(matchingTitle)):
    title = matchingTitle[i]
    for j in range(len(resImdb)):
        if(matchingTitle[i] == resImdb[j][0]):
            year = resImdb[j][2]
            avgVoteImdb = resImdb[j][1]
            duration = resImdb[j][3]
    for j in range(len(res)):
        if(matchingTitle[i] == res[j][0]):
            avgVoteFilmtv = res[j][2]
            director = res[j][1]
            publicVote = res[j][3]
            criticsVote = res[j][4]
    resFinal.append([title,year,duration,avgVoteFilmtv,director,publicVote, criticsVote])

print(len(resFinal))




