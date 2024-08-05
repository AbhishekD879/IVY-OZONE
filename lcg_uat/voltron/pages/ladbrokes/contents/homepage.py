from voltron.pages.ladbrokes.components.base_components import LadbrokesEnhancedMultiplesTabContent
from voltron.pages.ladbrokes.components.home_page_components.desktop.desktop_home_modules import \
    LadbrokesDesktopHomeModules
from voltron.pages.ladbrokes.components.home_page_components.home_page_byb_tab import LadbrokesBYBTabContent
from voltron.pages.ladbrokes.components.home_page_components.home_page_inplay_tab import LadbrokesHomeInPlayTabContent
from voltron.pages.ladbrokes.components.home_page_components.home_page_private_markets_tab import \
    LadbrokesPrivateMarketsTabContent
from voltron.pages.ladbrokes.contents.inplay_watchlive import InPlayWatchLiveTabContentLadbrokes
from voltron.pages.ladbrokes.components.home_page_components.home_page_live_stream_tab import LadbrokesLiveStreamTabContent
from voltron.pages.shared.contents.homepage import HomePage, HomePageDesktop
from voltron.utils.waiters import wait_for_result
from voltron.pages.ladbrokes.components.fanzone_banner import FanZoneBanner


class LadbrokesHomePage(HomePage):
    _tab_content_byb_type = LadbrokesBYBTabContent
    _tab_content_in_play_type = LadbrokesHomeInPlayTabContent
    _tab_content_live_stream_type = LadbrokesLiveStreamTabContent
    _tab_content_enhanced_multiples_type = LadbrokesEnhancedMultiplesTabContent
    _tab_content_private_markets_type = LadbrokesPrivateMarketsTabContent
    _tab_content_live_stream = 'xpath=.//*[@data-crlat="tabContent"]'
    _free_ride_banner = 'xpath=.//*[contains(@class, "launch-banner-mob")]'
    _fanzone_banner = 'xpath=.//*[contains(@class, "fanzone-banner")]'
    _tab_content_watch_live_type = InPlayWatchLiveTabContentLadbrokes

    @property
    def desktop_modules(self):
        return LadbrokesDesktopHomeModules(web_element=self._we, selector=self._selector)

    def free_ride_banner(self, timeout=10):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._free_ride_banner, context=self._we, timeout=5) is not None,
                                 timeout=timeout,
                                 name='Waiting for free ride banner to display')
        if result:
            return self._find_element_by_selector(selector=self._free_ride_banner, context=self._we, timeout=5)
        else:
            return result

    def fanzone_banner(self, timeout=10):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._fanzone_banner, context=self._we, timeout=5) is not None,
                                 timeout=timeout,
                                 name='Waiting for fanzone banner to display')
        if result:
            return FanZoneBanner(selector=self._fanzone_banner, context=self._we, timeout=5)
        else:
            return result

    @property
    def _tab_content_attribute_types(self) -> dict:
        return {
            'tab.showFeaturedContent': self._tab_content_featured_type,
            'tab.showInPlayModule': self._tab_content_in_play_type,
            'tab.showInplay': self._tab_content_in_play_type,
            'tab.showWatchLiveContent': self._tab_content_live_stream_type,
            'tab.showEnhancedMultiplesModule': self._tab_content_enhanced_multiples_type,
            'tab.showCouponsModule pageContainer': self._tab_content_coupons_type,
            'tab.showTopBetsModule': self._tab_content_top_bets_type,
            'tab.showPrivateMarketsModule': self._tab_content_private_markets_type,
            'tab.showBYB': self._tab_content_byb_type
        }


class LadbrokesHomePageDesktop(HomePageDesktop):
    _free_ride_banner = 'xpath=.//*[contains(@class, "launch-banner-mob")]'
    _fanzone_banner = 'xpath=.//*[contains(@class, "fanzone-banner")]'

    def free_ride_banner(self, timeout=10):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._free_ride_banner, context=self._we, timeout=5) is not None,
                                 timeout=timeout,
                                 name='Waiting for free ride banner to display')
        if result:
            return self._find_element_by_selector(selector=self._free_ride_banner, context=self._we, timeout=5)
        else:
            return result

    def fanzone_banner(self, timeout=10):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._fanzone_banner, context=self._we, timeout=5) is not None,
                                 timeout=timeout,
                                 name='Waiting for fanzone banner to display')
        if result:
            return FanZoneBanner(selector=self._fanzone_banner, context=self._we, timeout=5)
        else:
            return result

    @property
    def desktop_modules(self):
        return LadbrokesDesktopHomeModules(web_element=self._we)
