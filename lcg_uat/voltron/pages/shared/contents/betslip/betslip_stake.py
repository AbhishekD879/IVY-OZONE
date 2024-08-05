import re
import tests
from voltron.pages.shared import get_device
from voltron.pages.shared.components.acca_insurance_offer import AccaInsuranceOffer
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.odds_boost_price_container import OddsBoostPriceContainer
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons import ImageIconBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.components.odds_drop_down import OddsDropdownList
from voltron.pages.shared.contents.betslip.bet_slip_stake_amount_form import BetSlipStakeAmountForm
from voltron.pages.shared.contents.betslip.betslip_each_way import EachWay
from voltron.pages.shared.contents.betslip.betslip_freebet_link import FreebetLink
from voltron.pages.shared.contents.betslip.betslip_stake_check_box_input import StakeCheckboxInput
from voltron.pages.shared.contents.betslip.betslip_tote_outcomes import MultipleToteOutcomes
from voltron.pages.shared.contents.betslip.betslip_tote_outcomes import SingleToteOutcomes
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


class BetslipStake(ComponentBase):
    def __init__(self, *args, **kwargs):
        super(BetslipStake, self).__init__(*args, **kwargs)
        self.scroll_to_we(web_element=self._we)

    _remove_btn = 'xpath=.//*[@data-crlat="stake.deleteButton"] | //*[@class="bs-overask-bet-remove-icon"]'
    _expand_stake = 'xpath=.//*[@data-crlat="expandStake"]'
    _info_icon = 'xpath=.//*[@data-crlat="stakeInfoButton"]'
    _expanded = 'xpath=.//*[@data-crlat="singleStake.header" or @data-crlat="complexStake.header"]'
    _outcome_name = 'xpath=.//*[@data-uat="selectionName" or @data-crlat="selectionName"]'
    _bets_multiplier = 'xpath=.//*[@data-crlat="stakeMultiplier"]'
    _bets_title = 'xpath=.//*[@data-crlat="stakeBetsTitle"]'
    _market_name = 'xpath=.//*[@data-uat="marketName"]'
    _event_name = 'xpath=.//*[@data-uat="eventName"]'
    _odds_boost_price = 'xpath=.//*[@data-crlat="oddsBoostPrice"]'
    _odds_boost_price_type = OddsBoostPriceContainer
    _odds_boost_info_icon = 'xpath=.//*[@data-crlat="infoButton"]'
    _odds = 'xpath=.//*[@data-crlat="odds"]'
    _old_odds = 'xpath=.//*[@data-crlat="oldOdds"]'
    _odds_dropdownlist = 'xpath=.//lp-sp-dropdown'
    _odds_dropdown_type = OddsDropdownList
    _price_change_arrows = 'xpath=.//*[@data-crlat="priceChangeArrows"]'
    _amount_input_form = 'xpath=.//*[@data-crlat="stake.amountInputForm"]'
    _est_returns_label = 'xpath=.//*[@data-crlat="estReturn.label"]'
    _est_returns = 'xpath=.//*[@data-crlat="estReturn"]'
    _each_way = 'xpath=.//*[@data-crlat="eachWayForm" or @data-uat="eachWay"]'
    _each_way_type = EachWay
    _freebet_stake = 'xpath=.//*[@data-crlat="addFreeBet"]'
    _freebet_tooltip = 'xpath=.//*[@data-crlat="fbTooltip"]'
    _remove_free_bet = 'xpath=.//*[@data-crlat="removeFB"]'
    _free_bet_value = 'xpath=.//*[@data-crlat="fbValue"]'
    _stake_error_msg = 'xpath=.//*[@data-crlat="stake.errorMessage"]'
    _stake_overask_msg = 'xpath=.//*[@data-crlat="stake.overaskMessage"]'
    _select_stake = 'xpath=.//*[@data-crlat="selectStakeCheckbox"]'
    _acca_insurance_offer = 'xpath=.//*[@data-crlat="accaContainer"]'
    _amount_input_type = BetSlipStakeAmountForm
    _tote_outcomes = 'xpath=.//*[@data-crlat="toteBetOutcomes"]'
    _tote_outcomes_type = SingleToteOutcomes
    _multiple_tote_outcomes = 'xpath=.//*[@data-crlat="toteBetSlip.multipleLegs"]'
    _multiple_tote_outcomes_type = MultipleToteOutcomes
    _event_date = 'xpath=.//*[@data-crlat="eventDate"]'
    _stake_content = 'xpath=.//*[@data-crlat="stakeContent"]'
    _offered_stake = 'xpath=.//*[@data-crlat="stakeValue"]'
    _undo_button = 'xpath=.//*[@data-crlat="oUndoBtn"] | .//*[contains(@class,"bs-overaks-undo-btn")]'
    _acca_insurance_icon = 'xpath=.//*[@data-crlat="accaInsIcon"]'
    _offered_price = 'xpath=.//*[@class="stake-odd-number"]'
    _previous_price = 'xpath=.//*[@class="stake-odd-number-prev"]'
    _odds_boost_info_tooltip = 'xpath=.//*[contains(@class, "tooltip tooltip-container")]'
    _ew_text = 'xpath=.//*[@data-crlat="oEWText"]'
    _ew_tick = 'xpath=.//*[@data-crlat="oEWTick"]'
    _win_only_text = 'xpath=.//*[contains(@class,"bs-stake-each-way")]'
    _leg_remove_marker = 'xpath=.//*[@class="bs-stake-info"]'

    @property
    def leg_remove_marker(self):
        return self._find_element_by_selector(selector=self._leg_remove_marker, context=self._we)

    @property
    def ew_text(self):
        return self._get_webelement_text(selector=self._ew_text)

    @property
    def ew_tick(self):
        return self._find_element_by_selector(selector=self._ew_tick)

    @property
    def win_only_text(self):
        return self._get_webelement_text(selector=self._win_only_text)

    @property
    def previous_price(self):
        return TextBase(selector=self._previous_price, context=self._we)

    @property
    def undo_button(self):
        return ButtonBase(selector=self._undo_button, context=self._we)

    def has_undo_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._undo_button,
                                                                      timeout=0.5) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Undo Button status to be "{expected_result}"')

    @property
    def offered_stake(self):
        return TextBase(selector=self._offered_stake, context=self._we)

    @property
    def offered_price(self):
        return TextBase(selector=self._offered_price, context=self._we)

    @property
    def suspended_stake_label(self):
        return self.after_element(selector=self._stake_content, context=self._we)

    @property
    def amount_form(self):
        return self._amount_input_type(selector=self._amount_input_form, context=self._we)

    def select(self):
        self._find_element_by_selector(selector=self._select_stake).click()

    @property
    def information_button(self):
        return ButtonBase(selector=self._info_icon, context=self._we)

    @property
    def name(self):
        return self.outcome_name

    @property
    def remove_button(self):
        return ButtonBase(selector=self._remove_btn, context=self._we)

    @property
    def outcome_name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._outcome_name, timeout=1).replace('(', '').replace(')', '')

    @property
    def outcome(self):
        return TextBase(selector=self._outcome_name, context=self._we)

    @property
    def bets_multiplier(self):
        return self._get_webelement_text(selector=self._bets_multiplier)

    @property
    def bets_title(self):
        return self._get_webelement_text(selector=self._bets_title)

    @property
    def market_name(self):
        name = self._get_webelement_text(selector=self._market_name, timeout=3)
        if name == "To Win" and 'virtual-sports' not in get_device().get_current_url():
            return 'Win or Each Way'
        return name

    def has_event_name(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._event_name, timeout=0) is not None,
                               name=f'Event name displayed status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def event_name(self):
        return normalize_name(self._wait_for_not_empty_web_element_text(selector=self._event_name, timeout=3))

    @property
    def has_event_date(self):
        return self._find_element_by_selector(selector=self._event_date, timeout=0.5) is not None

    @property
    def event_date(self):
        text = self._get_webelement_text(selector=self._event_date)
        if not text:
            text = ComponentBase(selector=self._event_date, context=self._we).get_attribute('innerHTML')
        return text

    @property
    def event_date_element(self):
        return TextBase(selector=self._event_date, context=self._we)

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
    def boosted_odds_container(self):
        return self._odds_boost_price_type(selector=self._odds_boost_price, context=self._we)

    @property
    def has_boosted_odds(self):
        return self._find_element_by_selector(selector=self._odds_boost_price, context=self._we, timeout=2) is not None

    @property
    def odds_boost_info_icon(self):
        return ImageIconBase(selector=self._odds_boost_info_icon, context=self._we, timeout=2)

    def has_odds_boost_info_icon(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._odds_boost_info_icon, timeout=3) is not None,
            name=f'Has odds boost info icon displayed status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def is_original_odds_crossed(self):
        odds = self._find_element_by_selector(selector=self._odds, timeout=5)
        return wait_for_result(lambda: 'boosted' in odds.get_attribute('class'),
                               timeout=3,
                               name='Odds are boosted and crossed out')

    @property
    def is_original_odds_crossed_for_lp_sp_dropdown(self):
        odds = self._find_element_by_selector(selector=self._odds, timeout=5)
        return wait_for_result(lambda: 'odds-value' in odds.get_attribute('class'),
                               timeout=3,
                               name='Odds are boosted and crossed out')

    @property
    def est_returns_label(self):
        return self._find_element_by_selector(selector=self._est_returns_label, context=self._we)

    @property
    def _est_returns_text(self):
        initial_text = wait_for_result(lambda: self._get_webelement_text(selector=self._est_returns, timeout=0),
                                       name='Waiting for estimate return', timeout=1)
        wait_for_result(lambda: initial_text != self._get_webelement_text(selector=self._est_returns, timeout=0),
                        name='Est. Return to change',
                        timeout=1)
        return self._get_webelement_text(selector=self._est_returns, timeout=0)

    @property
    def est_returns(self):
        est_returns = self._est_returns_text
        return self.strip_currency_sign(est_returns).replace(',', '') if est_returns else ''

    @property
    def est_returns_currency(self):
        result = self._est_returns_text
        return re.sub(r'\d+.\d+', '', result)

    @property
    def each_way_checkbox(self):
        self.scroll_to_we()
        return self._each_way_type(selector=self._each_way, context=self._we)

    def has_each_way_checkbox(self, expected_result=True, timeout=3):
        self.scroll_to_we()
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._each_way, timeout=0) is not None,
                               name=f'{self.__class__.__name__} Each Way displayed status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def get_free_bet_text(self):
        return self._get_webelement_text(selector=self._freebet_stake, timeout=5)

    @property
    def use_free_bet_link(self):
        return FreebetLink(selector=self._freebet_stake, context=self._we, timeout=5)

    def has_use_free_bet_link(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._freebet_stake, timeout=0) is not None,
                               name=f'Has Use Free Bet Button displayed status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def freebet_tooltip(self):
        return TextBase(selector=self._freebet_tooltip, context=self._we, timeout=1)

    def has_freebet_tooltip(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._freebet_tooltip, timeout=0) is not None,
                               name=f'Freebet tooltip status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    def has_odds_boost_tooltip(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._odds_boost_info_tooltip, timeout=0) is not None,
                               name=f'oddsboost tooltip status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    def odds_boost_tooltip(self):
        return self._find_element_by_selector(selector=self._odds_boost_info_tooltip, timeout=4)

    @property
    def remove_free_bet_link(self):
        return ButtonBase(selector=self._remove_free_bet, context=self._we, timeout=5)

    def has_remove_free_bet_link(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._remove_free_bet, timeout=0) is not None,
                               name=f'Remove Free Bet link displayed status to be {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def free_bet_stake(self) -> str:
        return self.strip_currency_sign(self._get_webelement_text(selector=self._free_bet_value))

    @property
    def error_message(self):
        return self._get_webelement_text(selector=self._stake_error_msg)

    def wait_for_error_message(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self.error_message,
                               name='BetslipStake error message to show up/hide',
                               expected_result=expected_result,
                               timeout=timeout)

    def wait_for_message_to_change(self, expected_message='', timeout=5):
        return wait_for_result(lambda: self.error_message == expected_message,
                               name=f'BetslipStake error message to equal "{expected_message}" ',
                               expected_result=True,
                               timeout=timeout)

    @property
    def overask_message(self):
        return self._get_webelement_text(selector=self._stake_overask_msg, timeout=1)

    def has_acca_insurance_offer(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._acca_insurance_offer, timeout=0) is not None,
            name=f'ACCA insurance offer displayed status is "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def acca_insurance_offer(self):
        return AccaInsuranceOffer(selector=self._acca_insurance_offer, context=self._we)

    @property
    def tote_outcomes(self):
        return self._tote_outcomes_type(selector=self._tote_outcomes, context=self._we, timeout=2)

    @property
    def multiple_tote_outcomes(self):
        return self._multiple_tote_outcomes_type(selector=self._multiple_tote_outcomes, context=self._we)

    @property
    def stake_checkbox(self):
        return StakeCheckboxInput(selector=self._select_stake, context=self._we, timeout=2)

    def has_remove_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._select_stake,
                                                                      timeout=0.5) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Remove Button status to be "{expected_result}"')

    def is_suspended(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: 'suspended' in self.get_attribute('class'),
                               name=f'Stake to become {expected_result}',
                               expected_result=expected_result,
                               timeout=timeout)

    def has_acca_insurance_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._acca_insurance_icon, timeout=0)is not None,
                               timeout=timeout,
                               name=f'"Acca Insurance Icon" presence to be {expected_result}',
                               expected_result=expected_result)


class LottoBetslipStake(BetslipStake):
    _est_returns = 'xpath=.//*[@class="est-Returns-Amt"]'
