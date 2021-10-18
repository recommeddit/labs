# # importing the module
# import imdb
#
# # creating instance of IMDb
# ia = imdb.IMDb()
#
# # movie name
# name = "3 idiots"
#
# # searching the movie
# search = ia.search_movie(name)
#
# # printing the result
# for i in search:
#     print(i)

# importing the module
import imdb

# creating instance of IMDb
ia = imdb.IMDb()

# movie name
name = "Tarzan the wonder car"

# searchning the movie
search = ia.search_movie(name)

# printing the result
for i in search:
    print(i)
