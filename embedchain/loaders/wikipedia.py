import logging
import wikipedia

from embedchain.loaders.base_loader import BaseLoader


class WikipediaLoader(BaseLoader):
    def load_data(self, url):
        """Load data from a wikipedia page."""

        # Extract title from the url
        title_list = url.split("/")
        title = title_list[-1].replace("_", " ", title_list[-1].count("_"))

        # Retrieve wikipedia page using the title
        try:
            page_obj = wikipedia.page(title)

            # Extract data from wikipedia page
            data = page_obj.content
            metadata = {"url": page_obj.url, "title": page_obj.title}
        except wikipedia.exceptions.DisambiguationError as e:
            logging.error(f"DisambiguationError:{e.options}")
            page_obj = None
        except wikipedia.exceptions.PageError as e:
            logging.error(f"PageError: {e}")
            page_obj = None
        if page_obj is not None:
            return [
                {
                    "content": data,
                    "meta_data": metadata,
                }
            ]
