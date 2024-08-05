from collections import OrderedDict

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import voltron.environments.constants as vec
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroupHeader
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.base_contents.sport_base import SportPageBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import scroll_to_center_of_element
from voltron.utils.waiters import wait_for_result


class InPlaySportIcon(ButtonBase):
    _use = 'xpath=.//*'

    @property
    def href(self):
        return ComponentBase(selector=self._use, context=self._we, timeout=2).get_attribute('xlink:href')


class InPlayEventGroupHeader(EventGroupHeader):
    _sport_icon = 'xpath=.//*[@data-crlat="icon.header"]'

    @property
    def sport_icon(self):
        return InPlaySportIcon(selector=self._sport_icon, context=self._we)


class InPlayEventGroup(EventGroup):
    _item = 'xpath=.//*[@data-crlat="eventEntity"]'
    _show_all = 'xpath=.//*[@data-crlat="showMoreLeagues"]'
    _header_type = InPlayEventGroupHeader

    @property
    def event_name(self):
        return self.name

    @property
    def show_all(self):
        return LinkBase(selector=self._show_all)

    @property
    def has_show_all(self, timeout=1, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._show_all, context=self._we) is not None,
            name=f'"Show all" is displayed to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout
        )
        return result


class InPlayAccordionList(AccordionsList):
    _list_item_type = InPlayEventGroup
    _name = 'xpath=.//*[contains(@data-crlat, "inplayLabel") or contains(@data-crlat, "inplay.")]'
    _count_label = 'xpath=.//*[@data-crlat="inplayCountLabel"]'

    def _wait_active(self, timeout=20):
        self._we = self._find_myself()
        self._wait_all_items(poll_interval=3, timeout=timeout)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we, timeout=1)

    @property
    def get_first_item(self):
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            list_item.scroll_to()
            items_ordered_dict.update({list_item.name: list_item})
            if len(items_ordered_dict)>0:
                return items_ordered_dict

    @property
    def events_count_label(self):
        return self._get_webelement_text(selector=self._count_label, context=self._we, timeout=3)



class InPlayGroupingButton(ButtonBase):
    _name = 'xpath=.//*[@data-crlat="switcher.name"]'
    _counter = 'xpath=.//*[@data-crlat="switcher.eventCount"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    @property
    def counter(self):
        text = self._get_webelement_text(selector=self._counter, timeout=0.5)
        if text:
            return int(text.strip('()'))
        return 0

    def has_counter(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._counter, timeout=0) is not None,
            name=f'Counter status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class InPlayGroupingSelectionButtons(GroupingSelectionButtons):
    _list_item_type = InPlayGroupingButton


class InPlayTabContent(TabContent):
    _item = 'xpath=.//*[@data-crlat="accordionsList"]'
    _grouping_selection_buttons_type = InPlayGroupingSelectionButtons
    _list_item_type = InPlayAccordionList
    _live_now_counter_number = 'xpath=.//*[@data-crlat="inplay.livenow"]/following-sibling::span'
    _upcoming_counter_number = 'xpath=.//*[@data-crlat="inplay.upcoming"]/following-sibling::span'
    _in_play_header = 'xpath=.//*[@data-crlat="inPlayHeader"]//*[contains(@data-crlat,"inplay.live") or contains(@data-crlat,"inplay.upcoming")]'
    _selected_market_name = 'xpath=.//*[@class="option-title"] | .//*[@data-crlat="selected-item"]'
    _down_arrow = 'xpath=.//*[@class="select-arrow"]'
    _verify_spinner = True

    @property
    def has_down_arrow(self):
        return self._find_element_by_selector(selector=self._down_arrow, timeout=1) is not None

    @property
    def _section_headers(self):
        web_elements = self._find_elements_by_selector(selector=self._in_play_header)
        return [self._get_webelement_text(we=element, timeout=0.3) for element in web_elements]

    @property
    def selected_market(self):
        return self._get_webelement_text(selector=self._selected_market_name)

    @property
    def has_live_now_section(self):
        return vec.inplay.LIVE_NOW_EVENTS_SECTION in self._section_headers

    @property
    def has_upcoming_section(self):
        return vec.inplay.UPCOMING_EVENTS_SECTION in self._section_headers

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            list_item.scroll_to()
            name = list_item.name if list_item.name else vec.inplay.LIVE_NOW_EVENTS_SECTION # for live now section, Live Now header and Counter won't display for mobile. OZONE-12249 (New Change for release-167)
            items_ordered_dict.update({name: list_item})
        return items_ordered_dict

    @property
    def live_now(self):
        items_as_ordered_dict = self.items_as_ordered_dict
        if vec.inplay.LIVE_NOW_EVENTS_SECTION in items_as_ordered_dict:
            return items_as_ordered_dict[vec.inplay.LIVE_NOW_EVENTS_SECTION]
        else:
            raise VoltronException(f'No "{vec.inplay.LIVE_NOW_EVENTS_SECTION}" section in the page')

    @property
    def upcoming(self):
        items_as_ordered_dict = self.items_as_ordered_dict
        if vec.inplay.UPCOMING_EVENTS_SECTION in items_as_ordered_dict:
            return items_as_ordered_dict[vec.inplay.UPCOMING_EVENTS_SECTION]
        else:
            raise VoltronException(f'No "{vec.inplay.UPCOMING_EVENTS_SECTION}" section in the page')

    def has_live_now_counter(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._live_now_counter_number, timeout=0) is not None,
            name=f'Live Now counter status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_upcoming_counter(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._upcoming_counter_number, timeout=0) is not None,
            name=f'Upcoming counter status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def live_now_counter(self):
        text = self._get_webelement_text(selector=self._live_now_counter_number, context=self._we, timeout=1)
        if text:
            return int(text.strip('()'))
        return 0

    @property
    def upcoming_counter(self):
        text = self._get_webelement_text(selector=self._upcoming_counter_number, context=self._we, timeout=1)
        if text:
            return int(text.strip('()'))
        return 0


class InPlaySportCarouselButton(ButtonBase):
    _name = 'xpath=.//*[@data-crlat="menuItem.title"]'
    _counter = 'xpath=.//*[@data-crlat="eventCount"]'
    _icon = 'xpath=.//*[@data-crlat="submenuListIcon"]'
    _tab = 'xpath=.//*[@data-crlat="menu.item"]'
    _is_live = 'xpath=.//*[contains(@class,"is-live")]'

    def _wait_active(self, timeout=0):
        try:
            self._find_element_by_selector(selector=self._name, context=self._context,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=3)
        except StaleElementReferenceException:
            self._logger.debug('*** Overriding StaleElementReferenceException in %s' % self.__class__.__name__)

    @property
    def counter(self) -> int:
        text = wait_for_result(lambda: self._get_webelement_text(selector=self._counter),
                               name='Counter to show up',
                               timeout=1, bypass_exceptions=())
        return int(text) if text else 0

    @property
    def is_live(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: 'is-live' in self.get_attribute('class'),
                               expected_result=expected_result,
                               timeout=timeout,
                               name='"is-live" to be shown in @class')

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=2).strip()

    @property
    def icon(self):
        return self._find_element_by_selector(selector=self._icon, context=self._we)

    def is_underscored(self, expected_result=True):
        tab = ComponentBase(selector=self._tab, context=self._we, timeout=1)
        result = wait_for_result(lambda: tab.css_property_value('border-bottom') == '2px solid rgb(239, 51, 64)',
                                 name=f'{self.__class__.__name__} – Tab is underscored',
                                 expected_result=expected_result,
                                 timeout=2)
        return result


class InPlaySportCarouselMenu(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="carouselMenu.item"]'
    _list_item_type = InPlaySportCarouselButton
    _selected_item = 'xpath=.//*[contains(@class, "active")]'

    def _wait_active(self, timeout=5):
        self._we = self._find_myself(timeout=timeout)
        try:
            self._find_element_by_selector(selector=self._item,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=timeout)
        except StaleElementReferenceException:
            self._we = self._find_myself(timeout=timeout)

    @property
    def current(self):
        try:
            return self._list_item_type(selector=self._selected_item, context=self._we, timeout=2).name
        except (StaleElementReferenceException, VoltronException):
            self._logger.debug(f'*** Overriding Exception in {self.__class__.__name__}')
            self._we = self._find_myself(timeout=2)
            return self._list_item_type(selector=self._selected_item, context=self._we, timeout=2).name

    def click_item(self, item_name: str, timeout: int = 5):
        wait_for_result(lambda: item_name in self.items_as_ordered_dict,
                        name=f'"{item_name}" to appear in {self.items_as_ordered_dict.keys()}',
                        timeout=2)
        try:
            scroll_to_center_of_element(self.items_as_ordered_dict[item_name]._we)
            self.items_as_ordered_dict[item_name].click()
        except (VoltronException, StaleElementReferenceException):
            scroll_to_center_of_element(self.items_as_ordered_dict[item_name]._we)
            self.items_as_ordered_dict[item_name].click()
        except KeyError:
            raise VoltronException(f'"{self.__class__.__name__}" item: "{item_name}" '
                                   f'not found in items list: {self.items_as_ordered_dict.keys()}')


class InPlay(SportPageBase):
    _banner_section = 'xpath=.//*[@data-crlat="bannersSection"]'
    _inplay_sport_menu = 'xpath=.//*[@data-crlat="menuCarousel.inPlay"]'
    _inplay_sport_menu_type = InPlaySportCarouselMenu
    _tab_content_type = InPlayTabContent
    _watch_live = 'tag=inplay-watch-live-page'
    _verify_spinner = True

    @property
    def tab_content(self):
        watch_live = self._find_element_by_selector(selector=self._watch_live, context=self._we, timeout=1)
        if watch_live:
            from voltron.pages.shared.contents.inplay_watchlive import InPlayWatchLiveTabContent
            return InPlayWatchLiveTabContent(selector=self._tab_content, context=self._we)
        else:
            return InPlayTabContent(selector=self._tab_content, context=self._we)

    @property
    def inplay_sport_menu(self):
        return self._inplay_sport_menu_type(selector=self._inplay_sport_menu, context=self._we)

    def has_inplay_sport_menu(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._inplay_sport_menu,
                                                   timeout=0) is not None,
            name=f'Sport Menu Visible Status "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
