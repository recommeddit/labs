import firebase_admin
import datetime
import asyncio
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db=firestore.client()




async def get_query_results(string_query):
    docs = db.collection('queries').where("name","==",string_query).get()
    for doc in docs:
        dict_query = doc.to_dict()
        list_query = list(dict_query.values())
        return(list_query) #returns results as list

        #id_doc = doc.id 
        #doc_ref = db.collection(u'queries').document(id_doc).get({u'entities'}).to_dict()
        #for value in doc_ref.values():
            #entities_list = [d['entity'] for d in value]
            #return(entities_list)
            #these lines above would return the actual entities fromm query in a list format if needed 
    else: 
        return None



async def get_entity(string_name):
    docx = db.collection('entities').where("name","==",string_name).get()
    for doc in docx:
        dict_ent = doc.to_dict() #returns all results of the entitiy as a dictionary
        list_ent = list(dict_ent.values())
        return(list_ent) #returns all results as list
    else: 
        return None



async def merge_entity(string_name, validCategories = [],invalidCategories = [],description = '', imageUrl = ''):
    docs = db.collection('entities').where("name","==",string_name).get()
    for doc in docs:
        ref = doc.to_dict()
        x = len(ref.keys())
        if x>0:
            key = doc.id
            db.collection('entities').document(key).set({'name':string_name,'description':description,'imageUrl':imageUrl},merge=True)
            ref = db.collection('entities').document(key)
            ref.update({u'invalidCategories':firestore.ArrayUnion([invalidCategories]),u'validCategories':firestore.ArrayUnion([validCategories])})
            break 
    else:
        db.collection('entities').add({'name':string_name,'validCategories':validCategories,'invalidCategories':invalidCategories,'description':description,'imageUrl':imageUrl})

#merges new data with specific existing entity in database
#if it doesn’t exist, the function create its



