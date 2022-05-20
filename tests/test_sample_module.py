"""Tests for the cdstemplate.sample_module methods and classes.

In pytest, each individual test is a python function that starts with `test`.
"""
# Import your library for testing
from cdstemplate import sample_module


def test_tokenize_document():
    my_document = "It was all very well to say `Drink me,' but the wise little Alice was not going to do that in a hurry."

    expected_tokens = [
        "It",
        "was",
        "all",
        "very",
        "well",
        "to",
        "say",
        "`Drink",
        "me,'",
        "but",
        "the",
        "wise",
        "little",
        "Alice",
        "was",
        "not",
        "going",
        "to",
        "do",
        "that",
        "in",
        "a",
        "hurry.",
    ]

    assert sample_module.tokenize(my_document) == expected_tokens


def test_tokenize_change_pattern():
    formatted_document = "here's-a-document-with-strange-formatting"
    expected_tokens = ["here's", "a", "document", "with", "strange", "formatting"]
    assert sample_module.tokenize(formatted_document, pattern="-") == expected_tokens


def test_corpus_counter_init():
    cc = sample_module.CorpusCounter()
    assert cc.doc_counter == 0
    assert cc.get_token_count("word") == 0
    assert cc.case_insensitive == False
    assert cc.tokenization_pattern == r"\s"


def test_corpus_counter_add_docs():
    cc = sample_module.CorpusCounter()
    cc.add_doc("a b a word")
    assert cc.doc_counter == 1
    assert cc.get_token_count("a") == 2
    assert cc.get_token_count("b") == 1
    assert cc.get_token_count("word") == 1
    cc.add_tokenized_doc(["Word", "word", "b"])
    assert cc.get_token_count("a") == 2
    assert cc.get_token_count("b") == 2
    assert cc.get_token_count("word") == 2
    assert cc.get_token_count("Word") == 1


def test_corpus_counter_add_empty_doc():
    cc = sample_module.CorpusCounter()
    cc.add_doc("")
    assert cc.doc_counter == 1
    assert len(cc.token_counter) == 0


def test_corpus_counter_case_insensitive():
    cc = sample_module.CorpusCounter(case_insensitive=True)
    cc.add_doc("A a B b")
    assert cc.get_token_count("a") == 2
    assert cc.get_token_count("b") == 2
    assert cc.get_token_count("A") == 0
    assert cc.get_token_count("B") == 0


# The tmp_path fixture allows you save results to a temporary directory
# that will automatically be cleaned up by the OS later
def test_corpus_counter_save_csv(tmp_path):
    my_csv = tmp_path / "token_count.csv"
    cc = sample_module.CorpusCounter()
    cc.add_doc("a b c")
    cc.add_doc("a x y z")
    cc.save_token_counts(my_csv)
    assert my_csv.exists()
    assert my_csv.is_file()
    expected_csv = "token,count\na,2\nb,1\nc,1\nx,1\ny,1\nz,1\n"
    assert my_csv.read_text() == expected_csv
