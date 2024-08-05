import re
from abc import ABC
from collections import OrderedDict
from multidict import MultiDict
from selenium.common.exceptions import WebDriverException, NoSuchElementException, StaleElementReferenceException
import voltron.environments.constants as vec
from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.content_header import HeaderLine
from voltron.pages.shared.components.header_desktop import DesktopHeader
from voltron.pages.shared.components.match_center import MatchCenter
from voltron.pages.shared.components.primitives.buttons import FavouritesIcon, ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase, TextBase
from voltron.pages.shared.contents.betslip.betslip import UserHeader
from voltron.pages.shared.contents.betslip.betslip_overask_changed_multiple import OveraskChangedMultiple
from voltron.pages.shared.contents.betslip.betslip_overask_trader_offer import OveraskTraderOfferPrices
from voltron.pages.shared.contents.bet_receipt.bet_receipt_boosted_section import BetReceiptBoostedSection
from voltron.pages.shared.contents.trending_bets.trending_bets import TrendingBets
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result
from voltron.utils.js_functions import scroll_to_center_of_element


class ReceiptMultiples(ComponentBase):
    _multiples_header = 'xpath=.//*[@data-uat="selectionName"]'
    _receipt_bet_info = 'xpath=.//*[@data-crlat="singleStakeFooter"]'
    _item_odds = 'xpath=.//*[@data-uat="odds"] | //div[@data-crlat="betType"]/span'
    _description = 'xpath=.//*[@data-uat="selectionName"]'
    _market_type = 'xpath=.//*[@data-uat="marketName"]'
    _event_description = 'xpath=.//*[@data-uat="eventName"]'
    _fav_icon = 'xpath=.//*[@data-crlat="favouriteIcon"]'
    _multiple_boosted_section = 'xpath=.//*[@data-crlat="boostSect"]'
    _ew_terms = 'xpath=.//*[@data-crlat="eachWay"]'
    _total_stake = 'xpath=.//*[@data-crlat="receiptStakePerLineMulti"]'
    _ew_terms_each = 'xpath=.//span[@class="eachway-terms eachway-terms-multiple"]'
    _promo_icon = 'xpath=.//*[@data-crlat="promo.icon"]'
    _promo_label = 'xpath=.//*[@data-crlat="promo.label"]'
    _trending_bets_type = TrendingBets
    _trending_bets = 'xpath=.//*[@data-crlat="trending-acc"]'

    def has_trending_bet_carousel(self, expected_result=True, timeout=3):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._trending_bets, timeout=0) is not None,
            name=f'"trending bet carousel" shown status "{expected_result}"',
            timeout=timeout,
            expected_result=expected_result)

    @property
    def trending_bets_section(self):
        return self._trending_bets_type(selector=self._trending_bets, context=self._we)

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description, timeout=10).replace('(', '').replace(')', '')

    @property
    def market_type(self):
        return self._get_webelement_text(selector=self._market_type, timeout=10)

    @property
    def event_description(self):
        return self._get_webelement_text(selector=self._event_description, timeout=10)

    @property
    def item_odds(self):
        return self._get_webelement_text(selector=self._item_odds, timeout=10)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._multiples_header, timeout=10).replace('(', '').replace(')', '')

    def has_favourite_icon(self, expected_result=True, timeout=1) -> bool:
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._fav_icon, timeout=0) is not None,
            expected_result=expected_result,
            timeout=timeout,
            name=f'Icon presence status to be "{expected_result}"')

    def has_promo_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._promo_icon,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Icon status to be {expected_result}')

    @property
    def promo_label_text(self):
        return self._get_webelement_text(selector=self._promo_label)

    @property
    def multiple_boosted_section(self):
        return BetReceiptBoostedSection(selector=self._multiple_boosted_section, context=self._we)

    def has_multiple_boosted_section(self, timeout=1, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._multiple_boosted_section, timeout=0) is not None,
            name=f'boosted section to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result

    @property
    def ew_terms(self) -> str:
        return self._get_webelement_text(selector=self._ew_terms)

    @property
    def ew_terms_lines(self) -> str:
        return self._get_webelement_text(selector=self._ew_terms_each)

    @property
    def total_stake(self) -> str:
        return self.strip_currency_sign(self._get_webelement_text(selector=self._total_stake))


class LegItem(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="legItemTitle"]'
    _outcome = 'xpath=.//*[@data-crlat="itemOutcome"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def outcome(self):
        return self._get_webelement_text(selector=self._outcome)


class BetReceiptMultipleLegs(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="legItem"]'
    _list_item_type = LegItem


class ReceiptSingles(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="selectionName" or @data-uat="selectionName" or @data-crlat="selType"]'
    _bet_id = 'xpath=.//*[@data-crlat="betId.value"]'
    _event_name = 'xpath=.//*[@data-uat="eventName"]'
    _event_market = 'xpath=.//*[@data-uat="marketName"]'
    _line_at = 'xpath=.//*[@class="lines-info"]'
    _odds = 'xpath=.//*[@data-uat="odds"]'
    _total_stake = 'xpath=.//*[@data-crlat="totalStake"]'
    _est_returns = 'xpath=.//*[@data-uat="estReturns"]'
    _ew_terms = 'xpath=.//*[@data-crlat="eachWay"]'
    _fav_icon = 'xpath=.//*[@data-crlat="favouriteIcon"]'
    _runners_names = 'xpath=.//*[@data-crlat="runnerName"]'
    _runners_numbers = 'xpath=.//*[@data-crlat="runnerNumber"]'
    _multiple_legs = 'xpath=.//*[@data-crlat="multipleLegs"]'
    _free_bet_value = 'xpath=.//*[@data-crlat="fbValue"]'
    _multiple_legs_type = BetReceiptMultipleLegs
    _type_name = 'xpath=.//*[@data-crlat="selType"]'
    _cash_out = 'xpath=.//*[@class="cashout-label"]'
    _boosted_section = 'xpath=.//*[@data-crlat="boostSect"]'
    _lucky_dip_market_name = 'xpath=.//*[@class="promo-label small-icon"]'
    _lucky_dip_event_name = 'xpath=.//*[@class="qb-stake-description"]'
    _lucky_dip_successful_message = 'xpath=.//*[@data-crlat="receiptHeaderText"]'
    _lucky_dip_player_name = 'xpath=.//*[@class="selection-type"]'
    _lucky_dip_bet_id = 'xpath=.//*[@class="receipt-id"]/span[2]'
    _lucky_dip_odds = 'xpath=.//*[@class="qb-single-receipt-odds"][2]'
    _lucky_dip_total_stake = 'xpath=.//*[@class="qb-stake-footer"]/div[1]/span'
    _lucky_dip_estimate_returns = 'xpath=.//*[@class="qb-stake-footer"]/div[2]/span'
    _lucky_dip_close_button='xpath=.//*[@data-crlat="closeButton"]'

    @property
    def multiple_legs(self):
        return self._multiple_legs_type(selector=self._multiple_legs, context=self._we)

    @property
    def runners_names(self):
        runners_names = []
        for element in self._find_elements_by_selector(selector=self._runners_names):
            runners_names.append(self._get_webelement_text(we=element))
        return runners_names

    @property
    def runners_numbers(self):
        runners_numbers = []
        for element in self._find_elements_by_selector(selector=self._runners_numbers):
            runners_numbers.append(self._get_webelement_text(we=element))
        return runners_numbers

    @property
    def favourite_icon(self):
        return FavouritesIcon(selector=self._fav_icon, context=self._we)

    @property
    def name(self) -> str:
        return self._get_webelement_text(selector=self._name)

    @property
    def lucky_dip_market_name(self) -> str:
        return self._get_webelement_text(selector=self._lucky_dip_market_name)

    @property
    def lucky_dip_event_name(self) -> str:
        return self._get_webelement_text(selector=self._lucky_dip_event_name)

    @property
    def lucky_dip_bet_placement_messeage(self) -> str:
        return self._get_webelement_text(selector=self._lucky_dip_successful_message)
    @property
    def lucky_dip_player_name(self) -> str:
        return self._get_webelement_text(selector=self._lucky_dip_player_name)

    @property
    def lucky_dip_close_button(self):
        return self._find_element_by_selector(selector=self._lucky_dip_close_button)

    @property
    def lucky_dip_bet_id(self) -> str:
        return self._get_webelement_text(selector=self._lucky_dip_bet_id)

    @property
    def lucky_dip_odds(self) -> str:
        return self._get_webelement_text(selector=self._lucky_dip_odds)

    @property
    def lucky_dip_total_stake(self) -> str:
        return self.strip_currency_sign(self._get_webelement_text(selector=self._lucky_dip_total_stake))

    @property
    def lucky_dip_estimate_returns(self) -> str:
        return self.strip_currency_sign(self._get_webelement_text(selector=self._lucky_dip_estimate_returns)).replace(',', '')

    @property
    def bet_id(self) -> str:
        return self._get_webelement_text(selector=self._bet_id)

    @property
    def event_name(self) -> str:
        return normalize_name(self._get_webelement_text(selector=self._event_name))

    @property
    def event_market_name(self) -> str:
        return self._get_webelement_text(selector=self._event_market)

    @property
    def event_market(self) -> str:
        return self.event_market_name.replace(' /', '').strip()

    @property
    def line_at(self) -> str:
        return self._get_webelement_text(selector=self._line_at)

    @property
    def odds(self) -> str:
        return self._get_webelement_text(selector=self._odds)

    @property
    def unit_stake(self):
        raise VoltronException('There is no Unit stake on OX99 design. Please Update autotest')

    @property
    def ew_terms(self) -> str:
        return self._get_webelement_text(selector=self._ew_terms)

    @property
    def total_stake(self) -> str:
        return self.strip_currency_sign(self._get_webelement_text(selector=self._total_stake))

    @property
    def free_bet_stake(self) -> str:
        return self.strip_currency_sign(self._get_webelement_text(selector=self._free_bet_value))

    @property
    def estimate_returns(self) -> str:
        return self.strip_currency_sign(self._get_webelement_text(selector=self._est_returns)).replace(',', '')

    @property
    def est_returns_raw(self) -> str:
        return self._get_webelement_text(selector=self._est_returns)

    @property
    def estimate_returns_currency(self) -> str:
        est_returns = self._get_webelement_text(selector=self._est_returns)
        matched = re.match(u'^($|Kr|£|€)', est_returns)
        if matched:
            return matched.group(1)
        raise VoltronException(f'Failed parsing amount string: "{est_returns}"')

    @property
    def stake_currency(self) -> str:
        stake = self._get_webelement_text(selector=self._total_stake)
        matched = re.match(u'^($|Kr|£|€)', stake)
        if matched:
            return matched.group(1)
        raise VoltronException(f'Failed parsing amount string: "{stake}"')

    @property
    def type_name(self):
        return TextBase(selector=self._type_name, context=self._we)

    def has_cash_out_label(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._cash_out, timeout=0),
                               name=f'"Cash out" label presence status"{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def boosted_section(self):
        return BetReceiptBoostedSection(selector=self._boosted_section, context=self._we)

    def has_boosted_section(self, timeout=1, expected_result=True):
        result = wait_for_result(
            lambda: self._find_element_by_selector(selector=self._boosted_section, timeout=0) is not None,
            name=f'boosted section to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)
        return result


class Footer(ComponentBase):
    _reuse_selections_button = 'xpath=.//*[@data-crlat="reuseButton"]'
    _done_button = 'xpath=.//*[@data-crlat="doneButton"]'
    _stake = 'xpath=.//*[@data-crlat="stake"]'
    _total_stake = 'xpath=.//*[@data-crlat="totalStake"]'
    _total_est_returns = 'xpath=.//*[@data-crlat="totalEstReturns"]'
    _notification_message = 'xpath=.//*[@data-crlat="stake.errorMessage"]'
    _german_tax_message = 'xpath=.//*[@data-crlat="taxMessage"]'
    _free_bet_value = 'xpath=.//*[@data-crlat="fbValue"]'

    @property
    def message(self):
        return self._get_webelement_text(selector=self._notification_message, timeout=3)

    @property
    def stake(self):
        stake = self._find_element_by_selector(selector=self._stake).text
        return self.strip_currency_sign(stake)

    @property
    def free_bet_stake(self):
        return self.strip_currency_sign(self._get_webelement_text(selector=self._free_bet_value))

    @property
    def total_stake(self):
        stake = self._find_element_by_selector(selector=self._total_stake).text
        return self.strip_currency_sign(stake)

    @property
    def total_estimate_returns(self):
        stake = self._get_webelement_text(selector=self._total_est_returns, timeout=2)
        return self.strip_currency_sign(stake).replace(',', '')

    @property
    def total_est_returns_raw(self):
        return self._get_webelement_text(selector=self._total_est_returns, timeout=2)

    def has_reuse_selections_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._reuse_selections_button, timeout=0),
                               name=f'"Reuse Selections" button presence status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def reuse_selection_button(self):
        return ButtonBase(selector=self._reuse_selections_button, context=self._we)

    def has_done_button(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._done_button, timeout=0),
                               name=f'"Done" button presence status to be "{expected_result}"',
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def done_button(self):
        return ButtonBase(selector=self._done_button, context=self._we)

    def click_done(self):
        button = self.done_button
        """for some reason bet receipt after appearing jumps up on several pixels and looks like click on
        done button is not performed on button's center therefore it is not clicked at all """
        try:
            button.is_enabled(timeout=5)
            click(self.done_button._we)
        except (VoltronException, WebDriverException):
            self.done_button.is_enabled(timeout=5)
            click(self.done_button._we)
        is_closed = self.wait_for_element_disappear(we=self._we)
        if not is_closed:
            "TODO : added this as script is not able to click on done button"
            self._logger.info('*** Bet Receipt was not closed ***')
#           raise VoltronException('Bet Receipt was not closed')

    def has_german_tax_message(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._german_tax_message, timeout=0) is not None,
            name=f'"Tax message" message to be "{expected_result}"', expected_result=expected_result,
            timeout=timeout)

    @property
    def german_tax_message_text(self):
        return self._get_webelement_text(selector=self._german_tax_message, timeout=1)


class BetReceiptSection(ReceiptMultiples):
    _bet_id = 'xpath=.//*[@data-crlat="betId.value"]'
    _section_header = 'xpath=.//*[@data-crlat="betType"]/strong'
    _selections_count = 'xpath=.//*[@data-crlat="receiptsCounter"]'
    _receipt = 'xpath=.//*[contains(@data-crlat,"receiptLeg") or contains(@data-crlat, "receiptSingles")]'
    _multiple_bet_type = 'xpath=.//*[@data-crlat="multipleType"]'
    _multiplier = 'xpath=.//*[@data-crlat="multiplier"]'
    _template_types_dict = {
        vec.betslip.SINGLE: ReceiptSingles,
        'Multiples': ReceiptMultiples
    }
    _unit_stake = 'xpath=.//*[@data-crlat="unitStake"]'
    _total_stake = 'xpath=.//*[@data-crlat="receiptStakePerLineMulti"]'
    _est_returns = 'xpath=.//*[@data-uat="estReturns"]'
    _declined_bet = 'xpath=.//*[@data-crlat="declinedBet"]'
    _multiple_declined_bet = 'xpath=.//*[@data-crlat="declinedMultBet"]'
    _acca_sign_post = 'xpath=.//*[@data-crlat="promo.label"]'

    def has_acca_sign_post(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._acca_sign_post, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Acca sign post status to be "{expected_result}"')

    @property
    def unit_stake(self):
        return self.strip_currency_sign(self._get_webelement_text(selector=self._unit_stake, timeout=2))

    @property
    def total_stake(self):
        return self.strip_currency_sign(self._get_webelement_text(selector=self._total_stake, timeout=2))

    @property
    def total_stake_currency(self):
        total_stake = self._get_webelement_text(selector=self._total_stake)
        matched = re.match(r'^(\$|Kr|£|€)', total_stake)
        if matched:
            return matched.group(1)
        raise VoltronException(f'Failed parsing amount string: "{total_stake}"')

    @property
    def estimate_returns(self):
        return self.strip_currency_sign(self._get_webelement_text(selector=self._est_returns, timeout=2)).replace(',', '')

    @property
    def total_estimate_returns_currency(self):
        est_returns = self._get_webelement_text(selector=self._est_returns)
        matched = re.match(r'^(\$|Kr|£|€)', est_returns)
        if matched:
            return matched.group(1)
        raise VoltronException(f'Failed parsing amount string: "{est_returns}"')

    @property
    def template_type(self):
        crlat_attribute = self.get_attribute('data-crlat')
        self._logger.debug('*** Identifying template type by data-crlat attribute value "%s"' % crlat_attribute)
        for template_type_name in self._template_types_dict.keys():
            if template_type_name in crlat_attribute:
                return template_type_name
        else:
            raise VoltronException('Template type not in ["%s"]' % '", "'.join(self._template_types_dict.keys()))

    @property
    def name(self):
        crlat_attribute = self.get_attribute('data-crlat')
        if 'isSingles' in crlat_attribute:
            return vec.betslip.SINGLE
        elif 'isMultiples' in crlat_attribute:
            return self.multiple_bet_type
        else:
            raise VoltronException(f'Bet receipt section "{crlat_attribute}" is not known')

    @property
    def selections_count(self):
        return self._find_element_by_selector(selector=self._selections_count).text

    @property
    def items(self) -> list:
        items_we = self._find_elements_by_selector(selector=self._receipt, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_array = []
        for item_we in items_we:
            item_component = self._template_types_dict[self.template_type](web_element=item_we)
            items_array.append(item_component)
        return items_array

    @property
    def items_as_ordered_dict(self) -> MultiDict:
        items_we = self._find_elements_by_selector(selector=self._receipt, context=self._we)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_ordered_dict = MultiDict()
        for item_we in items_we:
            list_item = self._template_types_dict[self.template_type](web_element=item_we)
            items_ordered_dict.add(list_item.name, list_item)
        return items_ordered_dict

    @property
    def bet_type(self):
        return self._get_webelement_text(selector=self._section_header, timeout=3, context=self._we)

    @property
    def bet_id(self) -> str:
        return self._get_webelement_text(selector=self._bet_id, context=self._we)

    @property
    def multiple_bet_type(self) -> str:
        return self._get_webelement_text(selector=self._multiple_bet_type, context=self._we)

    @property
    def bet_multiplier(self) -> int:
        text = re.search(r'\d+', self._get_webelement_text(selector=self._multiplier, context=self._we))
        if text is None:
            raise VoltronException(f'Bet multiplier on UI "{text}" does not match expected pattern')
        return int(text.group(0))

    @property
    def declined_bet(self):
        return OveraskTraderOfferPrices(selector=self._declined_bet, context=self._we, timeout=5)

    @property
    def multiple_declined_bet(self):
        return OveraskChangedMultiple(selector=self._multiple_declined_bet, context=self._we, timeout=5)

    @property
    def multiple_odds_bet(self):
        return ReceiptMultiples(selector=self._multiple_declined_bet, context=self._we, timeout=5)


class BetReceiptSectionsList(ComponentBase):
    _item = 'xpath=.//*[contains(@data-crlat,"isSingles") or contains(@data-crlat, "isMultiples")]'
    _list_item_type = BetReceiptSection

    def _wait_active(self, timeout=10):
        self._we = self._find_myself()
        wait_for_result(lambda: self._find_element_by_selector(selector=self._local_spinner, timeout=0) is not None,
                        name='Local spinner appears',
                        timeout=1)
        result = wait_for_result(lambda: self.items_as_ordered_dict,
                                 timeout=timeout,
                                 name='Waiting for Bet Receipt items')
        if not result:
            raise VoltronException('There is no Bet Receipt items')


class BetReceiptBannerSection(ComponentBase):
    _banner = 'xpath=.//*[@data-crlat="betslipBannerLink"]'

    @property
    def banner(self):
        return LinkBase(selector=self._banner, context=self._we)

    @property
    def has_banner(self):
        return self._find_element_by_selector(selector=self._banner, timeout=2) is not None


class BetReceiptHeader(ComponentBase):
    _header_text = 'xpath=.//*[@data-crlat="receiptHeaderText"]'
    _header_timer = 'xpath=.//*[@data-crlat="receiptTime"]'
    _check_icon = 'xpath=.//*[@data-crlat="receiptIcon"]'

    @property
    def bet_placed_text(self):
        return self._get_webelement_text(selector=self._header_text, context=self._we)

    @property
    def bet_datetime(self):
        return self._get_webelement_text(selector=self._header_timer, context=self._we)

    @property
    def check_icon(self):
        return ComponentBase(selector=self._check_icon, context=self._we)


class SubHeader(ComponentBase):
    _receipts_counter = 'xpath=.//*[@data-crlat="receiptsCounter"]'
    _add_all_to_favourites_button = 'xpath=.//*[@data-crlat="favouritesAddAll"]'

    @property
    def bet_counter_text(self):
        return self._get_webelement_text(selector=self._receipts_counter, context=self._we)

    def has_add_all_to_favourites_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._add_all_to_favourites_button,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class BetReceipt(BetReceiptSection):
    _betreceipt_sections_list = 'xpath=.//*[@data-crlat="betreceiptSectionsContainer"]'
    _match_center = 'xpath=.//*[@data-crlat="matchCenter"]'
    _load_complete_pattern = 'xpath=.//*[@data-crlat="sidebarInner"]'
    _close_button = 'xpath=.//*[@data-crlat="sidebarClose"]'
    _page_title = 'xpath=.//*[@data-crlat="betslipHeader"]'
    _user_header = 'xpath=.//*[@data-crlat="sidebarMenuHeader"]'
    _banner_section = 'xpath=.//*[@data-crlat="betslipBanner"]'
    _footer = 'xpath=.//*[@data-crlat="bsFoot"]'
    _footer_type = Footer
    _header_line = 'xpath=.//header[@data-crlat="topBar"]'
    _header_line_type = HeaderLine
    _receipt_header = 'xpath=.//*[@data-crlat="receiptHeader"]'
    _receipt_header_type = BetReceiptHeader
    _receipt_sub_header = 'xpath=.//*[@data-crlat="receiptSubheader"]'
    _receipt_sub_header_type = SubHeader
    _cash_out_label = 'xpath=.//*[@data-crlat="labelCashout"]'
    _free_bet_icon = 'xpath=.//*[@data-crlat="fbIcon"]'
    _fade_out_overlay = True
    _verify_spinner = True
    _price_boost_label = 'xpath=.//*[@class="promo-label evflag_pb price-boost"] | .//*[@data-crlat="label.price-boost"]'
    _odds_boost_signpost = 'xpath=.//div[@class="bs-stake-boost"]'
    _bog_icon_signpost = 'xpath=.//*[@data-crlat="bogIcon"]'

    def _wait_active(self, open_status=True, timeout=15):
        """Waits for Bet Receipt widget to be opened of closed
           Just specify open status as a parameter, True goes for open, False - for close"""
        self._we = self._find_myself(timeout=timeout)
        return wait_for_result(
            lambda: 'is-visible' in self.get_attribute('class') and self._find_element_by_selector(selector=self._betreceipt_sections_list, timeout=0) is not None,
            name=f'Waiting for {self.__class__.__name__} form displayed',
            expected_result=open_status,
            timeout=timeout)

    @property
    def header_line(self):
        return self._header_line_type(selector=self._header_line)

    @property
    def user_header(self):
        return UserHeader(selector=self._user_header, timeout=1)

    @property
    def bet_receipt_header_name(self):
        return self._get_webelement_text(selector=self._page_title, context=self._we)

    def wait_for_page_title(self, page_title, timeout=10):
        if not wait_for_result(lambda: self.header_line.page_title.sport_title == page_title,
                               name='"%s" in page title' % page_title, timeout=timeout):
            self._logger.error(
                '*** Error waiting for title "%s", current is "%s"' % (
                    page_title,
                    self.header_line.page_title.sport_title))

    def is_displayed(self, expected_result=True, timeout=10, poll_interval=0.5, name=None, scroll_to=True,
                     bypass_exceptions=(NoSuchElementException, StaleElementReferenceException)):
        if not name:
            name = f'"{self.__class__.__name__}" displayed status is: {expected_result}'
        result = wait_for_result(lambda: self._find_element_by_selector(selector=self._betreceipt_sections_list, timeout=0) is not None,
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 bypass_exceptions=bypass_exceptions,
                                 name=name)
        return result

    @property
    def bet_receipt_sections_list(self):
        return BetReceiptSectionsList(selector=self._betreceipt_sections_list, context=self._we, timeout=30)

    @property
    def receipt_header(self):
        return self._receipt_header_type(selector=self._receipt_header, context=self._we, timeout=15)

    @property
    def receipt_sub_header(self):
        return self._receipt_sub_header_type(selector=self._receipt_sub_header, context=self._we, timeout=15)

    @property
    def cash_out_label(self):
        return ComponentBase(selector=self._cash_out_label, context=self._we, timeout=15)

    @property
    def footer(self):
        return self._footer_type(selector=self._footer, context=self._we)

    @property
    def match_center(self):
        return MatchCenter(self._match_center, context=self._we)

    @property
    def has_match_center(self):
        return self._find_element_by_selector(selector=self._match_center, timeout=0) is not None

    @property
    def banner_section(self):
        return BetReceiptBannerSection(self._banner_section, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we, timeout=1)

    def has_free_bet_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._free_bet_icon, timeout=3, context=self._we),
            name=f'Free Bet icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def price_boost_label(self):
        return ComponentBase(selector=self._price_boost_label, context=self._we, timeout=1)

    def has_price_boost_label(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._price_boost_label, timeout=3, context=self._we),
            name=f'price boost label status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_cashout_label(self, timeout=1, expected_result=True):
        return wait_for_result(
                lambda: self._find_element_by_selector(selector=self._cash_out_label,
                                                   timeout=0) is not None,
            name=f'Cashout label status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_odds_boost_signpost(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._odds_boost_signpost, timeout=1) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Odds boost sign post status to be "{expected_result}"')

    def has_bog_icon_signpost(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._bog_icon_signpost, timeout=1) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Odds boost sign post status to be "{expected_result}"')


class LottoBetReceiptSection(ComponentBase):
    _lottery_name = 'xpath=.//*[@data-uat="selectionName"]/span | .//*[@class="receipt-lable"]'
    _bet_id = 'xpath=.//*[@data-uat="selectionName"]/div | .//*[@data-uat="selectionName"]//*[@class="receiptId lotto-top-padng"]'
    _bet_receipt_selected_numbers = 'xpath=.//div[contains(@class,"selections-layout")]'
    _draws = 'xpath=.//*[@class="lotto-details-layout summary-details"]//*[@class="lotto-top-padng"] | .//*[@class="lotto-details-layout summary-details"]//*[contains(@class,"nOfDraws")]'
    _show_hide_summary = 'xpath=.//*[@class="lotto-details-layout summary-details"]//div[contains(@class,"show-hide-accordion")]'
    _draw_heading = 'xpath=.//div[contains(@class,"lotto-details-layout summary")]//*[contains(@class,"lotto-heading")]'
    _draw_date = 'xpath=.//*[contains(@class,"lotto-text-format")]//*[@data-uat="selectionName"] | .//*[contains(@class,"lotto-desc lotto")]'
    _total_stake_label = 'xpath=.//*[@class="lotto-details-layout lotto-text-format"]//*[@class="total-lable"]'
    _total_stake_value = 'xpath=.//*[@class="lotto-details-layout lotto-text-format"]//*[@class="total-lable"]//following-sibling::span[@class="est-Returns-Amt"] | .//*[@class="lotto-details-layout lotto-text-format"]//*[@class="total-lable"]//following-sibling::div[@class="est-Returns-Amt"]'
    _est_returns_label = 'xpath=.//*[@class="lotto-details-layout lotto-text-format"]//*[@data-crlat="estReturn.label"]'
    _est_returns_value = 'xpath=.//*[@class="lotto-details-layout lotto-text-format"]//*[@data-crlat="estReturn.label"]/following-sibling::span | .//*[@class="lotto-details-layout lotto-text-format"]//*[@data-crlat="estReturn.label"]/following-sibling::div'
    _outer_total_stake_label = 'xpath=.//*[@class="lotto-details-layout"]//*[@class="total-lable"]'
    _outer_total_stake_value = 'xpath=.//*[@class="lotto-details-layout"]//*[@class="total-lable"]/following-sibling::span[@class="est-Returns-Amt"]'
    _outer_est_returns_label = 'xpath=.//span[contains(@class, "lotto-text-format")]//*[@class="total-lable"] | .//div[contains(@class,"lotto-info lotto")]//*[@class="total-lable"]'
    _outer_est_returns_value = 'xpath=.//*[@class="lotto-info lotto-text-format"]//*[@class="total-lable"]/following-sibling::span[@class="est-Returns-Amt"] | .//*[@class="lotto-info lotto-top-padng"]//*[@class="total-lable"]/following-sibling::span[@class="est-Returns-Amt"]'

    @property
    def name(self):
        return f'{self._get_webelement_text(selector=self._lottery_name, context=self._we)}-{self.draw_heading}-' \
               f'{self.draw_date}-{" ".join(self.betslip_selected_numbers)}'

    @property
    def bet_id(self):
        return self._get_webelement_text(selector=self._bet_id, context=self._we)

    @property
    def show_hide_summary(self):
        return ButtonBase(selector=self._show_hide_summary, context=self._we)

    @property
    def lottery_name(self):
        return self._get_webelement_text(selector=self._lottery_name, context=self._we).replace('(', '').replace(')', '')

    @property
    def betslip_selected_numbers(self):
        items_we = self._find_elements_by_selector(selector=self._bet_receipt_selected_numbers, context=self._we,
                                                   timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} items')
        items_array = []
        for item_we in items_we:
            if item_we.is_displayed():
                item_component = self._get_webelement_text(we=item_we)
                items_array.append(item_component)
        return items_array

    @property
    def draws(self):
        return self._get_webelement_text(selector=self._draws, context=self._we)

    @property
    def draw_heading(self):
        return self._get_webelement_text(selector=self._draw_heading, context=self._we)

    @property
    def draw_date(self):
        items_we = self._find_elements_by_selector(selector=self._draw_date, context=self._we, timeout=self._timeout)
        self._logger.debug(f'*** Found {len(items_we)} draw date items')
        items_array = ', '.join(self._get_webelement_text(we=we) for we in items_we if we.is_displayed())
        return items_array

    @property
    def total_stake_label(self):
        return self._get_webelement_text(selector=self._total_stake_label, context=self._we)

    @property
    def total_stake_value(self):
        return self._get_webelement_text(selector=self._total_stake_value, context=self._we).replace('£', "")

    @property
    def est_returns_label(self):
        return self._get_webelement_text(selector=self._est_returns_label, context=self._we)

    @property
    def est_returns_value(self):
        return self._get_webelement_text(selector=self._est_returns_value, context=self._we).replace('£', "")

    @property
    def outer_total_stake_label(self):
        return self._get_webelement_text(selector=self._outer_total_stake_label, context=self._we)

    @property
    def outer_total_stake_value(self):
        return self._get_webelement_text(selector=self._outer_total_stake_value, context=self._we).replace('£', "")

    @property
    def outer_est_returns_label(self):
        return self._get_webelement_text(selector=self._outer_est_returns_label , context=self._we)

    @property
    def outer_est_returns_value(self):
        return self._get_webelement_text(selector=self._outer_est_returns_value, context=self._we).replace('£', "")


class LottoBetReceipt(BetReceipt):
    _item = 'xpath=.//div[contains(@class,"lotto-bet-receipt")]'
    _list_item_type = LottoBetReceiptSection

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        _show_hide_summary = 'xpath=.//*[@class="lotto-details-layout summary-details"]//div[contains(@class,"show-hide-accordion")]'
        show_hide_summary_buttons_we = self._find_elements_by_selector(selector=_show_hide_summary, context=self._we,
                                                                       timeout=self._timeout)
        show_hide_summary_buttons_count = 0
        for item in show_hide_summary_buttons_we:
            scroll_to_center_of_element(item)
            item.click()
            show_hide_summary_buttons_count += 1
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        if show_hide_summary_buttons_count != len(items_we):
            raise VoltronException(
                message=f'count of element "show hide summary buttons" {show_hide_summary_buttons_count} and found bet recipt section web elements {len(items_we)} is not equal')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({list_item.name: list_item})
        return items_ordered_dict


class BetReceiptDesktop(BetReceipt):
    _header_desktop = 'xpath=.//vn-responsive-header'
    _header_desktop_type = DesktopHeader

    def _wait_active(self, open_status=True, timeout=15):
        self._we = self._find_myself(timeout=3)
        return wait_for_result(
            lambda: self._we.is_displayed(),
            name=f'{self.__class__.__name__} - BetReceipt widget displayed status to be {open_status}',
            expected_result=open_status,
            timeout=timeout
        )

    @property
    def user_header(self):
        return self._header_desktop_type(selector=self._header_desktop, context=get_driver())

    @property
    def close_button(self):
        self._logger.warning('*** Close button is not present on Desktop. Use this property only for closing widget')
        return self.footer.done_button

    @property
    def bet_receipt_header_name(self):
        raise NotImplementedError('Desktop site does not have "BET RECEIPT" header')


class LottoBetReceiptDesktop(LottoBetReceipt, BetReceiptDesktop, ABC):
    pass
