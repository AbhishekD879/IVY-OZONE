import voltron.environments.constants as vec
from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.collection import Collection
from voltron.pages.shared.contents.betslip.betslip_overask_trader_offer import OveraskTraderOfferPrices
from voltron.pages.shared.contents.betslip.betslip_section_list_collection import BetSlipSectionsListCollection
from voltron.pages.shared.contents.betslip.betslip_stake import BetslipStake, LottoBetslipStake
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.pages.shared.contents.betslip.bet_slip_stake_amount_form import BetSlipStakeAmountForm
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class BetSlipSectionHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="bsHeadMsg"]'
    _count = 'xpath=.//*[@data-crlat="bsHeadCount"]'

    @property
    def count(self):
        return self._get_webelement_text(selector=self._count, timeout=1)

    @property
    def title_text(self):
        return self._get_webelement_text(selector=self._title, timeout=1)


class BetSlipSection(Collection, Accordion):
    _section_accordion = 'xpath=.//*[@data-crlat="accordion"]'
    _item = 'xpath=.//*[@data-crlat="betslip.stake"]'
    _list_item_type = BetslipStake
    _all_stakes = 'xpath=.//preceding-sibling::*[@data-crlat="betslip.allStakesContainer"]'
    _all_stakes_section = BetslipStake
    _all_stakes_label = 'xpath=.//preceding-sibling::*[@data-crlat="betslip.allStakesContainer"]/.//*[@data-crlat="label.allStakes"]'
    _overask_section_type = OveraskTraderOfferPrices
    _promo_icon = 'xpath=.//*[@data-crlat="promo.icon"]'

    @property
    def _attr(self):
        return self.get_attribute('data-crlat')

    @property
    def name(self):
        name_dict = {'singles': vec.betslip.BETSLIP_SINGLES_NAME,
                     'acca': vec.betslip.MULTIPLES,
                     'multiples': vec.betslip.MULTIPLES}
        name = name_dict.get(self._attr)
        if not name:
            raise VoltronException(message=f'Unrecognized betslip attribute: "{self._attr}"')
        self._logger.debug(f'*** Betslip section name: "{name}"')
        return name

    def has_all_stakes(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._all_stakes,
                                                   timeout=0) is not None,
            name=f'All stakes status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def all_stakes_label(self):
        return self._get_webelement_text(selector=self._all_stakes_label)

    @property
    def all_stakes_section(self):
        return self._all_stakes_section(self._all_stakes)

    @property
    def overask_trader_offer(self):
        return self._overask_section_type(selector=self._item, context=self._we)

    def has_promo_icon(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._promo_icon,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Icon status to be {expected_result}')


class BetSlipSectionsList(BetSlipSectionsListCollection):
    _item = 'xpath=(.//*[@data-crlat="singles" or @data-crlat="multiples" or @data-crlat="acca"][*])'
    _list_item_type = BetSlipSection
    _section_header_type = BetSlipSectionHeader
    _multiple_header = 'xpath=.//*[@data-crlat="multiplesHeader"]'
    _default_notification = 'xpath=.//*[contains(@class,"bs-notification")]'
    _fade_out_overlay = True

    @property
    def multiple_selections_count(self):
        return self.multiple_header.count

    @property
    def multiple_selections_label(self):
        return self.multiple_header.title_text

    @property
    def multiple_header(self):
        return self._section_header_type(self._multiple_header, context=self._we)

    @property
    def default_notification(self):
        return self._get_webelement_text(selector=self._default_notification, context=self._we, timeout=1)


class LottoBetSlipSection(Accordion):
    _selection_name = 'xpath=.//*[@data-uat="selectionName"]'
    _show_hide_summary = 'xpath=.//*[@data-uat="selectionName"]//following-sibling::div[@class="show-hide-accordion"]'
    _draw_heading = 'xpath=.//*[@class="lotto-top-pad on-expand"]//*[@class="lotto-heading"]'
    _draw_date = 'xpath=.//*[@class="lotto-top-pad on-expand"]//*[@data-uat="selectionName"]'
    _total_stake_label = 'xpath=.//*[@class="lotto-details-layout lotto-text-format"]//*[@class="total-lable"]'
    _total_stake_value = 'xpath=.//*[@class="lotto-details-layout lotto-text-format"]//*[@class="est-Returns-Amt"]'
    _est_returns_label = 'xpath=.//*[@class="lotto-details-layout lotto-text-format"]//*[@data-crlat="estReturn.label"]'
    _est_returns_value = 'xpath=.//*[@class="lotto-details-layout lotto-text-format"]/*[@data-crlat="totalestReturnsAmount"]'
    _betslip_selected_numbers = 'xpath=.//div[contains(@class,"numbercol")]'
    _amount_input_form = 'xpath=.//*[@data-crlat="stake.amountInputForm"]'
    _amount_input_type = BetSlipStakeAmountForm
    _remove_line = 'xpath=.//*[@class="remove-line"]'
    _show_hide_multiples = 'xpath=.//*[contains(@class,"lotto-details-layout lotto-summary")]//*[@class="show-hide-accordion"]/span'
    _over_all_est_returns_label = 'xpath=.//*[@class="lotto-details-layout lotto-summary"]//*[@data-crlat="estReturn.label"]'
    _over_all_est_returns_value = 'xpath=.//*[@class="lotto-details-layout lotto-summary"]//*[@data-crlat="estReturn.label"]/following-sibling::span'
    _item = 'xpath=.//*[contains(@class,"lotto-details-layout lotto-wrapper lotto-padding padng")]'
    _list_item_type = LottoBetslipStake

    @property
    def name(self):
        return f'{self._get_webelement_text(selector=self._selection_name, context=self._we)}-{self.draw_heading}-' \
               f'{self.draw_date}-{" ".join(self.betslip_selected_numbers)}'

    @property
    def show_hide_summary(self):
        return ButtonBase(selector=self._show_hide_summary, context=self._we)

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
    def remove_line(self):
        return ButtonBase(selector=self._remove_line, context=self._we)

    @property
    def show_hide_multiples(self):
        return ButtonBase(selector=self._show_hide_multiples, context=self._we)

    @property
    def over_all_est_returns_label(self):
        return self._get_webelement_text(selector=self._over_all_est_returns_label, context=self._we)

    @property
    def over_all_est_returns_value(self):
        return self._get_webelement_text(selector=self._over_all_est_returns_value, context=self._we).replace('£', "")

    @property
    def betslip_selected_numbers(self):
        items_we = self._find_elements_by_selector(selector=self._betslip_selected_numbers, context=self._we,
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
    def amount_form(self):
        return self._amount_input_type(selector=self._amount_input_form, context=self._we)


class LottoBetSlipSectionsList(ComponentBase):
    _item = 'xpath=.//*[@class="lotto-content"]'
    _list_item_type = LottoBetSlipSection
