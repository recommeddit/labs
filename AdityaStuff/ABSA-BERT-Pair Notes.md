Paper: https://arxiv.org/pdf/1903.09588v1.pdf
1) Source Code: https://github.com/HSLCY/ABSA-BERT-pair
2) targets are the specific entities (VSCode, Microsoft, iPhone, etc.)
3) aspects are common descriptors (price, safety, availability, location, etc.)
4) Both methods turn the task into a method of sentence pair classification and "dumb down" the input sentence into a simple sentence either in the form of a question or simple statement
5) QA = question answering | NLI = natural language inference
5) BERT-NLI performs well in aspect detection while BERT-QA performs well in sentiment classification
6) BERT-NLI-B and BERT-QA-B have best AUC in sentiment classification