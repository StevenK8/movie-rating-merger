import csv



res = []
fh = open('filmTVDataset/filmtv_movies.csv',encoding='utf-8')
reader = csv.reader(fh, delimiter = ',')
next(reader)
for ligne in reader:
    film_id         = ligne[0]
    film_title      = ligne[1]
    film_director   = ligne[6]

    if ligne[8] != '' and ligne[9] != '' and ligne[10] != '' and ligne[11] != '':
        film_avgVote    = float(ligne[8])
        film_publicVote = float(ligne[10])
        film_criticsVote= float(ligne[9])
        film_totalVote  = int(ligne[11])
    if(film_totalVote > 100):
        temp = [film_id,film_title,film_director,film_avgVote,film_publicVote,film_criticsVote]
        res.append(temp)

"""
res[i][0] = id
res[i][1] = original title
res[i][2] = director
res[i][3] = average vote
res[i][4] = public vote
res[i][5] = critics vote
"""

#print les films qui ont une avg note sup à 8
for i in range(len(res)):
    if res[i][3] > 8:
        print(res[i][1])
