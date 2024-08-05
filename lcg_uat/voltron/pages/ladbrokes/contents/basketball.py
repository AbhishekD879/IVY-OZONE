from voltron.pages.ladbrokes.contents.base_contents.sport_base import LadbrokesSportPageBase, \
    LadbrokesDesktopSportPageBase


class LadbrokesMobileBasketball(LadbrokesSportPageBase):
    _url_pattern = r'^https?:\/\/.+\/basketball(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'


class LadbrokesDesktopBasketball(LadbrokesDesktopSportPageBase):
    _url_pattern = r'^https?:\/\/.+\/basketball(\/)?(live|matches|competitions|specials|coupons|outrights)?(\/)?(today|tomorrow|future)?'
