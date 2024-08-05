from collections import OrderedDict

from selenium.common.exceptions import ElementNotVisibleException, StaleElementReferenceException, \
    NoSuchElementException

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroupHeader, EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.promotion_icons import PromotionIcons

from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


class NameColumn(ComponentBase):
    _horse_name = 'xpath=.//*[@data-crlat="raceCard.runnerName"]'
    _jockey_trainer_name = 'xpath=.//*[@data-crlat="raceCard.runnerJockey"]'
    _form_guide = 'xpath=.//*[@data-crlat="raceCard.runnerFormGuide"]'

    @property
    def horse_name(self):
        we = self._find_element_by_selector(selector=self._horse_name, timeout=0)
        text = self._get_webelement_text(we=we)
        return text if text else we.get_attribute('innerHTML')


class RunnerInfo(ComponentBase):
    _silks = 'xpath=.//*[@data-crlat="raceCard.silk"] | .//*[@data-crlat="gh-silk"]'
    _name_section = 'xpath=.//*[@data-crlat="raceCard.runner"]'

    @property
    def name_section(self):
        name_column = NameColumn(selector=self._name_section, context=self._we)
        return name_column

    @property
    def has_silks(self):
        return self._find_element_by_selector(selector=self._silks, timeout=.5) is not None

    @property
    def has_silks_info(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._silks, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'Runner info to be "{expected_result}"')


class MarketRowsItem(ComponentBase):
    def __init__(self, *args, **kwargs):
        super(MarketRowsItem, self).__init__(*args, **kwargs)
        if not self.is_safari:
            self.scroll_to_we(web_element=self._we)

    _runner_info = 'xpath=.//*[@data-crlat="raceCard.runnerInfo"]'
    _runner_info_type = RunnerInfo
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _previous_price = 'xpath=.//*[@data-crlat="previousPrices"]'

    @property
    def runner_info(self):
        return self._runner_info_type(selector=self._runner_info, context=self._we)

    def has_runner_info(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._runner_info, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'Runner info to be "{expected_result}"')

    @property
    def name(self):
        horse_name = self.runner_info.name_section.horse_name
        return horse_name

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)

    @property
    def previous_price(self):
        return self._get_webelement_text(self._previous_price, timeout=2)

    def has_previous_price(self, timeout=1, expected_result=True):
        self.scroll_to()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._previous_price,
                                                   timeout=0) is not None,
            name=f'Full race card status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class Next4ColumnPanel(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="raceCard.eventName"]/*[@class="gap-signpost"]'
    _is_virtual = 'xpath=.//*[@data-crlat="raceCard.eventName"]/*[@class="virtual-title"]'
    # our locator is not needed here, as ew terms are not expected on Next Races carousel. More to that - we can't set attribute.
    # to verify ew terms are really not displayed, so we will search for it using visible text
    _ew_container = 'xpath=.//*[contains(text(), "Each Way")] | .//*[contains(text(), "EW") or contains(text(), "E/W")]'
    _item = 'xpath=.//*[@data-crlat="raceCard.odds"]'
    _list_item_type = MarketRowsItem
    _full_race_links = 'xpath=.//*[@data-crlat="raceNextLink"]'
    _full_race_span = 'xpath=.//*[@data-crlat="viewFullRace"]'
    _cash_out_label = 'xpath=.//*[@data-crlat="labelCashout"]'
    _promotion_icons = 'xpath=.//*[@data-crlat="promotionIcons"]'
    _timer = 'xpath=.//*[@data-crlat="raceCountdown"]'
    _race_time = 'xpath=.//*[@class="race-timer"]'
    _more_link = 'xpath=.//*[@data-crlat="raceNextLink"]'

    @property
    def more_link(self):
        return LinkBase(selector=self._more_link, context=self._we, timeout=1)

    @property
    def is_virtual(self):
        return self._find_element_by_selector(selector=self._is_virtual, context=self._we, timeout=1) is not None

    @property
    def timer(self):
        return self._find_element_by_selector(selector=self._timer)

    def has_timer(self, timeout=3, expected_result=True):
        self.scroll_to()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._timer,
                                                   timeout=0) is not None,
            name=f'Full race card status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_view_full_race_card(self, timeout=1, expected_result=True):
        self.scroll_to()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._full_race_links,
                                                   timeout=0) is not None,
            name=f'Full race card status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def full_race_card(self):
        self.scroll_to()
        return LinkBase(selector=self._full_race_links, context=self._we, timeout=1)

    @property
    def cash_out_label(self):
        self.scroll_to()
        return IconBase(selector=self._cash_out_label, context=self._we)

    def has_cashout_label(self, timeout=1, expected_result=True):
        self.scroll_to()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._cash_out_label,
                                                   timeout=0) is not None,
            name=f'cashout label status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def event_id(self):
        self.scroll_to()
        return self.get_attribute('data-eventid')

    def has_each_way_terms(self, timeout=1, expected_result=True):
        self.scroll_to()
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._ew_container,
                                                   timeout=0) is not None,
            name=f'Each way terms status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def each_way_terms(self):
        return self._get_webelement_text(selector=self._ew_container, timeout=1)

    @property
    def name(self):
        self.scroll_to()
        we = self._find_element_by_selector(selector=self._name, context=self._we, timeout=1)
        self.scroll_to_we(we)
        return self._get_webelement_text(we=we, timeout=2)

    @property
    def event_name(self):
        self.scroll_to()
        return self.name

    def click(self):
        self.scroll_to()
        we = self._find_element_by_selector(self._full_race_span, timeout=0)
        self.scroll_to_we(we)
        try:
            we.click()
        except ElementNotVisibleException:
            click(we)

    @property
    def promotion_icons(self):
        self.scroll_to()
        return PromotionIcons(selector=self._promotion_icons, context=self._we)


class Next4GroupHeader(EventGroupHeader):
    _title = 'xpath=.//*[@data-crlat="headerTitle.leftMessage"]'
    _chevron_arrow = 'xpath=.//*[@data-crlat="chevronArrow"]'

    @property
    def title_text(self):
        return self._get_webelement_text(selector=self._title, timeout=1)

    @property
    def chevron_arrow(self):
        return self._find_element_by_selector(selector=self._chevron_arrow, timeout=1)

    def has_chevron_arrow(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._chevron_arrow,
                                                   timeout=0) is not None,
            name=f'Chevron arrow status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class Next4FeaturedGroupHeader(Next4GroupHeader):
    _title = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'


class Next4Section(EventGroup):
    _header = 'xpath=.//*[@data-crlat="containerHeader"]'
    _header_type = Next4GroupHeader
    _item = 'xpath=.//*[@data-crlat="raceData"]//*[@data-crlat="raceCard.event"]'
    _list_item_type = Next4ColumnPanel
    _next_arrow = 'xpath=.//*[@data-crlat="sb.nextRaces"]'
    _prev_arrow = 'xpath=.//*[@data-crlat="sb.previousRaces"]'

    @property
    def _items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_ordered_dict = OrderedDict()
        for num in range(0, len(items_we)):
            try:
                items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
                section = self._list_item_type(web_element=items_we[num])
                items_ordered_dict.update({section.name: section})
            except IndexError as e:
                raise VoltronException(e)
            except (StaleElementReferenceException, VoltronException):
                items_we = self._find_elements_by_selector(selector=self._item, context=self._we)
                section = self._list_item_type(web_element=items_we[num])
                items_ordered_dict.update({section.name: section})
        return items_ordered_dict

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        try:
            return self._items_as_ordered_dict
        except (StaleElementReferenceException, VoltronException) as e:
            self._logger.warning(e)
            return self._items_as_ordered_dict

    def click_next_arrow(self):
        click(self._find_element_by_selector(selector=self._next_arrow, timeout=3))

    def click_prev_arrow(self):
        click(self._find_element_by_selector(selector=self._prev_arrow, timeout=3))

    def _wait_active(self, timeout=2):
        self._we = self._find_myself(timeout=timeout)
        try:
            self._find_element_by_selector(selector=self._item,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=timeout)
        except StaleElementReferenceException:
            self._we = self._find_myself(timeout=timeout)

    @property
    def date_header(self):
        return ''

    @property
    def name(self):
        try:
            return self.group_header.title_text
        except VoltronException:
            self._get_webelement_text(we=self._we)


class Next4SectionLegacy(Next4Section):
    _expanded_criteria = 'xpath=.//*[@data-crlat="accordion"]'
    _show_more = 'xpath=.//*[@data-crlat="showMore"]'

    def is_expanded(self, timeout=0.6, expected_result=True):
        section = self._find_element_by_selector(selector=self._expanded_criteria, timeout=timeout)
        if section:
            result = wait_for_result(lambda: 'is-expanded' in section.get_attribute('class'),
                                     name=f'"{self.__class__.__name__}" Accordion expand status to be "{expected_result}"',
                                     expected_result=expected_result,
                                     timeout=timeout)
            self._logger.debug(f'*** "{self.__class__.__name__}" Accordion expanded status is {result}')
            return result
        return False

    @property
    def name(self):
        return self.group_header.title_text

    @property
    def show_more_link(self):
        return LinkBase(selector=self._show_more, context=self._we)

    def has_show_more_link(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._show_more,
                                                   timeout=0) is not None,
            name=f'Show more link status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class Next4SectionFeatured(Next4Section):
    _header = 'xpath=.//*[@data-crlat="containerHeader"]'
    _header_type = Next4FeaturedGroupHeader
