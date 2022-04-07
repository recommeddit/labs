from doctest import DocTestSuite
from http import client
from google.cloud import firestore
import base64
import datetime
from datetime import date, timedelta

db = firestore.Client(project='recommeddit')



def validate(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)



google_results = ["url example1","url example2","url example3"]
#should equal to a list of reddit Urls

#actual code for function itself 
date_30_days_ago = datetime.datetime.now(tz=datetime.timezone.utc) - datetime.timedelta(days=30)
queries_doc = db.collection('queries').where("lastValidated","<=",date_30_days_ago).get() #checks to see if queries are older than 30 days, 
for doc in queries_doc:
    doc_id = doc.id
    doc_ref = db.collection('queries').document(doc_id).get({'googleResults'}).to_dict()
    for value in doc_ref.values(): 
        if value == google_results: #checks if the google_results (list of reddit urls) are the same as the current results.
            db.collection('queries').document(doc_id).update({'lastValidated':datetime.datetime.now(tz=datetime.timezone.utc)}) #date.time gets updated if same results
        else:
            db.collection('queries').document(doc_id).delete() #query document is deleted if different results

