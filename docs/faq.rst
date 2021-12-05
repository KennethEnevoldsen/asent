Frequently asked questions
================================


Citing asent
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you use this library in your research, please cite it using:

.. code-block::

   @inproceedings{asent2021,
      title={Asent: Fast, flexible and transparent sentiment analysis},
      author={Enevoldsen, Kenneth and Hansen, Lasse},
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

