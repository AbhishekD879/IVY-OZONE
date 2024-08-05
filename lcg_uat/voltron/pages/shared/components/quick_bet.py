import logging

from selenium.common.exceptions import StaleElementReferenceException
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.amount_form import AmountForm
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.info_panel import InfoPanel
from voltron.pages.shared.components.keyboard.mobile_keyboard import Keyboard
from voltron.pages.shared.components.primitives.buttons import ButtonBase, QuickBetButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.components.quick_bet_quick_deposit_panel import GVCQuickDeposit
from voltron.pages.shared.components.quick_deposit_button import QuickDepositButton
from voltron.pages.shared.components.quick_stake_panel import QuickStakePanel
from voltron.pages.shared.components.splash import Splash
from voltron.pages.shared.contents.bet_receipt.bet_receipt import ReceiptSingles
from voltron.pages.shared.contents.trending_bets.trending_bets import TrendingBets
from voltron.pages.shared.contents.betslip.betslip import BetNowSection
from voltron.pages.shared.contents.betslip.betslip_each_way import EachWay
from voltron.pages.shared.contents.betslip.betslip_stake import BetslipStake
from voltron.utils.waiters import wait_for_result


class QuickBetEachWay(EachWay):

    def click(self):
        checkbox = self._find_element_by_selector(selector=self._input, context=self._we)
        driver = get_driver()
        driver.execute_script("arguments[0].click();", checkbox)


class QuickBetContent(BetslipStake):
    _each_way_type = QuickBetEachWay
    _free_bet_icon = 'xpath=.//*[@data-crlat="fbIcon"]'
    _odds = 'xpath=.//*[@data-crlat="odds"]'
    _boosted_odds = 'xpath=.//*[@data-crlat="boostedPr"] | .//*[@data-crlat="oddsBoostPrice"]'
    _amount_input_type = AmountForm
    _price_boost_label = 'xpath=.//*[@class="promo-label evflag_pb price-boost"] | .//*[@data-crlat="label.price-boost"]'
    _dropdown_list = 'xpath=.//*[@data-crlat="dropdown"]'

    def is_boosted_odds(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._boosted_odds, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name='Boosted odds not found')

    @property
    def odds_value(self):
        return self._wait_for_not_empty_web_element_text(selector=self._odds, timeout=1)

    @property
    def odds_dropdown(self):
        dropdown_we = self._find_element_by_selector(selector=self._odds_dropdownlist, context=self._we, timeout=1)
        return self._odds_dropdown_type(web_element=dropdown_we) if dropdown_we else None

    @property
    def odds(self):
        text_we = self._find_element_by_selector(selector=self._odds, timeout=0.5)
        if text_we:
            return self._get_webelement_text(we=text_we)
        elif self.odds_dropdown:
            return self.odds_dropdown.selected_market_selector_item
        else:
            return 'SP'  # for SP prices

    @property
    def is_original_odds_crossed(self):
        odds = self._find_element_by_selector(selector=self._odds, timeout=5)
        return wait_for_result(lambda: 'crossed' in odds.get_attribute('class'),
                               timeout=3,
                               name='Odds are boosted and crossed out')

    @property
    def is_original_odds_crossed_for_lp_sp_dropdown(self):
        odds = self._find_element_by_selector(selector=self._dropdown_list, timeout=5)
        return wait_for_result(lambda: 'dropdown secondary' in odds.get_attribute('class'),
                               timeout=3,
                               name='Odds are boosted and crossed out')

    def has_free_bet_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._free_bet_icon, timeout=0, context=self._we),
            name=f'Free Bet icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def price_boost_label(self):
        return self._find_element_by_selector(selector=self._price_boost_label, timeout=2, context=self._we)


class QuickBetBetSummary(BetNowSection):
    _stake_label = 'xpath=.//*[@data-crlat="label"]'
    _total_stake = 'xpath=.//*[@data-crlat="value"] | .//*[@data-crlat="combinedStake"]/span[2]'
    _free_bet_icon = 'xpath=.//*[@data-crlat="fbIcon"]'
    _est_returns_label = 'xpath=.//*[@data-crlat="estReturnsLabel"]'
    _combined_total_stake = 'xpath=.//*[@data-crlat="combinedStake"]'
    _free_bet_value = 'xpath=.//*[@data-crlat="fbValue"]'

    @property
    def free_bet_stake(self) -> str:
        return self.strip_currency_sign(self._get_webelement_text(selector=self._free_bet_value))

    @property
    def stake_label(self):
        return self._get_webelement_text(selector=self._stake_label, timeout=1)

    @property
    def est_returns_label(self):
        return self._get_webelement_text(selector=self._est_returns_label, timeout=1)

    def has_free_bet_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._free_bet_icon, timeout=0, context=self._we),
            name=f'Free Bet icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def combined_total_stake(self):
        """
        Get combined total stake value when free bet and simple stake is used.
        Example:
            - '£1.03 + £3.25', where first entrance - free bet value, second - entered stake value
        :return: combined total stake value when free bet and simple stake is used
        """
        text = self._wait_for_not_empty_web_element_text(selector=self._combined_total_stake, context=self._we,
                                                         timeout=2)
        return text.replace('\n', '')


class QuickBetSelection(ComponentBase):
    _qb_content = 'xpath=.//*[@data-crlat="quickbet.content"]'
    _qb_content_type = QuickBetContent
    _keyboard = 'xpath=.//*[@data-crlat="betslip.keyboard"]'
    _quick_stake = 'xpath=.//*[@data-crlat="quickStakePanel"]'
    _quick_stake_type = QuickStakePanel
    _bet_summary = 'xpath=.//*[@data-crlat="betSummary"]'
    _bet_summary_type = QuickBetBetSummary

    @property
    def content(self):
        return self._qb_content_type(selector=self._qb_content, context=self._we)

    @property
    def quick_stakes(self):
        return self._quick_stake_type(selector=self._quick_stake, context=self._we)

    @property
    def bet_summary(self):
        return self._bet_summary_type(selector=self._bet_summary, context=self._we)

    @property
    def keyboard(self):
        return Keyboard(selector=self._keyboard, context=self._we, timeout=2)


class Header(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="header.title"]'
    _close_button = 'xpath=.//*[@data-crlat="closeButton"]'

    @property
    def title(self):
        return self._wait_for_not_empty_web_element_text(selector=self._title, timeout=1)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    def has_close_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._close_button,
                                                   timeout=0) is not None,
            name=f'Close button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass


class QuickBetReceiptHeader(ComponentBase):
    _header_text = 'xpath=.//*[@data-crlat="receiptHeaderText"]'
    _header_timer = 'xpath=.//*[@data-crlat="receiptTime"]'
    _check_icon = 'xpath=.//*[@data-crlat="receiptIcon"]'

    @property
    def bet_placed_text(self):
        return self._get_webelement_text(selector=self._header_text, context=self._we)

    @property
    def receipt_datetime(self):
        return self._get_webelement_text(selector=self._header_timer, context=self._we)

    @property
    def check_icon(self):
        return ComponentBase(selector=self._check_icon, context=self._we)

    def has_bet_placed_text(self, timeout=3, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._header_text,
                                                   timeout=0) is not None,
            name=f'Header text to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class QuickBetReceiptBoostedSection(ComponentBase):
    _boosted_icon = 'xpath=.//*[@data-crlat="boostedIc"] | .//*[@class="qb-boosted-icon"]'
    _boosted_text = 'xpath=.//*[@data-crlat="boostedTxt"] | .//*[@class="qb-boosted-text"]'

    @property
    def icon(self):
        return ButtonBase(selector=self._boosted_icon)

    @property
    def text(self):
        return self._get_webelement_text(selector=self._boosted_text)


class QuickBetReceipt(ReceiptSingles):
    _reuse_selection = 'xpath=.//*[@data-crlat="reuseSelectionButton"] | .//*[@class="qb-reuse-button"]'
    _done_button = 'xpath=.//*[@data-crlat="doneButton"]'
    _free_bet_icon = 'xpath=.//*[@data-crlat="fbIcon"]'
    _boosted_section = 'xpath=.//*[@data-crlat="boostedSec"] | .//*[@class="qb-stake-boosted"]'
    _cash_out_label = 'xpath=.//*[@data-crlat="labelCashout"]'
    _header = 'xpath=.//*[@data-crlat="receiptHeader"]'
    _places = 'xpath=(.//*[@class="eachway-terms"])[1]'  # todo: 'xpath=.//*[@data-crlat="ewPlaces"]'
    _lines = 'xpath=.//*[@data-crlat="ewLines"]'
    _header_type = QuickBetReceiptHeader
    _price_boost_label = 'xpath=.//*[contains(@class, "promo-label evflag_pb price-boost")] | .//*[@data-crlat="label.price-boost"]'
    _selection_type = 'xpath=.//*[@data-crlat="selType"]'
    _odds_value = 'xpath=.//*[@data-uat="odds"]'
    _bet_id_label = 'xpath=.//*[@data-crlat="betId.label"]'
    _bet_id_value = 'xpath=.//*[@data-uat="betId"]'
    _selection_name = 'xpath=.//*[@data-uat="selectionName"]'
    _market_name = 'xpath=.//*[@data-uat="marketName"]'
    _event_name = 'xpath=.//*[@data-uat="eventName"]'
    _stake_label = 'xpath=.//*[@data-crlat="totalStake.label"]'
    _stake_value = 'xpath=.//*[@data-crlat="totalStake"]'
    _potential_return_label = 'xpath=.//*[@data-crlat="estimatedResults.label"]'
    _potential_return_value = 'xpath=.//*[@data-crlat="estimatedResults.value"]'
    _free_bet_stake = 'xpath=.//*[@data-crlat="fbValue"]'
    _trending_bets_type = TrendingBets
    _trending_bets = 'xpath=.//*[@data-crlat="trending-acc"]'

    def has_trending_bet_carousel(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._trending_bets, timeout=0) is not None,
            name=f'"trending bet carousel" shown status "{expected_result}"',
            timeout=timeout,
            expected_result=expected_result)

    @property
    def free_bet_stake(self) -> str:
        return self.strip_currency_sign(self._get_webelement_text(selector=self._free_bet_stake))

    @property
    def header(self):
        return QuickBetReceiptHeader(selector=self._header, context=self._we)

    @property
    def trending_bets_section(self):
        return self._trending_bets_type(selector=self._trending_bets, context=self._we)

    @property
    def reuse_selection_button(self):
        return ButtonBase(selector=self._reuse_selection, context=self._we)

    @property
    def done_button(self):
        return ButtonBase(selector=self._done_button, context=self._we)

    @property
    def places(self):
        return TextBase(selector=self._places, context=self._we, timeout=5)

    @property
    def lines(self):
        return TextBase(selector=self._lines, context=self._we, timeout=5)

    def has_cashout_label(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._cash_out_label,
                                                   timeout=0) is not None,
            name=f'Cashout label status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_free_bet_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._free_bet_icon, timeout=0, context=self._we),
            name=f'Free Bet icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def boosted_section(self):
        return QuickBetReceiptBoostedSection(selector=self._boosted_section, context=self._we)

    def has_price_boost_label(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._price_boost_label, timeout=3, context=self._we),
            name=f'price boost label status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def price_boost_label(self):
        return self._find_element_by_selector(selector=self._price_boost_label, timeout=2, context=self._we)

    @property
    def cashout_label(self):
        return self._find_element_by_selector(selector=self._cash_out_label, timeout=2, context=self._we)

    @property
    def selection_type(self):
        return self._get_webelement_text(selector=self._selection_type, timeout=2, context=self._we)

    @property
    def odds_value(self):
        return self._get_webelement_text(selector=self._odds_value, timeout=2, context=self._we)

    @property
    def bet_id_label(self):
        return self._get_webelement_text(selector=self._bet_id_label, timeout=2, context=self._we)

    @property
    def bet_id_value(self):
        return self._get_webelement_text(selector=self._bet_id_value, timeout=2, context=self._we)

    @property
    def selection_name(self):
        return self._get_webelement_text(selector=self._selection_name, timeout=2, context=self._we).replace('(', '').replace(')', '')

    @property
    def market_name(self):
        return self._get_webelement_text(selector=self._market_name, timeout=2, context=self._we)

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._event_name, timeout=2, context=self._we)

    @property
    def stake_label(self):
        return self._get_webelement_text(selector=self._stake_label, timeout=2, context=self._we)

    @property
    def stake_value(self):
        return self._find_element_by_selector(selector=self._stake_value, timeout=2, context=self._we)

    @property
    def potential_return_label(self):
        return self._get_webelement_text(selector=self._potential_return_label, timeout=2, context=self._we)

    @property
    def potential_return_value(self):
        return self._find_element_by_selector(selector=self._potential_return_value, timeout=2, context=self._we)


class QuickBetOverlay(Splash):
    _inner = 'xpath=.//*[@data-crlat="loading-overlay"]'

    def wait_to_hide(self, timeout=25):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._inner, timeout=0).is_displayed() is not True and
                               'true' in self._find_element_by_selector(selector=self._inner, timeout=0).get_attribute('hidden'),
                               timeout=timeout,
                               bypass_exceptions=(AttributeError, StaleElementReferenceException),
                               name='Quick Bet overlay to hide')


class QuickBetViewEntry(ComponentBase):
    _5_A_side_logo = 'xpath=.//*[@class="entrybadge-logo"]'
    _view_entry_title = 'xpath=.//*[@class="section-content"]/div[@class="title"]'
    _view_entry_button = 'xpath=.//*[@class="view-showdown-btn"]/button'

    def has_5_A_side_logo(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._5_A_side_logo,
                                                   timeout=0) is not None,
            name=f'5_A_side logo to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def view_entry_title(self):
        return self._get_webelement_text(selector=self._view_entry_title, timeout=0.2)

    @property
    def view_entry_button(self):
        return ButtonBase(selector=self._view_entry_button, timeout=0.2)


class QuickBet(ComponentBase):
    _header = 'xpath=.//*[@data-crlat="header"]'
    _header_type = Header
    _info_panel = 'xpath=.//*[@data-crlat="infPan.msg"][*]'
    _quickbet_selection = 'xpath=.//*[@data-crlat="quickbet.selection"]'
    _quickbet_selection_type = QuickBetSelection
    _quickbet_view_entry_type = QuickBetViewEntry
    _quickbet_receipt = 'xpath=.//*[@data-crlat="quickbetReceipt"]'
    _quickbet_lucky_dip_receipt = 'xpath=.//*[@id="quickbet-panel"]'
    _quickbet_receipt_type = QuickBetReceipt
    _selection_error = 'xpath=.//*[@data-crlat="selectionUndisplayed"]'
    _add_to_betslip_btn = 'xpath=.//*[@data-crlat="addToBetslipButton"]'
    _make_quick_deposit_btn = 'xpath=.//*[@data-crlat="quickDepositButton"]'
    _back_button = 'xpath=.//*[@data-crlat="quickbet.back"]'
    _deposit_and_place_bet_button = 'xpath=.//*[@data-crlat="quickbet.depositAndBet"]'
    # TODO need to unify auto attribute VOL-1344
    _place_bet_btn = 'xpath=.//*[@data-crlat="placeBetButton" ' \
                     'or @data-crlat="quickbet.depositAndBet" or @data-crlat="quickDepositButton"]'
    _deposit_form = 'xpath=.//*[@data-crlat="depositForm"]'
    _total_stake = 'xpath=.//*[@data-crlat="totalStake"]'
    _keyboard = 'xpath=.//*[@data-crlat="betslip.keyboard"]'
    _quick_stake_panel = 'xpath=.//*[@data-crlat="quickStakePanel"]'
    _odds_boost_button = 'xpath=.//*[@data-crlat="oddsBoostButton"]'
    _quick_deposit_panel = 'xpath=.//*[@data-crlat="quickDepositPanel"]'
    _each_way = 'xpath=.//*[@data-crlat="eachWayForm"]'
    _each_way_type = QuickBetEachWay
    _deposit_info_message = 'xpath=.//*[@class="reboost-info"]'
    _view_entry = 'xpath=.//*[@class="entry-confirmation"]'

    def __init__(self, *args, **kwargs):
        _logger = logging.getLogger('voltron_logger')
        _driver = get_driver()
        try:
            _container = 'id=quickbet-panel'
            element = self._find_element_by_selector(selector=_container, context=get_driver())
            element.click()
        except BaseException as e:
            _logger.info(f"QuickBet Component Not Found:\n\n {e}")
            pass  # element not found, this is expected if Quickbet Not Applicable
        try:
            _amount = 'xpath=//*[@data-crlat="quickbet.content"]//*[@data-crlat="stake.amountInputForm"]'
            element = self._find_element_by_selector(selector=_amount, context=_driver)
            element.click()
            is_focused = _driver.execute_script('return document.activeElement == document.getElementById("stake-input")')
            if not is_focused:
                _driver.execute_script('document.getElementById("stake-input").click()')
        except BaseException as e:
            _logger.info(f"QuickBet Reskin Component Not Found:\n\n {e}")
            pass  # element not found, this is expected if Quickbet Reskin Not Applicable
        super(QuickBet, self).__init__(*args, **kwargs)


    @property
    def deposit_info_message(self):
        return InfoPanel(selector=self._deposit_info_message, context=self._we, timeout=2)

    @property
    def odds_boost_button(self):
        return ButtonBase(selector=self._odds_boost_button, context=self._we)

    def has_odds_boost_button(self, timeout=3, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._odds_boost_button, context=self._we,
                                                   timeout=0) is not None,
            expected_result=expected_result,
            timeout=timeout,
            name='Waiting for odds boost button')
        return result

    @property
    def total_stake(self):
        result = wait_for_result(lambda: TextBase(selector=self._total_stake).value,
                                 timeout=3,
                                 name='Waiting for total stake')
        if result:
            return self.strip_currency_sign(result).replace(',', '')

    def wait_for_message_to_change(self, previous_message='', timeout=10):
        result = wait_for_result(lambda: self._get_webelement_text(selector=self._info_panel,
                                                                   timeout=0) != previous_message,
                                 name='Waiting for warning text to change',
                                 timeout=timeout,
                                 poll_interval=0.3)
        return result

    @property
    def selection(self):
        return self._quickbet_selection_type(selector=self._quickbet_selection, context=self._we)

    @property
    def view_entry(self):
        return self._quickbet_view_entry_type(selector=self._view_entry, context=self._we)

    def has_view_entry(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._view_entry, timeout=0) is not None,
                               name=f'View Entry button status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def header(self):
        return self._header_type(selector=self._header, context=self._we, timeout=1)

    def close(self):
        return self.header.close_button.click()

    @property
    def info_panels_text(self):
        return self.info_panels.texts

    @property
    def info_panels(self):
        return InfoPanel(selector=self._info_panel, context=self._we, timeout=15)

    @property
    def bet_receipt(self):
        return self._quickbet_receipt_type(selector=self._quickbet_receipt, context=self._we)

    @property
    def lucky_dip_outright_bet_receipt(self):
        return self._quickbet_receipt_type(selector=self._quickbet_lucky_dip_receipt)

    def wait_for_quick_bet_info_panel(self, expected_result=True, timeout=15):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._info_panel, timeout=0) is not None,
                               name='Quick Bet info panel to be present',
                               expected_result=expected_result,
                               timeout=timeout)

    def wait_for_bet_receipt_displayed(self, expected_result=True, timeout=10):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._quickbet_receipt, timeout=0,
                                                                      context=get_driver()) is not None,
                               name='Bet Receipt on Quick Bet is displayed',
                               expected_result=expected_result,
                               timeout=timeout)

    def wait_for_lucky_dip_bet_receipt_displayed(self, expected_result=True, timeout=10):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._quickbet_lucky_dip_receipt, timeout=0,
                                                                      context=get_driver()) is not None,
                               name='Bet Receipt on Quick Bet is displayed',
                               expected_result=expected_result,
                               timeout=timeout)
    @property
    def selection_error(self):
        return TextBase(selector=self._selection_error, timeout=15)

    @property
    def place_bet(self):
        context = QuickBetButtonBase(selector=self._place_bet_btn, context=self._we)
        context.is_enabled(timeout=0.5)
        return context

    @property
    def add_to_betslip_button(self):
        return QuickBetButtonBase(selector=self._add_to_betslip_btn, context=self._we)

    @property
    def make_quick_deposit_button(self):
        return QuickDepositButton(selector=self._make_quick_deposit_btn, context=self._we, timeout=5)

    def has_make_quick_deposit_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._make_quick_deposit_btn,
                                                   timeout=0) is not None,
            name=f'Quick deposit button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we)

    @property
    def deposit_and_place_bet_button(self):
        return QuickDepositButton(selector=self._deposit_and_place_bet_button, context=self._we)

    @property
    def quick_deposit_panel(self):
        return GVCQuickDeposit(selector=self._quick_deposit_panel, context=self._we, timeout=2)

    def wait_for_quick_deposit_panel(self, expected_result=True, timeout=15):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._quick_deposit_panel, timeout=0) is not None,
            expected_result=expected_result,
            name='Quick Bet panel to be displayed',
            timeout=timeout)

    @property
    def keyboard(self):
        return Keyboard(selector=self._keyboard, context=self._we, timeout=2)

    @property
    def quick_stake_panel(self):
        return QuickStakePanel(selector=self._quick_stake_panel, context=self._we, timeout=2)

    @property
    def is_quick_stake_panel_available(self):
        return self._find_element_by_selector(selector=self._quick_stake_panel, timeout=2) is not None

    @property
    def each_way_checkbox(self):
        self.scroll_to_we()
        return self._each_way_type(selector=self._each_way, context=self._we)
