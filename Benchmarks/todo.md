# Small steps
- [ ] convert pipeline to setters to avoid overwriting attributes
  - [ ] really only the buttom part should be replaced the other parts should be dynamic
  - [ ] Make the getter dynamic such that they store the attribute in e.g. ._.valence (i.e. things that should be able to be overwritten)
    - [ ] valence, intensifiers, getter, span
- [ ] redo dict to match patterns
- [ ] 

https://github.com/explosion/spaCy/blob/dfb23a419ee0410f5ef0ce8ebd8b031cd5790e2d/website/docs/usage/v2-3.md#user-content-load-and-save-extra-prob-lookups-table:~:text=If%20you'd%20like%20to%20include%20custom%20cluster%2C%20prob%2C%20or%20sentiment%20tables%20as


# Ordered list
- [ ] Convert danish dict to Token matches
- [ ] Use matches to set tokens attributes
- [ ] 


# Comparative analysis
- [x] Examine datapoints
- [x] Confusion matrix over performance

Performance seems to never be quite good as dictionary-based sentiment analysis, rarely is. However a better approach might to create a new dataset which more reasonably represent what I want the model to do (not what other want it to do).

What is that:
- 1) Derive positive/negative sentiment about an entity
- 2) Aspect-based sentiment
- 3) Given a positive/negative statement can confidently say what it is about 
 
# redo Asent
- [ ] Use matchers
- [ ] Use setters instead of getters
- [ ] Redo benchmark using spacy examples
- [ ] Redo lexicons according to catalogue suggestions? (such that it has a make instead of just loading in everything)

# improve docs:
- [ ] Add table of set values

Lav streamlit app over eksempler

# Fixing the grid search
- [ ] redo the grid script such that the grid is a list of runs which each contain a triplet of obj, ext, func
- [ ] create a function to set all the getters, with default for the rest to reset them

# Create pattern estimator for dataset


# Notes
What words are relevant? 

- Positive or negative adjectives
- "skældsord"
- "ordssprog"
- 

# Design pattern for pipeline

```
class Asent(nlp: Language,
        name: str = "asent",
        lexicon: Dict[str, float],
        intensifiers: Dict[str, float] = {},
        negations: Iterable[str] = set(),
        contrastive_conjugations: Iterable[str] = set(),
        lowercase: bool = True,
        lemmatize: bool = False,
        force: bool = False,
    )
```

```
pipe = class Asent(nlp: Language,
        name: str = "asent",
        valence,
        polarity,
        intensifiers,
        negations,
        cconj,
        span_polarity,
        doc_polarity,
        force: bool = False,
    )
pipe.replace("valence", new_valence_getter)
pipe.replace("polarity", new_valence_getter)
# error polarity is set for both, Token span and doc, please specify 
pipe.replace("polarity", setter=span_polarity_setter, container="Span")
```
# Create a pipeline visualizer like:

https://huggingface.co/spaces/spacy/pipeline-visualizer


# create an internal atrribute that keeps the list of highlights
Token.set_extension('_hl', default=list())

def get_highlights(token):
    # get highlights from internal attribute
    return [(start, end, token.text[start:end]) for start, end in token._._hl]

def set_highlight(token, value):
    # append value to existing list
    token._._hl.append(value)

# user-facing attribute used for getting and setting
Token.set_extension('highlight', getter=get_highlights, setter=set_highlight)

# Ask rebekkah about
