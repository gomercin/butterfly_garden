from butterfly_graph.hashing import canonical_json_hash, sha256_text


def test_sha256_text_is_stable():
    assert sha256_text("abc") == sha256_text("abc")


def test_canonical_json_hash_ignores_key_order():
    assert canonical_json_hash({"a": 1, "b": 2}) == canonical_json_hash({"b": 2, "a": 1})
