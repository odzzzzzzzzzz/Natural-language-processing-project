from src.utils.data_loader import list_opinions, load_opinion_text, iter_paragraphs


RAW_DIR = "data/raw/1K_scotus"


def test_list_opinions_returns_known_ids():
    opinions = list_opinions(RAW_DIR)
    assert "118034" in opinions
    assert "108632" in opinions
    assert "118384" in opinions
    assert opinions == sorted(opinions)


def test_load_opinion_text_returns_clean_text():
    text = load_opinion_text("118034", RAW_DIR)
    assert isinstance(text, str)
    assert len(text) > 200
    assert "<citation" not in text
    assert "<NAME" not in text


def test_iter_paragraphs_returns_nonempty_paragraphs():
    text = load_opinion_text("118034", RAW_DIR)
    paragraphs = list(iter_paragraphs(text))
    assert len(paragraphs) > 0
    assert all(isinstance(p, str) and p.strip() for p in paragraphs)
