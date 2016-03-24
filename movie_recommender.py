from os import path
import graphlab as gl

### Load Data ###
# MovieLens dataset collected by the GroupLens Research Project at the University of Minnesota.
# For more information, see http://grouplens.org/datasets/movielens/

# Path to the dataset directory
data_dir = './dataset/ml-20m'

# Table of movies we are recommending: movieId, title, genres
items = gl.SFrame.read_csv(path.join(data_dir, 'movies.csv'))

# Table of interactions between users and items: userId, movieId, rating, timestamp
actions = gl.SFrame.read_csv(path.join(data_dir, 'ratings.csv'))


### Prepare Data ###

# Prepare the data by removing items that are rare
rare_items = actions.groupby('movieId', gl.aggregate.COUNT).sort('Count')
rare_items = rare_items[rare_items['Count'] <= 5]
items = items.filter_by(rare_items['movieId'], 'movieId', exclude=True)
actions = actions.filter_by(rare_items['movieId'], 'movieId', exclude=True)

# Extract year, title, and genre
items['year'] = items['title'].apply(lambda x: x[-5:-1])
items['title'] = items['title'].apply(lambda x: x[:-7])
items['genres'] = items['genres'].apply(lambda x: x.split('|'))


### Train Recommender Model ###

training_data, validation_data = gl.recommender.util.random_split_by_user(actions, 'userId', 'movieId')
model = gl.recommender.create(training_data, 'userId', 'movieId')


### Evaluate and Explore the Model ###

# Get the metadata ready
urls = gl.SFrame.read_csv(path.join(data_dir, 'movie_urls.csv'))
items = items.join(urls, on='movieId')
users = gl.SFrame.read_csv(path.join(data_dir, 'user_names.csv'))

# Interactively evaluate and explore recommendations
view = model.views.overview(validation_set=validation_data,
                            user_data=users,
                            item_data=items,
                            item_name_column='title',
                            item_url_column='url',
                            user_name_column='name')
view.show()
