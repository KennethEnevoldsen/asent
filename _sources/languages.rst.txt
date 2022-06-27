Languages
================================


.. tab-set::


   .. tab-item:: English

      The lexicons contain a list of rated words for English along with intensifiers, contrastive conjugations and negations.
      The words are rated by 
      `Hutto and Gilbert, (2014) <https://ojs.aaai.org/index.php/ICWSM/article/view/14550>`__.

      The lexicons contain a total of 7504 rated words, 59 negations, 84 intensifiers, and 1 contrastive conjugations.

      You can load the English lexicons using:

      .. code-block:: python

         from asent import lexicons
         rated_words = lexicons.get("lexicon_en_v1") 
         negations = lexicons.get("negations_en_v1")
         intensifiers = lexicons.get("intensifiers_en_v1")
         cconj = lexicons.get("contrastive_conj_en_v1")


   .. tab-item:: Danish


      The Danish lexical resources contain a list of rated words derived from `Afinn <https://github.com/fnielsen/afinn>`__.
      The lexicon also include intensifier, contrastive conjugations
      and negations. It includes a total of 6593 rated lemmas along with intensifier, contrastive conjugations
      and negations.

      You can load the Danish lexicons using:

      .. code-block:: python

         from asent import lexicons
         rated_words = lexicons.get("lexicon_da_afinn_v1")
         negations = lexicons.get("negations_da_v1")
         intensifiers = lexicons.get("intensifiers_da_v1")
         cconj = lexicons.get("contrastive_conj_da_v1")

      Beyond the default lexicon Asent also include a series of words rated in context by
      `Dalsgaard, Lauridsen and  Svendsen (2019) <https://tidsskrift.dk/lwo/article/view/115711>`__. Which have been lemmatized using DaCy 
      `(Enevoldsen et al., 2021) <https://github.com/centre-for-humanities-computing/DaCy>`__. This dictionary:
      
      .. code-block:: python

         rated_words = lexicons.get("lexicon_da_sentida_lemma_v1") 



   .. tab-item:: Norwegian

      The lexicons contain a list of rated words for Norwegian. The words are rated in context by Finn
      A. Nielsen as a part of his package `AFINN <https://github.com/olavski/afinn/blob/master/afinn/data/AFINN-no-165.txt>`__.
      The contrastive conjugations, negations and intensifiers have been added by `Center for Humanities Computing Aarhus <https://chcaa.io>`__.

      The lexicon includes a total of 3214 rated words along with intensifier, contrastive conjugations and negations.

      You can load the Norwegian lexicons using:

      .. code-block:: python

         from asent import lexicons
         rated_words = lexicons.get("lexicon_no_v1") 
         negations = lexicons.get("negations_no_v1")
         intensifiers = lexicons.get("intensifiers_no_v1")
         cconj = lexicons.get("contrastive_conj_no_v1")


   .. tab-item:: Swedish

      The lexicons is the same as the one used by the Swedish Vader, (`vaderSentiment-swedish <https://pypi.org/project/vaderSentiment-swedish/>`__)
      available on PyPI. 

      The lexicon includes a total of 5501 rated orthographic words as well as with intensifier, contrastive conjugations and negations.

      You can load the Swedish lexicons using:

      .. code-block:: python

         from asent import lexicons
         rated_words = lexicons.get("lexicon_se_v1") 
         negations = lexicons.get("negations_se_v1")
         intensifiers = lexicons.get("intensifiers_se_v1")


   .. tab-item:: Emoji

      The rating of emojis is created by applying Vader `(Hutto and Gilbert, 2014) <https://ojs.aaai.org/index.php/ICWSM/article/view/14550>`__ to the description of the emojis. 
      Afterwards, the scores are normalized to be between -5 and 5. 

      It contains a total of 3570 rated emojis of which 391 of them has a non-zero rating.

      You can load the Emoji lexicon using:

      .. code-block:: python

         from asent import lexicons
         rated_words = lexicons.get("emoji_v1") 