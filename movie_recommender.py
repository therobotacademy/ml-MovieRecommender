#!/usr/bin/env python

from os import path
import graphlab as gl

### Load Data ###

# MovieLens dataset collected by the GroupLens Research Project at the University of Minnesota.
# For more information, see http://grouplens.org/datasets/movielens/

# Path to the dataset: ../../datasets
data_dir = path.join(path.dirname(path.realpath(__file__)), 'dataset')

# Table of movies we are recommending: movieId, title, genres
items = gl.SFrame.read_csv(path.join(data_dir, 'ml-20m/movies.csv'))

# Table of interactions between users and items: userId, movieId, rating, timestamp
interactions = gl.SFrame.read_csv(path.join(data_dir, 'ml-20m/ratings.csv'))


### Prepare Data ###

# Prepare the data by removing items that are rare
rare_items = interactions.groupby('movieId', gl.aggregate.COUNT).sort('Count')
rare_items = rare_items[rare_items['Count'] <= 5]
items = items.filter_by(rare_items['movieId'], 'movieId', exclude=True)
interactions = interactions.filter_by(rare_items['movieId'], 'movieId', exclude=True)

# Extract year, title, and genre
items['year'] = items['title'].apply(lambda x: x[-5:-1])
items['title'] = items['title'].apply(lambda x: x[:-7])
items['genres'] = items['genres'].apply(lambda x: x.split('|'))


### Train Recommender Model ###

training_set, validation_set = gl.recommender.util.random_split_by_user(interactions, 'userId', 'movieId')
model = gl.recommender.create(training_set, 'userId', 'movieId')


### Explore the Model ###

urls = gl.SFrame.read_csv(path.join(data_dir, 'ml-20m/movie_urls.csv'))
items = items.join(urls, on='movieId')

users = gl.SFrame.read_csv(path.join(data_dir, 'ml-20m/user_names.csv'))

# Interactively explore recommendations
v1 = model.views.explore(user_data=users, user_name_column='name',
                         item_data=items, item_name_column='title', item_url_column='url')
v1.show()

# Visualize model performance
v2 = model.views.performance(validation_set)
v2.show()
