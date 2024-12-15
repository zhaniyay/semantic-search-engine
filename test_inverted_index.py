import tempfile
from inverted_index import load_documents, build_inverted_index, InvertedIndex


# Test for loading documents
def test_load_documents():
    sample_data = "1\tHello World\n2\tPython is great\n"
    
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        tmp.write(sample_data)
        tmp_path = tmp.name
    
    docs = load_documents(tmp_path)
    assert docs == {
        1: "Hello World",
        2: "Python is great"
    }


# Test for building inverted index
def test_build_inverted_index():
    documents = {
        1: "Hello world",
        2: "World of Python"
    }
    index = build_inverted_index(documents)

    expected_index = {
        "hello": [1],
        "world": [1, 2],
        "of": [2],
        "python": [2]
    }
    assert index.index == expected_index


# Test for querying the index
def test_query():
    index = InvertedIndex({
        "hello": [1],
        "world": [1, 2],
        "python": [2]
    })

    # Successful queries
    assert index.query(["hello", "world"]) == [1]
    assert index.query(["world"]) == [1, 2]
    assert index.query(["python"]) == [2]

    # Edge case: Word not in the index
    assert index.query(["nonexistent"]) == []

    # Edge case: Multiple missing words
    assert index.query(["missing", "words"]) == []


# Test for saving and loading the index
def test_dump_and_load():
    index = InvertedIndex({
        "hello": [1],
        "world": [1, 2]
    })

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        tmp_path = tmp.name
        index.dump(tmp_path)

    loaded_index = InvertedIndex.load(tmp_path)
    assert loaded_index.index == index.index
