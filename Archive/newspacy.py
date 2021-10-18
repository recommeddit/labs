import spacy

texts = ['some movies include things like Fall Out or New Vegas', 'the other movie Star Wars was very interesting']
nlp = spacy.load('en_core_web_sm')
for doc in nlp.pipe(texts):
    print([(ent.text, ent.label_) for ent in doc.ents])
