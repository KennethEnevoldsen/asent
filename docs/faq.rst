Frequently asked questions
================================


Citing asent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you use this library in your research, please cite it using:

.. code-block::

   @inproceedings{asent2021,
      title={Asent: Fast, flexible and transparent sentiment analysis},
      author={Enevoldsen, Kenneth},
      year={2021}
   }


How do I test the code and run the test suite?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

asent comes with an extensive test suite. In order to run the tests,
you'll usually want to clone the repository and build asent from the
source. This will also install the required development dependencies
and test utilities defined in the `requirements.txt <https://github.com/KennethEnevoldsen/asent/blob/master/requirements.txt>`__.


.. code-block:: bash

   pip install -r requirements.txt
   pip install pytest

   python -m pytest


which will run all the test in the `asent/tests` folder.

Specific tests can be run using:

.. code-block:: bash

   python -m pytest asent/tests/desired_test.py



How is the documentation generated?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Asent uses `sphinx <https://www.sphinx-doc.org/en/master/index.html>`__ to generate
documentation. It uses the `Furo <https://github.com/pradyunsg/furo>`__ theme
with custom styling.

To make the documentation you can run:

.. code-block:: bash

   # install sphinx, themes and extensions
   pip install sphinx furo sphinx-copybutton sphinxext-opengraph

   # generate html from documentations

   make -C docs html


How do I add a new language?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check out the `customizing Asent <https://kennethenevoldsen.github.io/asent/customizing.html>`__ guide it gives an example of how to add a new language.
Once you have added we would very much appreciate a pull request with your new language.


Couldn't you just train a transformer for this?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is true that a trained transformer would probably perform sentence-level sentiment analysis much better. However, this modular approach to sentiment analysis
allows a more fine-grained sentiment analysis, as would for example be done in aspect-based sentiment analysis. This too, however, could be done using neural architectures.
The goal of Asent it not to exclude such approaches (in fact it can use transformer-based models  through spaCy) but to combine them in a way that allow the end user to examine the results.