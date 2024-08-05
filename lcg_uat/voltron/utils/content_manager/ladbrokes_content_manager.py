from voltron.pages.ladbrokes.contents.login import Login
from voltron.pages.shared import get_driver
from voltron.utils.content_manager.bma_content_manager import BMAContentManager
from voltron.pages.shared.contents.my_bets.open_bets.open_bets import OpenBets
from voltron.pages.ladbrokes.components.the_grid import TheGrid, InShopCoupons


class LadbrokesContentManager(BMAContentManager):

    def __init__(self):
        super(LadbrokesContentManager, self).__init__()
        self._driver = get_driver()

    lad_pages = {
        'open-bets': {
            'default_page': OpenBets
        },
        'login': {
            'default_page': Login
        },
        'retail': {
            'default_page': TheGrid
        },
        'digital-coupons': {
            'default_page': InShopCoupons
        },
    }

    @property
    def pages(self):
        BMAContentManager.pages.update(self.lad_pages)
        return BMAContentManager.pages
