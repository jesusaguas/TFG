import pymongo
import requests
import re
from sklearn.externals import joblib

# This function returns the unigrams and bigram found in the string 'text'
def get_unigrams_and_bigrams(text):
    s = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    # Break sentence in the token, remove empty tokens
    tokens = [token for token in s.split(" ") if token != ""]
#     Use the zip function to generate n-grams
#     Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(2)])
    bigrams = ([" ".join(ngram) for ngram in ngrams])

    return (set(tokens + bigrams))

# This function returns the categories and its key words in the string 'text'
def find_dui_categories_and_terms(dui_terms,text):
    ngrams = get_unigrams_and_bigrams(text)
    category_count_dic = {}
    category_term_dic = {}
    for category in dui_terms:
        common_terms = (set(dui_terms[category]).intersection(ngrams))
        if len(common_terms)>0:
            category_count_dic[category] = len(common_terms)
            category_term_dic[category] = common_terms

    return category_count_dic, category_term_dic



if __name__ == "__main__":

    # MongoDB connection
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Opiates_db"]
    mycol = mydb["posts"]

    #load pickled dictionary
    dui_terms = joblib.load('dui_terms.pkl')

    # We are going to write on 'data.txt'
    f = open("data.txt", "w")

    # Get all the Google Vision API data about the posts
    for x in mycol.find():
        text=x["title"]+' '+x["selftext"]+' '+x["comments"]
        document=""
        for image in x["images"]:
            for object in image.get("objects"):
                document=document+' '+object.get("name")
            for label in image.get("labels"):
                document=document+' '+label.get("description")
            for entity in image.get("web_entities"):
                document=document+' '+entity.get("description")
            for logo in image.get("logos"):
                document=document+' '+logo.get("description")
            #document=document + (image.get("text")).replace('\n',' ')

        # Do the DUI analysis with the title,text and comments from the post
        dui_category_count, dui_category_terms = find_dui_categories_and_terms(dui_terms,text)
        for cat in dui_category_count:
            document=document+' '+cat+repr(dui_category_terms[cat]).replace("{"," ").replace("}"," ").replace("\'"," ")

        # Write the combined data about the post on the 'data.txt' file
        f.write(document+'\n')

    f.close()
