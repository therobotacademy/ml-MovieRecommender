# Movie Recommender: Learn More

This document provides more detail about the sample movie recommender.


## How it works

The `movie_recommender.py` script performs the following actions:

```
[Load Data] -> [Prepare Data] -> [Train Model] -> [Explore Model]
```

### Load Data

For this sample, two datasets are loaded: movie item data (27,279 movies), 
and user action data (1,000,000 ratings).

Movie **item data** describes individual movies, with fields such as title, description, tags, etc.:

movieId  | title            | genres
-------- | ---------------- | -----------
1        | Toy Story (1995) | Adventure,Animation,Children,Comedy,Fantasy
2        | Jumanji (1995)   | Adventure,Children,Fantasy
3        | Grumpier Old Men (1995) | Comedy,Romance

User **action data** documents past interactions between users and movie items, and
includes fields such as `user_id`, `item_id`, and a numeric `rating` score column (optional):

userId | movieId | rating | timestamp
------ | ------- | ------ | ----------
1      | 2       | 3.5    | 1112486027
1      | 29      | 3.5    | 1112484676
1      | 32      | 3.5    | 1112484819


### Prepare Data

Once the data is loaded, you typically want to clean it up or transform it in various ways.
Here, we will remove items that were rated less than 5 times, because sometimes infrequently rated 
items can cause the model to behave unpredictably.

We also extract the `year` and `title` from the original `title` column, which
combined these together, and parse the `genres` column by splitting on commas.

See our [user guide on feature engineering](https://dato.com/learn/userguide/feature-engineering/introduction.html) for more discussion.


### Train Recommender Model

Next, we randomly split the data into a training set and validation set.
We use [`gl.recommender.create`](https://dato.com/products/create/docs/generated/graphlab.recommender.create.html) to build a recommender model on the training set with default settings.

For more background about recommender models in GraphLab Create, see our [guide for recommender systems](https://dato.com/learn/userguide/recommender/introduction.html).


### Explore the Model

Once you've trained the model, the sample script launches
two interactive web applications for exploring and evaluating
the model:

![Screenshot of Exploration](/assets/explore.png)

![Screenshot of Evaluation](/assets/evaluate.png)


## Use your own data

You can replace the sample data provided in this project with your own
dataset. The easiest way to do this is to look at the `items.csv` and
`ratings.csv` file loaded by the `movie_recommender.py` script and format your data
the same way. Then, simply replace the filenames in the `gl.SFrame.read_csv` 
commands in `movie_recommender.py` with your own data filenames.

If you want to use different column names in your data files, you will 
also need to make other changes to the example script. For example,
if your data contains a `bookId` column instead of a `movieId` column, 
you will need to replace references to `movieId` in `movie_recommender.py`.

Once you have built an initial model from your own data, you might also
find that the model performance can be improved if you change or replace the
data cleaning and feature extraction commands in `movie_recommender.py` with customized instructions.
The ideal set of data transformations typically varies from dataset to dataset,
so you will have to experiment a bit. For some suggestions, 
see our [user guide on feature engineering](https://dato.com/learn/userguide/feature-engineering/introduction.html).


## Integrate with your app

The interactive views that are created by the `movie_recommender.py` script
are powered by a local HTTP server running inside your Python process.
You can use this same service and the API it exposes to get started
quickly integrating your recommender model into your own app.

Here is a summary of the recommender model's REST API.
The returned items are provided in JSON object format:

method | parameters | return
------ | ---------- | ------
more_like_this | item_id (int) | a list of items
personalized_recommendations | item_ids (list) | a list of items
search  | query (str) | a list of items
details | item_ids (list) | a list of items

Requests must be POSTed to your view's url with
a JSON body specifying the method and parameters.

Below is a sample request body:
```json
{  
   "api_key":"",
   "data":{  
      "method":"more_like_this",
      "item_id":480,
      "num_recs":1
   }
}
```

And the resulting response:
```json
{  
   "status":"ok",
   "version":1,
   "uuid":"00000000-0000-0000-0000-000000000000",
   "model":"00000000-0000-0000-0000-000000000000",
   "response":{  
      "method":"more_like_this",
      "result":{
         "column_names":[
           "movieId","score","rank","title","genres",
           "imdbId","tmdbId","path","year"
         ],
         "data":[
            {
               "genres":["Comedy", "Drama", "Romance", "War"],
               "movieId":356,
               "title":"Forrest Gump",
               "imdbId":109830,
               "rank":1,
               "score":0.5820625484621349,
               "tmdbId":13,
               "year":"1994",
               "path":"http://image.tmdb.org/t/p/w500/z4ROnCrL77ZMzT0MsNXY5j25wS2.jpg"
            }
         ]
      }
   },
   "from_cache":false
}
```

