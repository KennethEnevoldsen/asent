import asent


def test_lexicons():
    d = asent.lexicons.get("emoji_v1")
    assert isinstance(d, dict)

    for lexicon in asent.lexicons.get_all():
        print(lexicon)

    asent.register_lexicon("my_custom_lexicon", {"happy": 2, "sad": -2})
    lex = asent.lexicons.get("my_custom_lexicon")
    assert isinstance(lex, dict)


def test_components():
    f = asent.components.get("asent_da_v1")
    assert callable(f)

    for _i, c in asent.components.get_all().items():
        assert callable(c)

    asent.register_component("my_custom_comp", lambda doc: doc)
    comp = asent.components.get("my_custom_comp")
    assert callable(comp)
