from voltron.pages.shared.components.market_selector_drop_down_desktop import MarketSelectorDesktopDropDown, \
    MarketSelectorOptionDesktop
from voltron.pages.shared.contents.coupons_page import CouponPage, CouponPageDesktop, CouponPageTabContentDesktop


class CouponPageLadbrokes(CouponPage):
    _coupon_name = 'xpath=.//*[@data-crlat="titleText" or @class="of-coupon"]'


class LadbrokesMarketSelectorOptionDesktop(MarketSelectorOptionDesktop):
    _name = 'xpath=.//*[@data-crlat="dropdown.menuTitle"]'


class LadbrokesMarketSelectorDesktopDropDown(MarketSelectorDesktopDropDown):
    _list_item_type = LadbrokesMarketSelectorOptionDesktop


class LadbrokesCouponPageTabContentDesktop(CouponPageTabContentDesktop):
    _dropdown_market_selector_type = LadbrokesMarketSelectorDesktopDropDown
    _selected_market_name = 'xpath=.//*[@class="option-title"]'

    @property
    def selected_market(self):
        return self._get_webelement_text(selector=self._selected_market_name)


class CouponPageDesktopLadbrokes(CouponPageDesktop):
    _market_selector_module = 'xpath=.//*[@class="selector-wrapper"]'
    _tab_content_type = LadbrokesCouponPageTabContentDesktop
