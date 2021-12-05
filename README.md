<a href="https://github.com/kennethenevoldsen/asent"><img src="https://github.com/KennethEnevoldsen/asent/blob/master/docs/img/logo_red_font.png?raw=true" width="200" align="right" /></a>
# Asent: Fast, flexible and transparent sentiment analysis


[![PyPI version](https://badge.fury.io/py/asent.svg)](https://pypi.org/project/asent/)
[![python version](https://img.shields.io/badge/Python-%3E=3.7-blue)](https://github.com/kennethenevoldsen/asent)
[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
[![github actions pytest](https://github.com/kennethenevoldsen/asent/actions/workflows/pytest-cov-comment.yml/badge.svg)](https://github.com/kennethenevoldsen/asent/actions)
[![github actions docs](https://github.com/kennethenevoldsen/asent/actions/workflows/documentation.yml/badge.svg)](https://kennethenevoldsen.github.io/asent/)
![github coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/KennethEnevoldsen/2d5c14e682c3560240fe05cc7c9f4d2d/raw/badge-asent-pytest-coverage.json)
[![CodeFactor](https://www.codefactor.io/repository/github/kennethenevoldsen/asent/badge)](https://www.codefactor.io/repository/github/kennethenevoldsen/asent)
[![pip downloads](https://img.shields.io/pypi/dm/asent.svg)](https://pypi.org/project/asent/)
<!-- [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/kennethenevoldsen/asent/dev/streamlit.py) -->


Inspired by Vader, made using SpaCy, transparent from the start.


## Simple Example
The following shows a simple example of how you can quickly apply sentiment analysis using asent. For more on using asent see the [usage guides].

```python
import spacy
import asent

# load spacy pipeline
nlp = spacy.load("da_core_news_lg")

# add the rule-based sentiment model
nlp.add_pipe("asent_da_v1")

# try an example
text = "jeg er ikke længere sur. 👿"
doc = nlp(text)

# visualize the results
asent.visualize(doc)
```

## 📖 Documentation

| Documentation              |                                                                             |
| -------------------------- | --------------------------------------------------------------------------- |
| 📚 **[Usage Guides]**       | Guides and instructions on how to use asent and its features.               |
| 📰 **[News and changelog]** | New additions, changes and version history.                                 |
| 🎛 **[Documentations]**     | The detailed reference for augmenty's API. Including function documentation |


[usage guides]: https://kennethenevoldsen.github.io/asent/introduction.html
[api references]: https://kennethenevoldsen.github.io/asent/
[Demo]: https://share.streamlit.io/kennethenevoldsen/augmenty/dev/streamlit.py
[News and changelog]: https://kennethenevoldsen.github.io/augmenty/news.html

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
python -m pytest augmenty/tests/desired_test.py
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

  asent uses [sphinx](https://www.sphinx-doc.org/en/master/index.html) to generate documentation. It uses the [Furo](https://github.com/pradyunsg/furo) theme with a custom styling.

  To make the documentation you can run:
  
  ```
  # install sphinx, themes and extensions
  pip install sphinx furo sphinx-copybutton sphinxext-opengraph

  # generate html from documentations

  make -C docs html
  ```
  
</details>


<br /> 
