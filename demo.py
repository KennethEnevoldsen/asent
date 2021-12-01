import spacy
import asent


# load spacy pipeline
nlp = spacy.load("da_core_news_lg")

# add the rule-based sentiment model
nlp.add_pipe("asent_da_v1")  # predifined danish model, generated in asent/lang/da.py


# try an example
text = "jeg er ikke længere sur. 👿"
doc = nlp(text)
sent = [sent for sent in doc.sents][0]

# # examine performance
print(sent._.polarity)  # sentence
for token in sent:
    print(token._.valence)  # token valence score (directly from lexicon)
    print(token._.polarity)  # token polarity score (from rule-based model)


# visualize the results
asent.visualize(doc)

## Alternative way to add the model (this will be updated to be more clean, but this format should always work):
from asent.component import Asent

# this adds the arguments to the extensions to the spacy doc object.
Asent(
    nlp, lexicon={"glad": 1, "sur": -1}, negations={"ikke"}, lemmatize=False, force=True
)  # there is more arguments to add
text = "jeg er ikke sur, bare lidt højstemt"
doc = nlp(text)
asent.visualize(doc)