from collections import OrderedDict
from time import sleep

from selenium.common.exceptions import WebDriverException, StaleElementReferenceException

from voltron.pages.shared import get_driver
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.accordions_container import AccordionHeader
from voltron.pages.shared.components.fixture_header import FixtureHeader
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.contents.base_contents.common_base_components.sport_list_item import SportEventListItem
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class EventGroupHeader(AccordionHeader):
    _badge_label = 'xpath=.//*[@data-crlat="badge.label"]'
    _byb_icon = 'xpath=.//*[@data-crlat="yourcallIcon"]'
    _league_icons_elements = 'xpath=.//*[@data-crlat="yourcallIcon"] | .//*[@data-crlat="labelCashout"]'
    _see_all_link = 'xpath=.//a[contains(@class, "see-all")]'

    @property
    def _league_icons(self):
        return self._find_elements_by_selector(selector=self._league_icons_elements, context=self._we)

    @property
    def icons_count(self):
        return len(self._league_icons)

    def has_byb_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._byb_icon,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def cash_out_mark(self):
        if self.icons_count > 1:
            return self._league_icons[1].get_attribute('data-crlat') == u'labelCashout'

    @property
    def badge_label(self):
        return self._get_webelement_text(selector=self._badge_label)

    @property
    def see_all_link(self):
        return self._find_element_by_selector(selector=self._see_all_link, context=self._we)

    def has_see_all_link(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._see_all_link,
                                                                      context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Button shown status to be {expected_result}')


class EventGroupSportHeader(EventGroupHeader):
    pass


class EventGroup(Accordion):
    _header = 'xpath=.//header'
    _competitions_market_headers = 'xpath=.//*[@class="co-name-title"]'
    _header_type = EventGroupHeader
    _sport_header = 'xpath=.//*[@data-crlat="containerHeader"]'
    _fixture_header = 'xpath=.//*[@data-crlat="eventOddsHeader"]'
    _fixture_header_type = FixtureHeader
    _item = 'xpath=.//*[@data-crlat="eventEntity"][.//*[contains(@data-crlat, "oddsCard") and contains(@data-crlat, "Template")]]'  # child is important here as it allows to select .//*[@event="eventEntity"] that are not empty!
    _list_item_type = SportEventListItem
    _outright_odds_card = 'xpath=.//*[@class="co-odds-card-container"]/div'
    _outright_ew_terms = 'xpath=.//*[@class ="co-left-header"]'
    _outright_date_time = 'xpath=.//*[@class="co-right-header"]'
    _fade_out_overlay = True
    _verify_spinner = True
    _league_table = 'xpath=.//*[@class="stats-link"]'
    _team_name = 'xpath=.//*[@class="team-name"]'

    def get_bet_button_by_selection_id(self, selection_id, timeout=3):
        button = self._find_element_by_selector(
            selector=f'xpath=.//*[contains(@class, "{selection_id}") or contains(@id, "{selection_id}")]',
            context=self._we, timeout=timeout)
        return BetButton(web_element=button) if button else None

    def has_fixture_header(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._fixture_header, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'Fixture header presence status in {self.__class__.__name__} to be {expected_result}')

    @property
    def fixture_header(self):
        return self._fixture_header_type(selector=self._fixture_header, context=self._we)

    @property
    def team_name(self):
        return self._find_element_by_selector(self._team_name, context=self._we)

    @property
    def team_names(self):
        return self._find_elements_by_selector(self._team_name, context=self._we)

    @property
    def league_table_link(self):
        return self._find_element_by_selector(selector=self._league_table,timeout=2)

    @property
    def has_league_table_link(self):
        return self._find_element_by_selector(selector=self._league_table, timeout=2) is not None

    @property
    def name(self):
        try:
            self.scroll_to()
            return self.group_header.title_text
        except (VoltronException,StaleElementReferenceException):
            try:
                wait_for_result(lambda: self._get_webelement_text(we=self._we), name="waiting for web element text",
                                timeout=2,bypass_exceptions=VoltronException)
            except (VoltronException,StaleElementReferenceException):
                wait_for_result(lambda: self._get_webelement_text(we=self._we), name="waiting for web element text",
                                timeout=2,bypass_exceptions=VoltronException)


    @property
    def sport_name(self):  # for in play events
        name = self.group_sport_header.title_text
        if name is not None:
            return name

    @property
    def cash_out(self):
        return self.group_header.cash_out_mark

    def has_byb_icon(self, expected_result=True):
        return self.group_header.has_byb_icon(expected_result=expected_result)

    @property
    def group_header(self):
        header = self._header_type(self._header, context=self._we, timeout=2)
        header.scroll_to()
        return header

    @property
    def competitions_market_headers_text(self):
        headers_text = []
        headers = self._find_elements_by_selector(
            selector=self._competitions_market_headers)
        for header in headers:
            headers_text.append(header.text)
        return headers_text


    @property
    def group_sport_header(self):  # for in play events
        we = self._find_element_by_selector(selector=self._sport_header, context=get_driver(), timeout=0)
        if we is not None:
            return EventGroupSportHeader(web_element=we)

    def get_league(self, league_name):  # if multiple leagues available
        web_elements = self._find_elements_by_selector(selector=self._sport_header, context=get_driver(), timeout=0)
        for we in web_elements:
            if league_name in we.text:
                return EventGroupSportHeader(web_element=we)

    def expand(self):
        self._spinner_wait()
        name = self.group_header.title_text
        if self.is_expanded():
            self._logger.warning('*** Bypassing accordion expand, since "%s" already expanded' % name)
        else:
            self._logger.info('*** Expanding "%s"' % name)
            try:
                self.scroll_to_we(web_element=self._we)
                self.group_header.click()
                wait_for_result(lambda: self.is_expanded(timeout=0), name='Expanded status for %s' % name, timeout=5)
            except WebDriverException as err:
                self._logger.warning('*** Overriding "%s" issue by retry in 2 seconds...' % err)
                self.scroll_to_we(web_element=self._we)
                self.group_header.click()
                wait_for_result(lambda: self.is_expanded(timeout=0), name='Expanded status for %s' % name, timeout=5)

    def collapse(self):
        self._spinner_wait()
        name = self.group_header.title_text
        if not self.is_expanded():
            self._logger.debug('*** Bypassing accordion collapse, since "%s" already collapsed' % name)
        else:
            self._logger.debug('*** Collapsing "%s"' % name)
            self.group_header.click()
            wait_for_result(lambda: self.is_expanded(expected_result=False, timeout=0),
                            expected_result=False, name='Expanded status for %s' % name, timeout=5)

    def get_items_count(self):
        return len(self._find_elements_by_selector(self._item, timeout=0))

    def _wait_all_items(self, poll_interval=1, timeout=20) -> list:
        prev_all_events = []
        iteration_limit = 20
        for iteration in range(0, int(timeout / poll_interval)):
            self._spinner_wait()
            all_events = self._find_elements_by_selector(self._item, timeout=0)
            self._logger.debug(
                '*** Wait for all events to be rendered. Was %s now %s. Iteration %s/%s' %
                (
                    len(prev_all_events),
                    len(all_events),
                    iteration,
                    iteration_limit
                )
            )

            if len(all_events) == len(prev_all_events) and len(all_events) > 0:
                return all_events
            if iteration >= iteration_limit:
                self._logger.warning('Iteration limit met {0} on get all events'.format(iteration_limit))
                return all_events
            self.scroll_to_we(web_element=all_events[-1]) if all_events else self.scroll_to_we()
            prev_all_events = all_events
            sleep(poll_interval)
            iteration += 1
        return []

    @property
    def items(self) -> list:
        items_we = self._wait_all_items()
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_array = []
        for item_we in items_we:
            item_component = self._list_item_type(web_element=item_we)
            items_array.append(item_component)
        return items_array

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._wait_all_items()
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.event_name.replace("\nSEE ALL", "").strip(): list_item})
        return items_ordered_dict

    @property
    def outright_selections(self) -> OrderedDict:
        web_elements = self._find_elements_by_selector(selector=self._outright_odds_card, context=get_driver(), timeout=0)
        return web_elements

    @property
    def outright_ew_terms(self):
        return self._find_element_by_selector(selector=self._outright_ew_terms, context=self._we)

    @property
    def outright_date_time(self):
        return self._find_element_by_selector(selector=self._outright_date_time, context=self._we)


class EventGroupBigComptition(EventGroup):
    _item = 'xpath=.//odds-card-component'
