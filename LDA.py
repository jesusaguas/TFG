from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import NMF, LatentDirichletAllocation

no_topics = 10          # Number of Topics in the analysis
no_top_words = 10       # Number of Top words shown for each topic

# This function displays the topics of the LDA analysis
def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print ("Topic %d:" % (topic_idx+1))
        print (" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

# Read the dataset and create the list of documents
fh = open("data.txt","r")
documents=[]
for line in fh:
    documents.append(line)
fh.close()


# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
no_features = 1000
tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=no_features, stop_words='english')
tf = tf_vectorizer.fit_transform(documents)
tf_feature_names = tf_vectorizer.get_feature_names()

# Run LDA
lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)

# Show topics and top words for each topic
print("\nLDA: ")
display_topics(lda, tf_feature_names, no_top_words)
