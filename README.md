<a href="https://github.com/kennethenevoldsen/asent"><img src="https://github.com/KennethEnevoldsen/asent/blob/main/docs/img/logo_black_font.png?raw=true" width="300" align="right" /></a>
# Asent: Fast, flexible and transparent sentiment analysis


[![PyPI version](https://badge.fury.io/py/asent.svg)](https://pypi.org/project/asent/)
[![python version](https://img.shields.io/badge/Python-%3E=3.9-blue)](https://github.com/kennethenevoldsen/asent)
[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
[![github actions pytest](https://github.com/kennethenevoldsen/asent/actions/workflows/tests.yml/badge.svg)](https://github.com/kennethenevoldsen/asent/actions)
[![github actions docs](https://github.com/kennethenevoldsen/asent/actions/workflows/documentation.yml/badge.svg)](https://kennethenevoldsen.github.io/asent/)
[![pip downloads](https://img.shields.io/pypi/dm/asent.svg)](https://pypi.org/project/asent/)


Asent is a rule-based sentiment analysis library for Python made using [SpaCy](https://spacy.io). 
It is inspired by [Vader](https://github.com/cjhutto/vaderSentiment), but uses a more modular ruleset, that allows the user to change e.g. the method for finding negations. Furthermore, it includes visualizers to visualize model predictions, making the model easily interpretable.


## Installation

Installing Asent is simple using pip:

```
pip install asent
```

There is no reason to update from GitHub as the version on pypi should always be the same of on GitHub.

## Simple Example
The following shows a simple example of how you can quickly apply sentiment analysis using asent. For more on using asent see the [usage guides].

```python
import spacy
import asent

# create spacy pipeline
nlp = spacy.blank('en')
nlp.add_pipe('sentencizer')

# add the rule-based sentiment model
nlp.add_pipe("asent_en_v1")

# try an example
text = "I am not very happy, but I am also not especially sad"
doc = nlp(text)

# print polarity of document, scaled to be between -1, and 1
print(doc._.polarity)
# neg=0.0 neu=0.631 pos=0.369 compound=0.7526
```

Naturally, a simple score can be quite unsatisfying, thus Asent implements a series of visualizer to interpret the results: 
```python
# visualize model prediction
asent.visualize(doc, style="prediction")
```

<img src="https://raw.githubusercontent.com/KennethEnevoldsen/asent/main/docs/img/model_pred.png" width="500" />

If we want to know why the model comes the result it does we can use the `analysis` style:
```python
# visualize the analysis performed by the model:
asent.visualize(doc[:5], style="analysis")
```
<img src="https://raw.githubusercontent.com/KennethEnevoldsen/asent/main/docs/img/model_analysis.png" width="700" />

Where the value in the parenthesis (2.7) indicates the human-rating of the word, while
the value outside the parenthesis indicates the value accounting for the negation.
Asent also accounts for contrastive conjugations (e.g. but), casing, emoji's and
punctuations. For more on how the model works check out the [usage guide].

# 📖 Documentation

| Documentation              |                                                                                                                         |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 🔧 **[Installation]**       | Installation instructions for Asent                                                                                     |
| 📚 **[Usage Guides]**       | Guides and instructions on how to use asent and its features. It also gives short introduction to how the models works. |
| 📰 **[News and changelog]** | New additions, changes and version history.                                                                             |
| 🎛 **[Documentation]**      | The detailed reference for Asents's API. Including function documentation                                               |

[Documentation]: https://kennethenevoldsen.github.io/asent/index.html
[Installation]: https://kennethenevoldsen.github.io/asent/installation.html
[usage guides]: https://kennethenevoldsen.github.io/asent/introduction.html
[News and changelog]: https://kennethenevoldsen.github.io/asent/news.html

# 💬 Where to ask questions

| Type                           |                        |
| ------------------------------ | ---------------------- |
| 🚨 **FAQ**                      | [FAQ]                  |
| 🚨 **Bug Reports**              | [GitHub Issue Tracker] |
| 🎁 **Feature Requests & Ideas** | [GitHub Issue Tracker] |
| 👩‍💻 **Usage Questions**          | [GitHub Discussions]   |
| 🗯 **General Discussion**       | [GitHub Discussions]   |


[FAQ]: https://kennethenevoldsen.github.io/asent/faq.html
[github issue tracker]: https://github.com/kennethenevoldsen/asent/issues
[github discussions]: https://github.com/kennethenevoldsen/asent/discussions
