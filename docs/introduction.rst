Getting started
==================

.. |colab_tut| image:: https://colab.research.google.com/assets/colab-badge.svg
   :width: 140pt
   :target: https://colab.research.google.com/github/kennethenevoldsen/asent/blob/main/docs/tutorials/introduction.ipynb

|colab_tut|


Asent is a package for fast and transparent sentiment analysis. The package applied uses a dictionary of
words rated as either positive or negative and a series of rules to determine whether a word,
sentence or a document is positive or negative. The current rules account for negations (i.e.
"not happy"), intensifiers ("very happy") and account for contrastive conjugations (i.e. "but")
as well as other emphasis markers such as exclamation marks, casing and question marks. The following
will take you through how the sentiment is calculated in a step by step fashion.

To start of with we will need a spaCy pipeline as well as we will need to add the asent pipeline to it.




.. tab-set::

    .. tab-item:: English

         For English we can add the :code:`asent_en_v1` to it, where :code:`en` indicates that it is the English pipeline and  :code:`v1` indicate
         that it is version 1.


         .. code-block:: python

            import asent
            import spacy

            # load spacy pipeline
            nlp = spacy.load("en_core_web_lg")

            # add the rule-based sentiment model
            nlp.add_pipe("asent_en_v1")

         .. note::

            You will need to install the spaCy pipeline beforehand it can be installed using the following command:

            .. code-block:: bash

               python -m spacy download en_core_web_lg


    .. tab-item:: Danish

         For Danish we can add the :code:`asent_da_v1` to it, where :code:`da` indicates that it is the Danish pipeline and  :code:`v1` indicate
         that it is version 1.


         .. code-block:: python

            import asent
            import spacy

            # load spacy pipeline
            nlp = spacy.load("da_core_news_lg")

            # add the rule-based sentiment model
            nlp.add_pipe("asent_da_v1")

         .. note::

            You will need to install the spaCy pipeline beforehand it can be installed using the following command:

            .. code-block:: bash

               python -m spacy download da_core_news_lg



    .. tab-item:: Norwegian

         For Norwegian we can add the :code:`asent_no_v1` to it, where :code:`no` indicates that it is the Norwegian pipeline and  :code:`v1` indicate
         that it is version 1.


         .. code-block:: python

            import asent
            import spacy

            # load spacy pipeline
            nlp = spacy.load("nb_core_news_lg")

            # add the rule-based sentiment model
            nlp.add_pipe("asent_no_v1")

         .. note::

            You will need to install the spaCy pipeline beforehand it can be installed using the following command:

            .. code-block:: bash

               python -m spacy download nb_core_news_lg


    .. tab-item:: Swedish

         For Swedish we can add the :code:`asent_se_v1` to it, where :code:`se` indicates that it is the Swedish pipeline and  :code:`v1` indicate
         that it is version 1.


         .. code-block:: python

            import asent
            import spacy

            # load spacy pipeline
            nlp = spacy.load("sv_core_news_sm")

            # add the rule-based sentiment model
            nlp.add_pipe("asent_sv_v1")

            



Token valence and polarity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As seen in the following. token valence is simply the value gained from a lookup in a rated dictionary.
For instance if the have the example sentence `"I am not very happy"` the word `"happy"`` have a positive
human rating of 2.7 which is not amplified by the word being in all-caps.


.. image:: https://raw.githubusercontent.com/KennethEnevoldsen/asent/main/docs/img/token_polarity.png
  :width: 800
  :alt: Calculation of token polarity and valence


We can extract valence quite easily using the `valence` extension:


.. code-block:: python

   doc = nlp("I am not very happy.")

   for token in doc:
      print(token, "\t", token._.valence)


.. code-block:: text
   
   I     0.0
   am    0.0
   not   0.0
   very  0.0
   happy 2.7
   .     0.0


.. seealso::

   Want to know more about the where these rated dictionaries come from?
   Check `Languages <https://kennethenevoldsen.github.io/asent/languages/index.html>`__ 
   to see the lexical resources used for each language.


Naturally, in this context happy should not be perceived positively as it is negated,
thus we should look at token polarity. Token polarity examines if a word is negated
and it so multiplies the values by a negative constant. This constant is emperically
derived to be 0.74 `(Hutto and Gilbert, 2014) <https://ojs.aaai.org/index.php/ICWSM/article/view/14550>`__. 
Similarly, with the specific example we chose we can also see that `"happy"`` is intensified by 
the word `"very"`, while increases it polarity. The constant 0.293 is similarly emperically 
derived by Hutto and Gilbert. We can similarly extract the polarity using the `polarity` extension:

.. code-block:: python

   for token in doc:
      print(token._.polarity)

.. code-block:: text

   polarity=0.0 token=I span=I
   polarity=0.0 token=am span=am
   polarity=0.0 token=not span=not
   polarity=0.0 token=very span=very
   polarity=-2.215 token=happy span=not very happy
   polarity=0.0 token=. span=.

Notice that here we even get further information, that token `"happy"`,
has a polarity of -2.215 and that this includes the span (sequence of tokens) 
`"not very happy"`.

Visualizing polarity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Asent also includes a series of methods to visualize the token polarity:

.. code-block:: python

   doc = nlp("I am not very happy, but aslo not very especially sad")
   asent.visualize(doc, style="prediction")

.. image:: https://raw.githubusercontent.com/KennethEnevoldsen/asent/main/docs/img/model_pred.png
  :width: 600
  :alt: Model prediction

You can even get more information about why the token has the polarity by plotting the model analysis:

.. code-block:: python

   asent.visualize(doc[:5], style="analysis")

.. image:: https://raw.githubusercontent.com/KennethEnevoldsen/asent/main/docs/img/model_analysis1.png
  :width: 600
  :alt: Model analysis



Document and Span Polarity
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We want to do more than simply calculate the polarity of the token, we want to extract
information about the entire sentence (span) and aggregate this across the entire document.

.. image:: https://raw.githubusercontent.com/KennethEnevoldsen/asent/main/docs/img/doc_polarity.png
  :width: 600
  :alt: Calculation of document polarity

The calculation of the sentence polarity includes a couple of steps. 
First, it checks if the sentence contains a contrastive conjugation (e.g. "but"), 
then overweight words after the but and underweight previous elements. 
This seems quite natural for example the sentence "The movie was great, 
but the acting was horrible", noticeably put more weight on the second statement. 
This has also been shown empirically by `(Hutto and Gilbert, 2014) <https://ojs.aaai.org/index.php/ICWSM/article/view/14550>`__.
Afterwards, the model takes into account question marks and exclamation marks, which both increases
the polarity of the sentence with negative sentences becoming more negative and positive sentences
becoming more positive. Lastly, the polarity is normalized between approximately -1 and 1.

You can easily extract the sentence polarity and the document polarity using: 

.. code-block:: python

   doc = nlp("I am not very happy.")
   
   for sentence in doc.sents:
      print(sentence._.polarity)
   
.. code-block:: text

   neg=0.391 neu=0.609 pos=0.0 compound=-0.4964 span=I am not very happy.

Here we see the normalized score for both the :code:`compound`, or aggregated, polarity as well
the the neutral :code:`neu`, negative :code:`neg`, and positive :code:`pos`.