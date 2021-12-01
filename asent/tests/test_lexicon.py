
import asent

def test_lexicons():
    d = asent.lexicons.get("emoji_v1")
    isinstance(d, dict)

    for lexicon in asent.lexicons.get_all():
        print(lexicon)
