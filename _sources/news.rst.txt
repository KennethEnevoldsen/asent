News and Changelog
==============================

* 0.1.0 (26/12/21)

  - Major updates to the documentation along with two new tutorials 📖
  - Cool new infographics 😎
  - Changes:

    * ``make_token_polarity_getter`` no longer takes the ``is_negation_getter``, but the ``is_negated_getter`` to avoid it setting the ``is_negated`` setting itself, potentially overwriting custom changes.

  - bug-fixes 🪲:

    * Lexicons is now properly installed with the package
    * Empty string no longer causes a bug
    * All extentions are now overwritten when ``force=True``
    * And many more


* 0.0.3 (05/12/21)

  - First version of asent launches
  
    * with four different languages supported, some of which have never had rule-based sentiment models 🎉
    * Tutorials allowing you to get started using and customizing your sentiment pipeline 🔧
    * Visualizers for examining the predictions of the model 🌟 
    * An extensive docuementation 📖

