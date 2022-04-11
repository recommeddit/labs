import json, random, argparse
from os import listdir, system
import spacy
from spacy.tokens import Doc, Span, DocBin
nlp = spacy.load('en_core_web_sm', disable=['tok2vec','tagger','parser', 'ner', 'attribute_ruler', 'lemmatizer'])

def json_to_terms(j):
    """
    Converts preparsed json data to terms to print in array form
    """
    d = j['1']
    comments_array = []
    for comment in d:
        arr = comment['rvarr']
        raw_words = [(d['tk'], 'aspect' in d) for d in arr]
        words = []
        entities = []
        number = 0
        for word, ent_bool in raw_words:
            if word.isspace() or word == '':
                continue
            if ent_bool:
                doc = nlp(word)
                start = number
                for word in doc:
                    if word.text.isspace() or word.text == '':
                        continue
                    number += 1
                    words.append(word.text)
                entities.append((start, number))
            else:
                words.append(word)
                number += 1
        words = [word.strip() for word in words]
        try:
            doc = Doc(nlp.vocab, words)
        except:
            print(words)
        doc.set_ents([Span(doc, start, end, "REC") for start, end in entities])
        comments_array.append(doc)
    return comments_array 

def load_json(infile):
    """
    Loads json file given string
    """
    with open(infile, 'r') as f:
        return json.load(f)

def to_spacy(sentences, destination):
    db = DocBin()
    for s in sentences:
        db.add(s)
    db.to_disk(destination)

def main():
    """
    Provided the given options, perform data cleaning
    """
    # Options
    parser = argparse.ArgumentParser(description='Converts PyAbsa .json data into .raw format')
    parser.add_argument('--files', default='../rawDataFiles/', type=str, help='Directory with _only_ json files (default rawDataFiles)')
    parser.add_argument('--devprop', default=0.1, type=float, help='Proportion of dev data (default 0.1)')
    parser.add_argument('--testprop', default=0.1, type=float, help='Proportion of test data (default 0.1)')
    parser.add_argument('--trainfile', default='./train.spacy', type=str, help='Location to output training data')
    parser.add_argument('--devfile', default='./dev.spacy', type=str, help='Location to output testing data')
    parser.add_argument('--testfile', default='./test.spacy', type=str, help='Location to output test data')
    args = parser.parse_args()

    # Get all json files
    all_files = [''.join([args.files, f])for f in listdir(args.files)]
    print('Fetching files from:', args.files)
    print('Saving files to', args.trainfile, 'and', args.testfile)
    print('Number of files to stitch:', len(all_files))

    # Compile all sentences 
    all_sentences = []
    for f in all_files:
        j = load_json(f)
        sentences = json_to_terms(j)
        all_sentences.extend(sentences)

    print('Number of input terms:', len(all_sentences))
    print('Train ratio:', 1 - args.devprop - args.testprop)
    print('Dev ratio:', args.devprop)
    print('Test ratio:', args.testprop)
    
    # Print and distribute into different files
    random.shuffle(all_sentences)
    to_spacy(all_sentences[:round(len(all_sentences) * (1 - args.devprop - args.testprop))], args.trainfile)
    to_spacy(all_sentences[round(len(all_sentences) * (1 - args.devprop - args.testprop)):round(len(all_sentences) * (1- args.testprop))], args.devfile)
    to_spacy(all_sentences[round(len(all_sentences) * (1- args.testprop)):], args.testfile)

if __name__ == '__main__':
    main()
