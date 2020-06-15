# TFG
**TFG (Trabajo de Fin de Grado) de Ingeniería Informática en la Universidad de Zaragoza.**

This document will explain all the files in the submission and all the necessary
instructions for compiling the code:  


## FILES

**data.txt**: Dataset that contains the combination of the Google Vision API's
            features and the DUI categories and terms. Each line corresponds to
            a document (Reddit post).  
            
**dui_terms.pkl**: This is a files required to run the DUI Tool.

**GoogleVision_DUI.py**: This python file extracts the data from the local MongoDB
                        database about the Google Vision API data from each post
                        and the text used to perform the DUI analysis.
                        It performs the DUI analysis and combines both data
                        (Google Vision API data and DUI data) and writes it in
                        the "data.txt" file.  
                        
**pushshift_image_only.py**: This python file uses the Pushshift API to get the
                        Top 1000 image posts from the subreddit r/opiates,
                        performs a Google Vision API analysis on the posts, and
                        stores all this information in a local MongoDB database.  
                        
**pushshift_text.py**: This python file is similar to the "pushshift_image_only" but
                        instead of getting the top 1000 posts from the subreddit
                        they are read from the file "textposts.txt", this posts
                        have the characteristic of having both text and images.  
                        
**textposts.txt**: Text file that contains the id and image urls of posts of the
                    subreddit r/opiates. All this posts contains text+image.
                    Most of the posts of the project were obtained from this
                    source.  
                    
**LDA.py**: This is the main file of the project. It gets the data from the text
        file "data.txt" and performs an LDA analysis.  



## INSTRUCTIONS

To run the project you need to have the 'LDA.py' and the 'data.txt' in the same
directory. This file requires the 'scikit learn' library, so if you don't have
it already installed, you can do it executing this command:
'pip install -U scikit-learn'  

To execute the program enter >> 'python LDA.py' in your command line.
The output should be the 10 topics of the 'data.txt' file with its most relevant
key words.  

You can change the parameters of the analysis if you want.
No. Topics: Change the value of the variable on the top of the file (default:10)
No. Top words: Change the value of the variable on the top of the file (deft:10)  

Note:
All the other python files are included with purpose of showing the steps of
the project, and cannot be run directly, as you need a mongoDB database
running and a 'key.json' file in order to make requests to the Google Vision API
