How does the model work?
==============================

Work in progress


.. Valence:
..  1) Look up the word in the lexicon
..  2) is the word all caps while the rest of the text is not, add capitilazation factor (0.733) to the valence score

.. Token polarity
..  1) Start of with the token valence
..  2) is the word intensified? If one of the three preceeding word is an intensifier add the intensifier score times a discounting constant such that intensifier 3 tokens away are not as influential as an intensifier one token away.
..  3) is the word negated? If either of the three previous word is a negation multiply it by a negation factoer (-0.74)

.. Span or sentence polarity
.. 1) Sum and normalize the score to be typically between -1 and 1.
.. 2) If there is a contrastive conjugation (e.g. but) downweight the polarity score before and upweight the following score. E.g. "the cast was horrible, but the storyline was great", here horrible would be downweighted and great wieghted more.
.. 3) If the sentence use exclamation or question mark amplifiy the polarity scores. Dependent on how many exclamationsmarks is present.