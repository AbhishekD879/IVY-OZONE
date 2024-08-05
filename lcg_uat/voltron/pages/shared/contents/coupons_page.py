from collections import OrderedDict

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import tests
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.fixture_header import FixtureHeader
from voltron.pages.shared.components.market_selector_drop_down_desktop import MarketSelectorDesktopDropDown, \
    MarketSelectorOptionDesktop
from voltron.pages.shared.components.markets.popular_goalscorer_market import PopularGoalscorerTable
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.base_contents.common_base_components.accordions_list import AccordionsList
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.contents.sports_tab_contents.sport_coupons_tab import CouponItem
from voltron.pages.shared.contents.sports_tab_contents.sport_coupons_tab import CouponItemDesktop
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.market_selector_drop_down import MarketSelectorOption


class CouponsFixtureHeader(FixtureHeader):
    _date_line = 'xpath=.//*[@data-crlat="dateTitle"]'

    @property
    def date_line(self) -> str:
        return self._get_webelement_text(selector=self._date_line, timeout=2)

    def has_date_line(self, timeout=1, expected_result=True) -> bool:
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._date_line,
                                                   timeout=0) is not None,
            name=f'Date line status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class GoalscorerSelection(ComponentBase):
    _player = 'xpath=.//*[@data-crlat="playerName"]'
    _team = 'xpath=.//*[@data-crlat="teamName"]'
    _bet_button = 'xpath=.//*[contains(@data-crlat, "betButton")]'

    @property
    def name(self):
        return self.player_name

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)

    @property
    def player_name(self):
        return self._get_webelement_text(selector=self._player, context=self._we, timeout=2)

    @property
    def team_name(self):
        return self._get_webelement_text(selector=self._team, context=self._we, timeout=2)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        headers = ['1st', 'Last', 'Anytime']
        items_we = self._find_elements_by_selector(selector=self._bet_button, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')

        items_ordered_dict = OrderedDict(
            [
                (header, self._list_item_type(web_element=item_we)) for header, item_we in zip(headers, items_we)
            ]
        )
        return items_ordered_dict


class GoalscorerTable(PopularGoalscorerTable):
    _list_item_type = GoalscorerSelection


class CouponsEventByDateGrouping(EventGroup):
    _fixture_header_type = CouponsFixtureHeader
    _table = 'xpath=.//*[@data-crlat="containerInnerContent"]'
    _table_type = GoalscorerTable

    @property
    def table(self):
        return self._table_type(selector=self._table, context=self._we)

    @property
    def name(self):
        return self.fixture_header.date_line


class CouponsEventGroup(EventGroup):
    _item = 'xpath=.//*[@data-crlat="eventsGroupedByDate"]'
    _list_item_type = CouponsEventByDateGrouping
    _fixture_header = None
    _fixture_header_type = None

    @property
    def fixture_header(self):
        raise VoltronException('There\'s no fixture header on section level on Coupons event details page')

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._wait_all_items()
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict


class Event(CouponsEventByDateGrouping):
    _name = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _see_all_link = 'xpath=.//*[@data-crlat="goToEvent"]'
    _go_to_event_icon = 'xpath=.//*[@data-crlat="goToEventIcon"]'
    _show_more_button = 'xpath=.//*[@data-crlat="showAllButton"]'

    @property
    def see_all_link(self):
        return ButtonBase(selector=self._see_all_link, context=self._we)

    def has_see_all_link(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._see_all_link,
                                                   timeout=0) is not None,
            name=f'Link status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we, timeout=2)

    @property
    def event_name(self):
        return self.name

    def has_go_to_event_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._go_to_event_icon,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def show_more_button(self):
        return ButtonBase(selector=self._show_more_button, context=self._we)

    def has_show_more_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._show_more_button,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class GoalScorerCouponLeague(AccordionsList, EventGroup):
    _list_item_type = Event
    _item = 'xpath=.//*[@data-crlat="event"]'
    _name = 'xpath=.//*[contains(@class, "league-name") or @data-crlat="headerTitle.centerMessage"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we, timeout=3)


class CouponPageAccordionList(AccordionsList):
    _coupon_type_recognition = 'xpath=.//*[contains(@data-crlat, "couponType")]'
    _default_coupon_accordions_list = 'xpath=.//*[@data-crlat="accordion"]'
    _default_coupon_accordions_list_type = CouponsEventGroup
    _goalscorer_coupon_accordions_list = 'xpath=.//*[@data-crlat="league"]'
    _goalscorer_coupon_accordions_list_type = GoalScorerCouponLeague

    def _wait_active(self, timeout=15):
        super()._wait_active(timeout=timeout)
        wait_for_result(lambda: self._find_elements_by_selector(selector=self._item, context=self._we, timeout=0),
                        name='Coupons to be loaded',
                        timeout=timeout)

    def _get_coupon_type(self):
        coupon_type = self._find_element_by_selector(selector=self._coupon_type_recognition, timeout=0)
        if not coupon_type:
            self._logger.warning('*** Cannot detect coupon type, returning default')
            return 'couponType.default'
        else:
            return coupon_type.get_attribute('data-crlat')

    @property
    def _item(self):
        coupon_types = {'couponType.default': self._default_coupon_accordions_list,
                        'couponType.goalscorer': self._goalscorer_coupon_accordions_list}
        coupon_type = self._get_coupon_type()
        return coupon_types.get(coupon_type, self._default_coupon_accordions_list)

    @property
    def _list_item_type(self):
        coupon_type = self._get_coupon_type()
        coupon_types = {'couponType.default': self._default_coupon_accordions_list_type,
                        'couponType.goalscorer': self._goalscorer_coupon_accordions_list_type}

        accordions_list_type = coupon_types.get(coupon_type, self._default_coupon_accordions_list_type)
        self._logger.info(f'*** Recognised "{self.__class__.__name__}" - "{accordions_list_type.__name__}" type')
        return accordions_list_type
class CouponsMarketSelector(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="dropdown.menuItem"]'
    _list_item_type = MarketSelectorOption
    _fade_out_overlay = True
    _verify_spinner = True

class CouponsList(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="couponItem" or  @data-crlat="dropdown.menuItem"]'
    _list_item_type = CouponItem
    _fade_out_overlay = True
    _verify_spinner = True

    def _wait_active(self, timeout=2):
        self._we = self._find_myself(timeout=timeout)
        try:
            wait_for_result(lambda: len(self.items_as_ordered_dict) > 0,
                            name=f'{self.__class__.__name__} - {self._list_item_type.__name__} to load',
                            timeout=timeout,
                            bypass_exceptions=(NoSuchElementException,))
        except StaleElementReferenceException:
            self._we = self._find_myself(timeout=timeout)


class CouponsListDesktop(CouponsList):
    _list_item_type = CouponItemDesktop


class CouponPageTabContent(TabContent):
    _accordions_list_type = CouponPageAccordionList


class CouponPageMarketSelectorOptionDesktop(MarketSelectorOptionDesktop):

    @property
    def name(self):
        return self.get_attribute('innerHTML').replace('&amp;', '&')


class CouponPageMarketSelectorDesktopDropDown(MarketSelectorDesktopDropDown):
    _item = 'xpath=.//*[@data-crlat="dropdown.menuItem"]'
    _list_item_type = CouponPageMarketSelectorOptionDesktop
    _dropdown_market_selector = 'xpath=.//*[@data-crlat="dropdown"]'


class CouponPageTabContentDesktop(CouponPageTabContent):
    _dropdown_market_selector_type = CouponPageMarketSelectorDesktopDropDown


class CouponPage(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/coupons\/football(?:\/[\w-]+\/[\d]+)?'
    _tab_content_type = CouponPageTabContent
    _coupon_name = 'xpath=.//*[@data-crlat="couponTitle" or @class="of-coupon"]'
    _coupon_selector = 'xpath=.//*[@data-crlat="changeCoupon" or text()="COUPON"]'
    _coupons_list = 'xpath=.//*[@data-crlat="couponsListContainer" or @data-crlat="dropdown-menu"]'
    _coupons_market_selector_list = 'xpath=.//*[text()="MARKET" ]/../..//*[@data-crlat="dropdownMenu" or @data-crlat="dropdown-menu"]'
    _bet_filter_link = 'xpath=.//*[@data-crlat="betFilterLink"]'
    _market_selector = 'xpath=.//*[@data-crlat="couponType.default"]'
    _fade_out_overlay = True
    _verify_spinner = True

    # todo: VOL-1619 Components: Implement Event Header (EDP) component
    @property
    def bet_filter_link(self):
        return ComponentBase(selector=self._bet_filter_link, context=self._we, timeout=3)

    def has_bet_filter_link(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._bet_filter_link,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'BetFilter to be {expected_result}')

    @property
    def name(self):
        return self._get_webelement_text(selector=self._coupon_name, timeout=5)

    @property
    def coupon_selector_link(self):
        return ButtonBase(selector=self._coupon_selector)

    @property
    def has_coupon_selector(self):
        return self._find_element_by_selector(selector=self._coupon_selector, timeout=0) is not None

    @property
    def coupons_market_selector_list(self):
        return CouponsMarketSelector(selector=self._coupons_market_selector_list)

    @property
    def coupons_list(self):
        return CouponsList(selector=self._coupons_list)

    @property
    def is_market_selector_sticky(self):
        we = self._find_element_by_selector(selector=self._market_selector, timeout=0)
        if we.get_attribute('class') and we.get_attribute('style'):
            sticky = 'sticky-on' in we.get_attribute('class')
            return sticky
        return False

    @property
    def market_selector_module(self):
        _market_selector_module = 'xpath=.//*[text()="MARKET" ]' if tests.settings.device_type == 'mobile' else 'xpath=.//*[@data-crlat="dropdown"]'
        return self._find_element_by_selector(selector=_market_selector_module, timeout=0)

    @property
    def has_market_selector_module(self):
        _market_selector_module = 'xpath=.//*[text()="MARKET" ]' if tests.settings.device_type == 'mobile' else 'xpath=.//*[@data-crlat="dropdown"]'
        return self._find_element_by_selector(selector=_market_selector_module, timeout=0) is not None


class CouponPageDesktop(CouponPage, CouponPageTabContent):
    _market_selector_module = 'xpath=.//*[@data-crlat="dropdown"]'
    _dropdown_market_selector_type = SelectBase
    _tab_content_type = CouponPageTabContentDesktop

    @property
    def coupons_list(self):
        return CouponsListDesktop(selector=self._coupons_list)

    @property
    def name(self):
        coupon_name = self._find_element_by_selector(selector=self._coupon_name, timeout=2)
        # .text returns "Tomorrow'S Matches" for "Tomorrow's Matches" UI text
        text = coupon_name.get_attribute('innerText').strip('\n').strip() if coupon_name else ''
        return text
