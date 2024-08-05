from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase, LinkBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.promotion_icons import PromotionIcons
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.racing_base_components.next4_section import MarketRowsItem, \
    Next4ColumnPanel
from voltron.utils.waiters import wait_for_result


class LadbrokesNextRacesEventHeader(Next4ColumnPanel):
    _name = 'xpath=.//*[@data-crlat="raceCard.eventName"]'
    _more_link = 'xpath=.//*[@data-crlat="raceNextLink"]'

    @property
    def name(self):
        self.scroll_to()
        return self._get_webelement_text(selector=self._name, context=self._we)

    @property
    def more_link(self):
        return LinkBase(selector=self._more_link, context=self._we, timeout=1)

    @property
    def race_header_name(self):
        return TextBase(selector=self._name, context=self._we)


class LadbrokesNextRacesEventSubHeader(ComponentBase):
    _e_w_and_places = 'xpath=.//*[@data-crlat="raceCard.eventTerms"]'
    _promotion_icons = 'xpath=.//*[@data-crlat="promotionIcons"]'
    _watch_label = 'xpath=.//*[@data-crlat="watchLabel"]'

    @property
    def e_w_and_places(self):
        """
        Represents section where E/W scores and Places represents. Examples:
            - 'E/W 1/8 Places 1-2-3'
            - 'E/W 1/4 Places 1-2'
        """
        return TextBase(selector=self._e_w_and_places, context=self._we)

    @property
    def promotion_icons(self):
        """
        Represents section where promotion icons are placed, like 'WatchLive' etc.
        """
        return PromotionIcons(selector=self._promotion_icons, context=self._we)

    def has_e_w_and_places(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._e_w_and_places,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Has each way status to be {expected_result}')

    def has_watch_label(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._watch_label,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Has each way status to be {expected_result}')

    @property
    def watch_label(self):
        return self._find_element_by_selector(selector=self._watch_label, timeout=1)


class LadbrokesNextRacesRunnersContainer(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="raceCard.odds"]'
    _list_item_type = MarketRowsItem


class LadbrokesNextRacesEventsContainer(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="raceCard.eventName"]/*[@class="gap-signpost"]'
    _is_virtual = 'xpath=.//*[@data-crlat="raceCard.eventName"]/*[@class="virtual-title"]'
    _sub_header = 'xpath=./following-sibling::*[@data-crlat="raceSubHeader"]'
    _runners = 'xpath=./following-sibling::*[@data-crlat="eventGroup"]'

    @property
    def is_virtual(self):
        return self._find_element_by_selector(selector=self._is_virtual, context=self._we, timeout=1) is not None

    @property
    def header(self):
        return LadbrokesNextRacesEventHeader(web_element=self._we, selector=self._selector)

    @property
    def sub_header(self):
        """
        Represent section where E/W scores and Places are placed together with different promotion icons like 'WatchLive' etc
        """
        return LadbrokesNextRacesEventSubHeader(selector=self._sub_header, context=self._we)

    @property
    def runners(self):
        """
        Represent section which contains list of runners with their new odds, and, if exists, old odds
        """
        return LadbrokesNextRacesRunnersContainer(selector=self._runners, context=self._we)

    @property
    def name(self):
        self.scroll_to()
        return self._get_webelement_text(selector=self._name, context=self._we)


class LadbrokesNextRacesEvents(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="raceHeader"]'
    _list_item_type = LadbrokesNextRacesEventsContainer


class LadbrokesNextRacesTabContent(TabContent):
    _accordions_list_type = LadbrokesNextRacesEvents

    def _wait_active(self, timeout=0):
        """
        Overriding method from TabContent
        """
        pass

    @property
    def accordions_list(self):
        return self._accordions_list_type(web_element=self._we, selector=self._selector)
