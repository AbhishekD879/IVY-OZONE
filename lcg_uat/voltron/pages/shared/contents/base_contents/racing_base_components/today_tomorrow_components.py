from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.promotion_icons import PromotionIcons
from voltron.pages.shared.contents.base_contents.racing_base_components.base_components import RacingSimpleEventListItem, \
    Meeting
from voltron.utils.waiters import wait_for_result


class TodayTomorrowByTimeEventListItem(RacingSimpleEventListItem):
    _item_name = 'xpath=.//*[@data-crlat="raceList.raceTime"]'
    _promotion_icons = 'xpath=.//*[@data-crlat="promotionIcons"]'
    _go_to_race_card_link = 'xpath=.//*[@data-crlat="linkRaceCard"]'
    _watch_live_icon = 'xpath=.//*[@class="odds-icon-stream small-icon"]'
    _watch_live = 'xpath=.//*[@class="odds-small"]'

    @property
    def promotion_icons(self):
        return PromotionIcons(selector=self._promotion_icons, context=self._we)

    @property
    def go_to_race_card_link(self):
        return self._find_element_by_selector(selector=self._go_to_race_card_link)

    @property
    def race_name(self):
        return self._find_element_by_selector(selector=self._item_name, context=self._we)

    @property
    def go_to_race_card(self):
        return ButtonBase(selector=self._race_card_link, context=self._we)

    def has_watch_live_icon(self, expected_result=True, timeout=3):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._watch_live_icon, timeout=0),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 name='Watch Live icon to be displayed')
        return result

    @property
    def watch_live_icon(self):
        return ButtonBase(selector=self._watch_live_icon, context=self._we)

    @property
    def watch_live(self):
        return self._find_element_by_selector(selector=self._watch_live, context=self._we)


class TodayTomorrowByTimeGroupListItem(EventGroup):
    _show_more_button = 'xpath=.//*[@data-crlat="raceList.buttonShowAll"]'
    _item = 'xpath=.//*[@data-crlat="raceList.eventEntity"]'
    _list_item_type = TodayTomorrowByTimeEventListItem

    @property
    def show_more_button(self):
        return ButtonBase(selector=self._show_more_button, timeout=1)

    def has_show_more_button(self, expected_result=True, timeout=3):
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._show_more_button, timeout=0),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 name='Show more button to be displayed')
        return result


class TodayTomorrowEventGroupListItem(EventGroup):
    _date_header = 'xpath=.//*[@data-crlat="raceGrid.getFullDate"]'
    _item = 'xpath=.//*[@data-crlat="raceGrid.meeting" or @data-crlat="raceGrid.sectionRace" or @data-crlat="accordion"]'
    _list_item_type = Meeting
    _race_by_time = 'xpath=.//*[@class="race-list"]'

    @property
    def date_header(self):
        return self._get_webelement_text(selector=self._date_header, timeout=0)

    @property
    def race_by_time(self):
        return TodayTomorrowByTimeGroupListItem(selector=self._race_by_time, context=self._we)


class TodayTomorrowByMeeting(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="racing.byMeeting"]//*[@data-crlat="accordion"]'
    _list_item_type = TodayTomorrowEventGroupListItem


class TodayTomorrowByTime(AccordionsList):
    _item = 'xpath=.//*[@data-crlat="accordion"]'
    _list_item_type = TodayTomorrowByTimeGroupListItem
