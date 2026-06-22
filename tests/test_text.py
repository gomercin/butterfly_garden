from butterfly_graph.text import clean_text, slugify


def test_clean_text():
    assert clean_text(" a\r\nb\n\n\n\nc ") == "a\nb\n\n\nc"


def test_slugify():
    assert slugify("Hello, Weird Butterfly!") == "hello-weird-butterfly"
