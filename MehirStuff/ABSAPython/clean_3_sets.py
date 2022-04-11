import json, random, argparse
from os import listdir, system
import spacy
nlp = spacy.load('en_core_web_sm', disable=['tok2vec','tagger','parser', 'ner', 'attribute_ruler', 'lemmatizer'])

""" GLOBALS """
MAX_SEQ_LENGTH = 85

def json_to_terms(j):
    """
    Converts preparsed json data to terms to print in array form
    """
    d = j['1']
    terms = []
    for comment in d:
        arr = comment['rvarr']
        sentence = []
        entities = []  # (position, entity, sentiment)
        comment_terms = []  # list of associated data
        tokens = 0
        for pos, token in enumerate(arr):
            tokens += sum(1 for tok in nlp(token['tk']))
            if tokens > MAX_SEQ_LENGTH:
                break
            token['tk'] = token['tk'].replace('$T$', ' ').replace('\n', '. ')
            sentence.append(token['tk'])
            if 'aspect' in token and 'sentiment' in token:
                entities.append([pos, token['tk'], token['sentiment']])
        if not entities: 
            continue
        for ent in entities:
            s = sentence.copy()
            s[ent[0]] = '$T$'
            if ent[2] == 'Pos':
                ent[2] = '1'
            elif ent[2] == 'Neg':
                ent[2] = '-1'
            else:
                ent[2] = '0'
            comment_terms.append([' '.join(s), ent[1], ent[2]])
        terms.append(comment_terms)        
    return terms

def print_terms(terms, outfile):
    """
    Prints data given terms from json_to_terms output
    """
    with open(outfile, 'w') as f:
        for comment_term in terms:
            for term in comment_term:
                print(term[0], term[1], term[2], sep='\n', end='\n', file=f)

def load_json(infile):
    """
    Loads json file given string
    """
    with open(infile, 'r') as f:
        return json.load(f)

def main():
    """
    Provided the given options, perform data cleaning
    """
    # Options
    parser = argparse.ArgumentParser(description='Converts PyAbsa .json data into .raw format')
    parser.add_argument('--files', default='../rawDataFiles/', type=str, help='Directory with _only_ json files (default rawDataFiles)')
    parser.add_argument('--trainprop', default=0.9, type=float, help='Proportion of train data (default 0.1)')
    parser.add_argument('--trainfile', default='./docker/pyabsa_files/datasets/custom/train.raw', type=str, help='Location to output training data (default cleanDataFiles/train.raw')
    parser.add_argument('--testfile', default='./docker/pyabsa_files/datasets/custom/test.raw', type=str, help='Location to output testing data (default cleanDataFiles/test.raw')
    args = parser.parse_args()

    # Get all json files
    all_files = [''.join([args.files, f])for f in listdir(args.files)]
    print('Fetching files from:', args.files)
    print('Saving files to', args.trainfile, 'and', args.testfile)
    print('Number of files to stitch:', len(all_files))

    # Compile all terms
    all_terms = []
    for f in all_files:
        j = load_json(f)
        terms = json_to_terms(j)
        all_terms.extend(terms)

    print('Number of input terms:', len(all_terms))
    print('Train ratio:', args.trainprop)
    
    # Print and distribute into different files
    random.shuffle(all_terms)
    print_terms(all_terms[:round(len(all_terms) * args.trainprop)], args.trainfile)
    print_terms(all_terms[round(len(all_terms) * args.trainprop):], args.testfile)

    print('Building dependency graphs...')
    # Build dependency graphs
    system(f'python3 ./docker/pyabsa_files/dependency_graph.py --dataset {args.trainfile}')
    system(f'python3 ./docker/pyabsa_files/dependency_graph.py --dataset {args.testfile}')

    print('Finished!')

if __name__ == '__main__':
    main()
