# -*- coding: utf-8 -*-
from datetime import datetime

from voltron.pages.shared.components.primitives.amount_field import AmountField
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import GroupingSelectionButtons
from voltron.pages.shared.contents.base_contents.sport_base import SportRacingPageBase
from voltron.pages.shared.contents.my_bets.cashout import Bet
from voltron.pages.shared.contents.my_bets.cashout import Cashout
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.components.content_header import HeaderLine
from voltron.pages.shared.components.primitives.text_labels import LinkBase


class DetailsBetLeg(ComponentBase):
    _result = 'xpath=.//*[@data-crlat="labelResult"]'
    _market_type = 'xpath=.//*[@data-uat="marketName"]'
    _outcome_name = 'xpath=.//*[@data-crlat="labelSelectionName"]'
    _odds = 'xpath=.//*[@data-uat="odds"]'
    _event_type = 'xpath=.//*[@data-uat="eventName"]'
    _event_date = 'xpath=.//*[@data-uat="eventStartTime"]'
    _ew_terms = 'xpath=.//*[@data-uat="eachWay"]'
    _selection_name = 'xpath=.//*[@data-crlat="selectionName" or @data-uat="selectionName"]'
    _track_name = 'xpath=.//*[@data-crlat="labelTrackName"]'
    _bet_type = 'xpath=.//*[@data-crlat="betPoolName"]'
    _event_name = 'xpath=.//*[@data-crlat="eventName" or @data-uat="eventName"]'
    _event_name_detail = 'xpath=.//*[@data-crlat="legEventDetail"]'
    _fade_out_overlay = True
    _verify_spinner = True

    @property
    def event_name(self):
        return normalize_name(self._get_webelement_text(selector=self._event_name))

    @property
    def event_name_detail(self):
        return self._get_webelement_text(selector=self._event_name_detail)

    @property
    def selection_name(self):
        return self._get_webelement_text(selector=self._selection_name).replace('(', '').replace(')', '')

    @property
    def track_name(self):
        return self._get_webelement_text(selector=self._track_name)

    @property
    def name(self):
        return '%s - %s' % (self.selection_name, self.event_name)

    @property
    def event_id(self):
        return self.get_attribute('data-eventid')

    @property
    def result(self):
        return self._get_webelement_text(selector=self._result, timeout=2)

    @property
    def outcome_name(self):
        return self._get_webelement_text(selector=self._outcome_name, timeout=2)

    @property
    def odds(self):
        return self._get_webelement_text(selector=self._odds, timeout=2)

    @property
    def market_type(self):
        return self._get_webelement_text(selector=self._market_type, timeout=2)

    @property
    def bet_type(self):
        return self._get_webelement_text(selector=self._bet_type, timeout=2)

    @property
    def ew_terms(self):
        return self._get_webelement_text(self._ew_terms)

    @property
    def event_date(self):
        date = self._find_element_by_selector(selector=self._event_date, timeout=0)
        if date is not None:
            return datetime.strptime(date.text, "%d.%m.%Y, %I:%M %p")
        else:
            raise VoltronException('Event date is not shown')

    @property
    def event_type(self):
        return ButtonBase(selector=self._event_type)


class BetDetails(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="legInBet"]'
    _list_item_type = DetailsBetLeg
    _bet_receipt = 'xpath=.//*[@data-uat="betId"]'

    @property
    def bet_receipt(self):
        return self._get_webelement_text(selector=self._bet_receipt, timeout=5)


class Selection(ComponentBase):
    _my_stable_signposting = 'xpath=.//*[@data-crlat="myStableSignpostingSvg"]'

    @property
    def my_stable_sign_posting(self):
        return self._find_element_by_selector(selector=self._my_stable_signposting, context=self._we, timeout=0)


class MyBetsSection(Bet):
    _name = 'xpath=.//*[@data-crlat="topBar"]'
    _bet_details = 'xpath=.//*[@data-crlat="betDetail.content"]'
    _section_date = 'xpath=.//*[@data-crlat="panel.betDetails"]'
    _bet_type = 'xpath=.//*[@data-crlat="betType"]'
    _total_stake = 'xpath=.//*[@data-crlat="value.totalStake"]'
    _unit_stake = 'xpath=.//*[@data-crlat="value.unitStake"]'
    _bet_time = 'xpath=.//*[@data-crlat="betDetailDate"]'
    _bet_status = 'xpath=.//*[@data-crlat="betStatus"]'
    _total_est_returns = 'xpath=.//*[@data-crlat="value.totalEstReturns" or @data-crlat="value.totalReturns"]'
    _item = 'xpath=.//*[@data-crlat="betDetails.container" or @data-crlat="cashout.betLegItem"]'
    _list_item_type = DetailsBetLeg
    _selection_name = 'xpath=.//*[@data-crlat="selectionName"]'
    _selection_price = 'xpath=.//*[@data-crlat="selectionPrice"]'

    @property
    def selection(self):
        return Selection(selector=self._selection_name, context=self._we)

    @property
    def selection_name(self):
        return self._get_webelement_text(selector=self._selection_name).replace('(', '').replace(')', '')

    @property
    def selection_price(self):
        return self._get_webelement_text(selector=self._selection_price)

    @property
    def section_header(self):
        return ComponentBase(selector=self._name, context=self._we)

    @property
    def name(self):
        return TextBase(selector=self._name, context=self._we, timeout=3).name

    @property
    def bet_details(self):
        return BetDetails(selector=self._bet_details, context=self._we, timeout=3)

    @property
    def bet_type(self):
        return self._get_webelement_text(selector=self._bet_type, timeout=3)

    @property
    def unit_stake(self):
        return AmountField(selector=self._unit_stake, context=self._we)

    @property
    def total_stake(self):
        return AmountField(selector=self._total_stake, context=self._we)

    @property
    def header(self):
        return self._find_element_by_selector(selector=self._name)

    @property
    def section_date(self):
        date = self._find_element_by_selector(selector=self._section_date, timeout=0)
        if date:
            return date.text
        else:
            raise VoltronException('Section date is not shown')

    @property
    def bet_time(self):
        item_time = self._find_element_by_selector(selector=self._bet_time, timeout=0)
        if item_time:
            return datetime.strptime(item_time.text, '%I:%M')
        else:
            raise VoltronException('Bet time is not shown')

    @property
    def bet_date_and_time(self):
        item_date_and_time = self._find_element_by_selector(selector=self._bet_time, timeout=0)
        if item_date_and_time:
            return datetime.strptime(item_date_and_time.text, '%d.%m %I:%M %p')
        else:
            raise VoltronException('Bet time is not shown')

    @property
    def bet_status(self):
        return self._get_webelement_text(self._bet_status, timeout=2)

    @property
    def total_est_returns(self):
        total_est_returns = self._get_webelement_text(self._total_est_returns, timeout=2)
        return self.strip_currency_sign(total_est_returns)


class MyBetsSectionsList(Cashout):
    _url_pattern = r'^http[s]?:\/\/.+\/?'
    _item = 'xpath=.//*[@data-crlat="section.betHistory"]'
    _list_item_type = MyBetsSection

    def wait_for_sections(self, timeout=5):
        if not wait_for_result(lambda: len(self.items_as_ordered_dict) > 20,
                               name=f'20 sections to be present, currently it is: "{len(self.items_as_ordered_dict)}"',
                               timeout=timeout):
            self._logger.warning(f'*** Error waiting for sections, current number of sections is "{len(self.items_as_ordered_dict)}"')


class MyBetsHeaderLine(HeaderLine):
    _deposit_link = 'xpath=.//*[@data-crlat="linkDeposit"]'

    @property
    def my_bets_deposit(self):
        return LinkBase(selector=self._deposit_link, timeout=1)


class MyBetsBase(SportRacingPageBase):
    _my_bets_sections_list = 'xpath=.//*[@data-crlat="betHistoryContainer"]'
    _my_bets_sections_list_type = MyBetsSectionsList
    _login_button = 'xpath=.//*[@data-crlat="signInButton"]'
    _grouping_selection_buttons = 'xpath=.//*[@data-crlat="switchers"]'
    _grouping_selection_buttons_type = GroupingSelectionButtons
    _bet_type = 'xpath=.//*[@data-crlat="betType"]'
    _header_line_type = MyBetsHeaderLine

    @property
    def has_grouping_buttons(self):
        return self._find_element_by_selector(self._grouping_selection_buttons, timeout=5) is not None

    @property
    def grouping_buttons(self):
        if self.has_grouping_buttons:
            return self._grouping_selection_buttons_type(self._grouping_selection_buttons, context=self._we)
        else:
            raise VoltronException('No Grouping Buttons object found')

    @property
    def my_bets_sections_list(self):
        return self._my_bets_sections_list_type(selector=self._my_bets_sections_list, context=self._we)

    def has_my_bets_sections_list(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._my_bets_sections_list,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'My bets section list status to be {expected_result}')

    @property
    def login_button(self):
        return ButtonBase(selector=self._login_button, context=self._we, timeout=3)

    def has_login_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._login_button,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Login button status to be "{expected_result}"')

    @property
    def bet_types(self):
        bet_headers = self._find_elements_by_selector(selector=self._bet_type, timeout=3)
        bet_headers_text = []
        for headers in bet_headers:
            bet_headers_text.append(headers.text)
        return bet_headers_text
