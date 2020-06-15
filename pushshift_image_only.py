from pymongo import MongoClient         # To use the MongoDB database
import requests                         # To create requests
import os                               # To set environment variables
import io                               # For reading from files
import argparse                         # To accept input filenames as arguments
from google.cloud import vision         # For accessing the Vision API
from google.cloud.vision import types   # For constructing requests

# Set the API key as an environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'key.json'

# Database class, to connect to the MongoDB database
class DataBase:
    # Initialize the database
    def __init__(self):
        self.client = MongoClient('mongodb://localhost')
        self.db = self.client['Opiates_db']
        self.collection = self.db['posts']

    # Insert a post in the database
    def insert_post(self, id, author, title, date, selftext, num_comments, url, allComment, images):
        try:
            self.collection.insert_one({"_id":id, "author":author, "title":title,"selftext":selftext, "date":date,"num_comments":num_comments, "url":url, "withtext":True,
            "comments":allComment,"images":images })
        except Exception as e:
            print("ERROR: INSERTING POST")
            raise

    # Informs that the database is closed
    def close(self):
        print("Database closed")

# Create a database instance
database = DataBase()
print("Succesfully conected to the database")

#Get top 50 posts with images on the subreddit r/opiates
url="https://api.pushshift.io/reddit/search/submission/?subreddit=opiates&limit=50&post_hint=image&fields=author,created_utc,id,num_comments,title,url"
res = requests.get(url);
data_arr = res.json()['data'];

# For each post
for post in data_arr:

        # Get info
        author = post['author'];
        date = post['created_utc'];
        id = post['id'];
        num_comments = post['num_comments'];
        title = post['title'];
        url = post['url'];
        selftext=""
        print("Inserting post " + id);

        # Get comments
        comments_url="https://api.pushshift.io/reddit/comment/search/?link_id="+id+"&limit=20000"
        res_comments = requests.get(comments_url);
        comment_arr = res_comments.json()['data'];
        comment_string = " ".join(comment['body'] for comment in comment_arr);

        # Get Google Vision API features
        client = vision.ImageAnnotatorClient()
        image = types.Image()
        image.source.image_uri = url

        # OBJECTS
        object_arr=[]
        object_response = client.object_localization(image=image).localized_object_annotations
        for object_ in object_response:
            object = {"name":object_.name,"score":object_.score}
            object_arr.append(object)
        # LABELS
        label_arr=[]
        labels_response = client.label_detection(image=image)
        for label in labels_response.label_annotations:
            object = {"description":label.description,"score":label.score}
            label_arr.append(object)
        # WEB ENTITIES
        web_arr=[]
        web_response = client.web_detection(image=image).web_detection
        if web_response.web_entities:
            for entity in web_response.web_entities:
                object = {"description": entity.description, "score": entity.score}
                web_arr.append(object)
        # FACE
        face_arr=[]
        face_response = client.face_detection(image=image)
        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')
        faces = face_response.face_annotations
        for face in faces:
            object = {"anger": likelihood_name[face.anger_likelihood],
                        "joy": likelihood_name[face.joy_likelihood],
                        "sorrow": likelihood_name[face.sorrow_likelihood],
                        "surprise": likelihood_name[face.surprise_likelihood]}
            face_arr.append(object)

        # LOGO
        logo_arr=[]
        logo_response = client.logo_detection(image=image)
        logos = logo_response.logo_annotations
        for logo in logos:
            object = {"description": logo.description}
            logo_arr.append(object)

        # TEXT
        text=""
        text_response = client.text_detection(image=image)
        texts = text_response.text_annotations
        if(len(texts)>0):
            text=texts[0].description

        # Construct the image dictionary and insert it in a list
        image = {"url":url, "objects":object_arr, "labels":label_arr, "web_entities": web_arr, "faces": face_arr,"logos": logo_arr, "text":text}
        images= [image]

        # Insert the post in the the MongoDB database
        database.insert_post(id,author,title,date,selftext,num_comments,url,comment_string,images);
