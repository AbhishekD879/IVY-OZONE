from collections import OrderedDict

from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.home_page_components.desktop.byb_module import BYBModule
from voltron.pages.shared.components.home_page_components.desktop.enhanced_multiples import EnhancesDesktopMultiples
from voltron.pages.shared.components.home_page_components.desktop.featured_module import FeaturedModule
from voltron.pages.shared.components.home_page_components.desktop.inplay_live_stream_module import InPlayLiveStreamModule
from voltron.pages.shared.components.home_page_components.desktop.next_races_module import NextRaceModule
from voltron.pages.shared.components.home_page_components.desktop.private_markets_module import PrivateMarketsModule
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class DesktopHomeModules(ComponentBase):
    """Designed to behave in a similar way as tabs on mobile"""
    _enhanced_multiples = 'xpath=.//*[@data-crlat="tab.showEnhancedMultiples"][*]'
    _enhanced_multiples_type = EnhancesDesktopMultiples
    _private_markets = 'xpath=.//*[@data-crlat="tab.showPrivateMarkets"][*]'
    _private_markets_type = PrivateMarketsModule
    _inplay_live_stream = 'xpath=.//*[@data-crlat="tab.showInplay"][*]'
    _inplay_live_stream_type = InPlayLiveStreamModule
    _next_races = 'xpath=.//*[@data-crlat="tab.showNextRacesModule"][*]'
    _next_races_type = NextRaceModule
    _byb_module = 'xpath=.//*[@data-crlat="tab.showBYBModule"][*]'
    _byb_module_type = BYBModule
    _featured = 'xpath=.//*[@data-crlat="tab.showFeaturedContent"][*]'
    _featured_type = FeaturedModule
    _item = 'xpath=.//*[@data-uat="pageContent"]//*[contains(@data-crlat, "tab.show")][*]'
    _right_arrow = 'xpath=.//*[contains(@class, "action-arrow right")]'
    _left_arrow = 'xpath=.//*[contains(@class, "action-arrow left")]'

    @property
    def _module_types(self):
        return {'tab.showBYBModule': self._byb_module_type,
                'tab.showFeaturedContent': self._featured_type,
                'tab.showNextRacesModuleDesktop': self._next_races_type,
                'tab.showInplay': self._inplay_live_stream_type,
                'tab.showPrivateMarkets': self._private_markets_type,
                'tab.showEnhancedMultiples': self._enhanced_multiples_type}

    def is_enhanced_module_displayed(self, timeout=3, expected_result=True):
        return wait_for_result(lambda: self._enhanced_multiples_type(selector=self._enhanced_multiples, context=self._we, timeout=0) is not None,
                               name=f'"Enhanced Module" display status to be "{expected_result}"',
                               expected_result=expected_result,
                               bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                               timeout=timeout)

    @property
    def enhanced_module(self):
        return self._enhanced_multiples_type(selector=self._enhanced_multiples, context=self._we)

    @property
    def private_markets_module(self):
        return self._private_markets_type(selector=self._private_markets, context=self._we)

    @property
    def inplay_live_stream_module(self):
        return self._inplay_live_stream_type(selector=self._inplay_live_stream, context=self._we)

    @property
    def next_races_module(self):
        return self._next_races_type(selector=self._next_races, context=self._we)

    @property
    def byb_module(self):
        return self._byb_module_type(selector=self._byb_module, context=self._we, timeout=2)

    @property
    def featured_module(self):
        return self._featured_type(selector=self._featured, context=self._we)

    @property
    @retry(stop=stop_after_attempt(2), retry=retry_if_exception_type((StaleElementReferenceException, IndexError)),
           wait=wait_fixed(wait=5), reraise=True)
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_ordered_dict = OrderedDict()
        for module in items_we:
            module_type = self._module_types.get(module.get_attribute('data-crlat'))
            if module_type:
                list_item = module_type(web_element=module)
                if list_item.is_displayed():
                    items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict

    @property
    def right_arrow(self):
        return self._find_element_by_selector(selector=self._right_arrow, timeout=1)

    @property
    def left_arrow(self):
        return self._find_element_by_selector(selector=self._left_arrow, timeout=1)

    @property
    def has_right_arrow(self):
        return self._find_element_by_selector(selector=self._right_arrow, timeout=1) is not None

    @property
    def has_left_arrow(self):
        return self._find_element_by_selector(selector=self._left_arrow, timeout=1) is not None
