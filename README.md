<a href="https://github.com/kennethenevoldsen/asent"><img src="https://github.com/KennethEnevoldsen/asent/blob/main/docs/img/logo_black_font.png?raw=true" width="300" align="right" /></a>
# Asent: Fast, flexible and transparent sentiment analysis


[![PyPI version](https://badge.fury.io/py/asent.svg)](https://pypi.org/project/asent/)
[![python version](https://img.shields.io/badge/Python-%3E=3.7-blue)](https://github.com/kennethenevoldsen/asent)
[![Code style: black](https://img.shields.io/badge/Code%20Style-Black-black)](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html)
[![github actions pytest](https://github.com/kennethenevoldsen/asent/actions/workflows/pytest-cov-comment.yml/badge.svg)](https://github.com/kennethenevoldsen/asent/actions)
[![github actions docs](https://github.com/kennethenevoldsen/asent/actions/workflows/documentation.yml/badge.svg)](https://kennethenevoldsen.github.io/asent/)
![github coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/KennethEnevoldsen/95471fd640b6c1c09717c5f88e2e9fae/raw/badge-asent-pytest-coverage.json)
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
| 🚨 **FAQ**              | [FAQ] |
| 🚨 **Bug Reports**              | [GitHub Issue Tracker] |
| 🎁 **Feature Requests & Ideas** | [GitHub Issue Tracker] |
| 👩‍💻 **Usage Questions**          | [GitHub Discussions]   |
| 🗯 **General Discussion**       | [GitHub Discussions]   |


[FAQ]: https://kennethenevoldsen.github.io/augmenty/faq.html
[github issue tracker]: https://github.com/kennethenevoldsen/asent/issues
[github discussions]: https://github.com/kennethenevoldsen/asent/discussions

## 🎓 Citing asent

If you use this library in your research, please cite it using:

```
@inproceedings{asent2021,
  title={Asent: Fast, flexible and transparent sentiment analysis},
  author={Enevoldsen, Kenneth and Hansen, Lasse},
  year={2021}
}
```