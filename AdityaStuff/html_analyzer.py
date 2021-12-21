# imports
import url_to_html as urlEx
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

##############################################################

redditComment = "code.visualstudio.com is the best code editor"
commentUrl = urlEx.get_url(redditComment)
resolvedUrl = urlEx.check_url(commentUrl)
parsedHtml = urlEx.html_to_text(resolvedUrl)


def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        if current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
            else:
                continue
    return continuous_chunk


keywords = []
for par in range(0, len(parsedHtml)):
    data = parsedHtml[par]
    entities = get_continuous_chunks(data)
    for ell in range(0, len(entities)):
        keywords.append(entities[ell])

print(keywords)
