from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.racing_base_components.racing_accordions_list import RacingDateTab
from voltron.utils.waiters import wait_for_result


class RaceMeetingItem(ComponentBase):
    @property
    def name(self):
        return self._we.text


class MeetingSelector(SelectBase):
    _item = 'xpath=.//option'
    _list_item_type = RaceMeetingItem
    _selected_item = 'xpath=.//option[@selected="selected"]'

    @property
    def selected_item(self):
        select = TextBase(selector=self._selected_item, context=self._we)
        return select.name


class MeetingeventsList(Accordion):
    _name = 'xpath=.//*[@data-crlat="raceGrid.raceTime"]'
    _resulted = 'xpath=.//*[@data-crlat="resulted"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we, timeout=1)

    def is_resulted(self, timeout=0.5, expected_result=True):
        return wait_for_result(lambda: 'resulted' in self.get_attribute('class'),
                               expected_result=expected_result,
                               timeout=timeout,
                               name='"resulted" to be shown in @class')


class MeetingListItem(Accordion):
    _name = 'xpath=.//*[@data-crlat="itemName"] | .//*[@data-crlat="raceGrid.meeting.name"]'
    _item = 'xpath=.//*[@data-crlat="raceGrid.event"]'
    _list_item_type = MeetingeventsList

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we, timeout=1)


class MeetingListSection(Accordion):
    _section_header = 'xpath=.//*[@data-crlat="sectionHeader"] | .//*[@data-crlat="headerTitle.leftMessage"] | .//*[@class="left-title-text"]'
    _item = 'xpath=.//*[@data-crlat="item"] | .//*[@data-crlat="raceGrid.meeting"]'
    _list_item_type = MeetingListItem

    @property
    def name(self):
        text = self._find_element_by_selector(selector=self._section_header, context=self._we, timeout=1).get_attribute('innerHTML').replace('&amp;', '&')
        return text.upper()


class MeetingsList(Accordion):
    _close_button = 'xpath=.//*[@data-crlat="closeMenuButton"]'
    _title = 'xpath=.//*[@data-crlat="meetingsHeader"]'
    _item = 'xpath=.//*[@data-crlat="meetingSection"][*] | .//racing-events/accordion | .//racing-featured//accordion | .//racing-events//accordion'
    _offers_and_featured = 'xpath=.//offers-and-featured-races'
    _next_races = 'xpath=.//race-card-content'
    _list_item_type = MeetingListSection
    _date_tab = 'xpath=.//*[@data-crlat="switchers"]'
    _date_tab_type = RacingDateTab

    @property
    def date_tab(self):
        return self._date_tab_type(selector=self._date_tab, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    def _wait_active(self, timeout=2):
        try:
            self._find_element_by_selector(selector=self._item, context=self._context,
                                           bypass_exceptions=(NoSuchElementException, ), timeout=timeout)
        except StaleElementReferenceException:
            self._we = self._find_myself(timeout=timeout)

    @property
    def next_races_name(self):
        text = self._find_element_by_selector(selector=self._next_races, context=self._we, timeout=1).text.split('\n')[0]
        return text.upper()

    @property
    def offers_and_featured_name(self):
        text = self._find_element_by_selector(selector=self._offers_and_featured, context=self._we, timeout=1).text.split('\n')[0]
        return text.upper()
