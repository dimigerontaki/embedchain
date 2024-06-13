from unittest.mock import patch

import pytest
import wikipedia

from embedchain.loaders.wikipedia import WikipediaLoader


@pytest.fixture
def wikipedia_loader():
    return WikipediaLoader()


def test_load_data(wikipedia_loader):
    page_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

    with patch("wikipedia.page") as mock_page:
        # Create a mock page object
        mock_page.return_value.title = "Python (programming language)"
        mock_page.return_value.url = page_url
        mock_page.return_value.content = "Python is a high-level, general-purpose programming language."

        result = wikipedia_loader.load_data(page_url)

        assert len(result) == 1
        assert mock_page.return_value.content in result[0].get("content")
        assert result[0].get("meta_data").get("url") == page_url
        assert result[0].get("meta_data").get("title") == "Python (programming language)"


def test_load_data_disambiguation_error(wikipedia_loader):
    page_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

    with patch(
        "wikipedia.page",
        side_effect=wikipedia.exceptions.DisambiguationError(
            "Python", ["Python (programming language)", "Python (mythology)"]
        ),
    ):
        result = wikipedia_loader.load_data(page_url)

        assert result is None


def test_load_data_page_error(wikipedia_loader):
    page_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

    with patch("wikipedia.page", side_effect=wikipedia.exceptions.PageError(pageid=1)):
        result = wikipedia_loader.load_data(page_url)

        assert result is None
