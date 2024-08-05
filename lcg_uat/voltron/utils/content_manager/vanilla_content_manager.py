from voltron.pages.shared import get_driver
from voltron.utils.content_manager.bma_content_manager import BMAContentManager


class VanillaContentManager(BMAContentManager):

    def __init__(self):
        super(VanillaContentManager, self).__init__()
        self._driver = get_driver()

    vanilla_pages = {

    }

    @property
    def pages(self):
        BMAContentManager.pages.update(self.vanilla_pages)
        return BMAContentManager.pages
