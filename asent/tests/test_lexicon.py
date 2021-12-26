import asent


def test_lexicons():
    d = asent.lexicons.get("emoji_v1")
    isinstance(d, dict)

    for lexicon in asent.lexicons.get_all():
        print(lexicon)
    
    asent.register_lexicon("my_custom_lexicon", {"happy": 2, "sad": -2})
    lex = asent.lexicons.get("my_custom_lexicon")
    assert isinstance(lex, dict)