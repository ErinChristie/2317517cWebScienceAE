import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

# Open text file so can write outputs to it 
file = open("Clusters.txt", "w")
tweets = pd.read_csv("C:/Users/Erin9/OneDrive/Documents/3rd Year/Web Science/WSAE.csv")
# Extract usernames from tweets
tweets_username = tweets['username']
# Extract hashtags from tweets
tweets_hashtags = tweets['hashtags']
# Extract text from tweets
tweets_text = tweets['text']

vectorizer = TfidfVectorizer(stop_words='english')
# Vectorise the usernames
username = vectorizer.fit_transform(tweets_username)
# Vectorise hashtags
hashtags = vectorizer.fit_transform(tweets_hashtags)
# Vectorise the text 
text = vectorizer.fit_transform(tweets_text)

# Set k (number of clusters) to 8
k = 8

# Cluster username of tweets 
model_username = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
model_username.fit(username)

# Print top 10 usernames per cluster
print("Top usernames per cluster:")
file.write("Top usernames per cluster:\n")
order_centroids = model_username.cluster_centers_.argsort()[:, ::-1]
terms_username = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in order_centroids[i, :10]:
        print (' %s' % terms_username[ind])
        file.write(' %s' % terms_username[ind])
        file.write("\n")

#print("\n")
open("Clusters.txt", "w+")

# Cluster hashtags of tweets 
model_hashtags = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
model_hashtags.fit(hashtags)

# Print top 10 usernames per cluster
print("Top hashtags per cluster:")
file.write("\nTop hashtags per cluster:\n")
order_centroids = model_hashtags.cluster_centers_.argsort()[:, ::-1]
terms_hashtags = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in order_centroids[i, :10]:
        print (' %s' % terms_hashtags[ind])
        file.write(' %s' % terms_hashtags[ind])
        file.write("\n")

print("\n")

# Cluster text of tweets 
model_text = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
model_text.fit(text)

# Print top 10 usernames per cluster
print("Top text per cluster:")
file.write("\nTop text per cluster:\n")
order_centroids = model_text.cluster_centers_.argsort()[:, ::-1]
terms_text = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in order_centroids[i, :10]:
        print (' %s' % terms_text[ind])
        file.write(' %s' % terms_text[ind])
        file.write("\n")

file.close()
