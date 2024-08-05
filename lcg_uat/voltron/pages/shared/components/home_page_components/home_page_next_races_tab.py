from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.racing_base_components.next4_section import Next4ColumnPanel, \
    MarketRowsItem


class HomePageNextRacesItem(Next4ColumnPanel):
    # _name = 'xpath=./preceding::h2[1]'  //these xpaths are not working
    # _full_race_links = 'xpath=./preceding::header[1]/div[2]/a'
    _ew_container = 'xpath=./preceding::div[4]/span'
    _runners = 'xpath=./following-sibling::*[@data-crlat="eventGroup"]'
    _timer = 'xpath=.//*[@data-crlat="raceCountdown"] | .//*[@class="countdown"]'
    _race_time = 'xpath=.//*[@data-crlat="raceCard.eventName"]'

    def has_timer(self, timeout=1, expected_result=True):
        self.scroll_to()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._timer,
                                                   timeout=0) is not None,
            name=f'Full race card status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def runners(self):
        """
        Represent section which contains list of runners with their new odds, and, if exists, old odds
        """
        return HomePageNextRacesRunnersContainer(selector=self._runners, context=self._we)


class HomePageNextRacesContent(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="raceHeader"]'
    _list_item_type = HomePageNextRacesItem


class HomePageExtraPlaceItem(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="raceCard.eventName"]'
    _promotion_label = 'xpath=.//*[@data-crlat="promotionIcon.EPR"]'
    _promotion_name = 'xpath=.//*[@data-crlat="event-card-text"]'
    _next_arrow = 'xpath=.//*[@data-crlat="nextArrow"]'

    @property
    def name(self):
        self.scroll_to()
        we = self._find_element_by_selector(selector=self._name, context=self._we, timeout=1)
        self.scroll_to_we(we)
        return self._get_webelement_text(we=we, timeout=2)

    def has_promotion_label(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._promotion_label, timeout=0).is_displayed(),
            expected_result=expected_result,
            timeout=timeout,
            name=f'Extra Place Module status to be {expected_result}')

    def has_promotion_label(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._next_arrow, timeout=0).is_displayed(),
            expected_result=expected_result,
            timeout=timeout,
            name=f'Extra Place Module status to be {expected_result}')

    @property
    def promotion_name(self):
        self.scroll_to()
        we = self._find_element_by_selector(selector=self._name, context=self._we, timeout=1)
        self.scroll_to_we(we)
        return self._get_webelement_text(we=we, timeout=2)


class HomePageExtraPlaceContent(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="raceCard.event"]'
    _list_item_type = HomePageExtraPlaceItem


class HomePageNextRacesTabContent(TabContent):
    _url_pattern = r'^http[s]?:\/\/.+\/(home\/next-races)?$'
    _accordions_list = 'xpath=.//*[@data-crlat="raceCard"]'
    _accordions_list_type = HomePageNextRacesContent
    _extra_place_module = 'xpath=.//*[@data-crlat="extraPlaceHomeMod"]'
    _extra_place_module_list_type = HomePageExtraPlaceContent

    def has_extra_place_module(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._extra_place_module, timeout=0).is_displayed(),
            expected_result=expected_result,
            timeout=timeout,
            name=f'Extra Place Module status to be {expected_result}')

    @property
    def extra_place_module(self):
        try:
            self._find_element_by_selector(selector=self._extra_place_module,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=1)
        except StaleElementReferenceException:
            self._we = self._find_myself()
        return self._extra_place_module_list_type(selector=self._extra_place_module, context=self._we)


class HomePageNextRacesRunnersContainer(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="raceCard.odds"]'
    _list_item_type = MarketRowsItem
