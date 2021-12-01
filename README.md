# Asent
A python package for flexible and transparent sentiment analysis.

Inspired by Vader, made using SpaCy, by default interpretable.


# Tutorial

simple usage on texts

```
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("asent_en_v1") 

text = "I am angry 😄"
doc = nlp(text)
doc._.polarity
```

visualize results
```
asent.visaulize(doc)
```

or if you have a long text it might be ideal to split it up into sentences.

```
text = "The plot was good, but the characters are uncompelling. The dialog on the other hand is great."

doc = nlp(text)
sentences = [sentence for sentence in doc.sents]

asent.visualize(sentences[0]) # visualize only the first sentence
```

# Correcting a model or building a new
- colab tutorial


# Available attributes

# Available Models
reference to Lexicons


# How does the model work?

Valence:
 1) Look up the word in the lexicon
 2) is the word all caps while the rest of the text is not, add capitilazation factor (0.733) to the valence score

Token polarity
 1) Start of with the token valence
 2) is the word intensified? If one of the three preceeding word is an intensifier add the intensifier score times a discounting constant such that intensifier 3 tokens away are not as influential as an intensifier one token away.
 3) is the word negated? If either of the three previous word is a negation multiply it by a negation factoer (-0.74)

Span or sentence polarity
1) Sum and normalize the score to be typically between -1 and 1.
2) If there is a contrastive conjugation (e.g. but) downweight the polarity score before and upweight the following score. E.g. "the cast was horrible, but the storyline was great", here horrible would be downweighted and great wieghted more.
3) If the sentence use exclamation or question mark amplifiy the polarity scores. Dependent on how many exclamationsmarks is present.

# FAQ


<details>
  <summary>How do I test the code and run the test suite?</summary>


asent comes with an extensive test suite. In order to run the tests, you'll usually want to clone the repository and build asent from the source. This will also install the required development dependencies and test utilities defined in the requirements.txt.


```
pip install -r requirements.txt
pip install pytest

python -m pytest
```

which will run all the test in the `asent/tests` folder.

Specific tests can be run using:

```
python -m pytest augmenty/tests/test_docs.py
```

**Code Coverage**
If you want to check code coverage you can run the following:
```
pip install pytest-cov

python -m pytest --cov=.
```


</details>


<br /> 



<br /> 

<details>
  <summary>How is the documentation generated?</summary>

  augmenty uses [sphinx](https://www.sphinx-doc.org/en/master/index.html) to generate documentation. It uses the [Furo](https://github.com/pradyunsg/furo) theme with a custom styling.

  To make the documentation you can run:
  
  ```
  # install sphinx, themes and extensions
  pip install sphinx furo sphinx-copybutton sphinxext-opengraph

  # generate html from documentations

  make -C docs html
  ```
  
</details>


<br /> 
