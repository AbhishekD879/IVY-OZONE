from multidict import MultiDict

from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.components.primitives.checkboxes import BuildYourRacecardCheckBox
from voltron.pages.shared.contents.base_contents.common_base_components.promotion_icons import PromotionIcons
from voltron.utils.waiters import wait_for_result


class Event(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="raceGrid.raceTime"]'
    _icon = 'xpath=.//*[@data-crlat="raceGrid.iconRace"]'
    _tab = 'xpath=.//*[@data-crlat="tab"]'
    _promotion_icons = 'xpath=.//*[@data-crlat="promotionIcons"]'
    _check_box = 'xpath=.//*[@data-crlat="checkBox"]'
    _race_off = 'xpath=.//*[@data-crlat="race-off"]'
    _is_live = 'xpath=.//*[@data-crlat="live"]'
    _resulted = 'xpath=.//*[@data-crlat="resulted"]'

    def click(self):
        we = self._find_element_by_selector(selector=self._tab, context=self._we)
        self.scroll_to_we(web_element=we)
        drv = get_driver()
        drv.execute_script("return arguments[0].click();", we)

    @property
    def event_id(self):
        return self.get_attribute('data-eventid')

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    @property
    def event_off_time(self):
        return ButtonBase(selector=self._name, context=self._we, timeout=10)

    @property
    def icon(self):
        return IconBase(selector=self._icon, timeout=0.5, context=self._we)

    def has_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._icon, timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def is_live(self):
        return IconBase(selector=self._is_live, timeout=0.5, context=self._we)

    def has_is_live(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._is_live, timeout=0) is not None,
            name=f'Is live status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_resulted(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._resulted, timeout=2) is not None,
            name=f'Is resulted status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_race_off(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._race_off, timeout=2) is not None,
            name=f'Race Off status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def is_resulted(self):
        return ('race-resulted' in self._we.get_attribute('class').strip(' ').split(' ') or
                'resulted' in self._we.get_attribute('class').strip(' ').split(' ')) and self.has_icon() and self.icon.is_displayed()

    @property
    def is_priced(self):
        return wait_for_result(lambda: 'text-bold' in self._find_element_by_selector(selector=self._name, timeout=2).get_attribute('class'),
                               name='Event is priced',
                               timeout=1)

    @property
    def promotion_icons(self):
        return PromotionIcons(selector=self._promotion_icons, context=self._we)

    @property
    def check_box(self):
        return BuildYourRacecardCheckBox(selector=self._check_box, context=self._we)

    def has_checkbox(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._check_box, timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Checkbox presence status to be "{expected_result}"')


class PoolIndicatorsContainer(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="indicator.poolType"]'
    _list_item_type = ButtonBase


class Meeting(ComponentBase):
    _meeting_name = 'xpath=.//*[@data-crlat="raceGrid.meeting.name"]'
    _stream_icon = 'xpath=.//*[@data-crlat="raceGrid.iconStream"]'
    _item = 'xpath=.//*[@data-crlat="raceGrid.event"]'
    _list_item_type = Event
    _cash_out_label = 'xpath=.//*[@data-crlat="labelCashout"]'
    _bog_icon = 'xpath=.//*[@data-crlat="bogIcon"]'
    _tote_indicator_container = 'xpath=.//*[@data-crlat="poolIndicatorsContainer"]'
    _right_arrow = 'xpath=..//*[@class="action-arrows"]/*[contains(@class, "action-arrow right")]'
    _left_arrow = 'xpath=..//*[@class="action-arrows"]/*[contains(@class, "action-arrow left")]'

    @property
    def cash_out_label(self):
        return IconBase(selector=self._cash_out_label, context=self._we)

    def has_cash_out_label(self, timeout=1):
        return self._find_element_by_selector(selector=self._cash_out_label, timeout=timeout) is not None

    @property
    def bog_icon(self):
        return IconBase(selector=self._bog_icon, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._meeting_name)

    @property
    def has_live_stream(self):
        return self._find_element_by_selector(selector=self._stream_icon, timeout=0) is not None

    def has_pool_indicators(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._tote_indicator_container,
                                                   timeout=0) is not None,
            name=f'Tote pool indicators availability to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def pool_indicator_container(self):
        return PoolIndicatorsContainer(selector=self._tote_indicator_container, context=self._we, timeout=0)

    @property
    def event_name(self):
        return self.name

    @property
    def items_as_ordered_dict(self) -> MultiDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = MultiDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.add(list_item.name, list_item)
        return items_ordered_dict

    @property
    def right_arrow(self):
        return ButtonBase(selector=self._right_arrow, context=self._we)

    @property
    def left_arrow(self):
        return ButtonBase(selector=self._left_arrow, context=self._we)

    def has_right_arrow(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._right_arrow, timeout=0) is not None,
            name=f'next button shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)
    def has_left_arrow(self, expected_result=True, timeout=2):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._left_arrow, timeout=0) is not None,
            name=f'prev button shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)


class RacingSimpleEventListItem(ComponentBase):
    _item_name = 'xpath=.//*[@data-crlat="outerAccordion"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._item_name, context=self._we, timeout=0)

    @property
    def event_name(self):
        return self.name
