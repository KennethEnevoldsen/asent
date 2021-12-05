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

## 💬 Where to ask questions

| Type                           |                        |
| ------------------------------ | ---------------------- |
| 🚨 **Bug Reports**              | [GitHub Issue Tracker] |
| 🎁 **Feature Requests & Ideas** | [GitHub Issue Tracker] |
| 👩‍💻 **Usage Questions**          | [GitHub Discussions]   |
| 🗯 **General Discussion**       | [GitHub Discussions]   |


[github issue tracker]: https://github.com/kennethenevoldsen/asent/issues
[github discussions]: https://github.com/kennethenevoldsen/asent/discussions



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
