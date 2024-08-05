from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.contents.my_bets.cashout import BetDetails
from voltron.utils.waiters import wait_for_result
from selenium.common.exceptions import StaleElementReferenceException


class Ball(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class Balls(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="ball"]'
    _list_item_type = Ball


class LottoBet(ComponentBase):
    _ball = 'xpath=.//*[@data-crlat="ball"]'
    _balls = 'xpath=.//*[@data-crlat="balls"]'
    _draw_name = 'xpath=.//*[@data-crlat="drawName"]'
    _status = 'xpath=.//*[@data-crlat="bet.status"]'
    _open_bet_lottery_name = 'xpath=.//*[@data-crlat="cashout.item.header"]'
    _open_bet_draw_heading = 'xpath=.//*[contains(@class,"lotto-bet-panel")]/*[@class="draw-name"]/*[@data-crlat="drawName"] | .//*[contains(@class,"lotto-bet-panel")]/*[contains(@class,"draw-name lad")]'
    _open_bet_draw_date = 'xpath=.//*[@data-crlat="drawName"]//following-sibling::span[@data-crlat="settledAt"]'
    _open_bet_selected_numbers = 'xpath=.//*[@class="lotto-balls"]/*[@data-crlat="ball"]'
    _open_bet_total_stake_label = 'xpath=.//*[@data-crlat="stake"]/*[@data-crlat="label"]'
    _open_bet_total_stake_value = 'xpath=.//*[@data-crlat="stake"]/*[@data-crlat="value"]'
    _open_bet_est_returns_label = 'xpath=.//*[@data-crlat="estimatedReturns"]/*[@data-crlat="label"]'
    _open_bet_est_returns_value = 'xpath=.//*[@data-crlat="estimatedReturns"]//following-sibling::span[@data-crlat="value"]'
    _open_bet_bet_id = 'xpath=.//*[@data-crlat="betReceipt"]/*[@data-crlat="value"]'
    _date = 'xpath=.//*[@data-crlat="settledAt"]'
    _bet_details = 'xpath=.//*[contains(@class,"betDetailsAccordion-lads")] | .//*[contains(@class,"betDetailsAccordion-coral")]/*[@data-crlat="accordion"]'
    _chevron_arrow = 'xpath=.//*[@data-crlat="chevronArrow"]'
    _subscription_message = 'xpath=.//*[@class="description-value"]'

    # @property
    # def name(self):
    #     """
    #     :return name in format:
    #     "{casino_name} - [{draw_name} {date}]", e.g. 'SINGAPORE 6 BALL DRAW - [Monday Draw 13.05 11:30 AM]'
    #     """
    #     name = '%s - [%s %s]' % (self.bet_type, self.draw_name, self.date)
    #     return name

    @property
    def name(self):
        return f'{self._get_webelement_text(selector=self._open_bet_lottery_name, context=self._we).lower()}-{self.draw_heading}-' \
               f'{self.draw_date}-{" ".join(self.open_bet_selected_numbers)}'

    @property
    def lottery_name(self):
        return self._get_webelement_text(selector=self._open_bet_lottery_name, context=self._we)

    @property
    def bet_id(self):
        return self._get_webelement_text(selector=self._open_bet_bet_id, context=self._we)

    @property
    def draw_heading(self):
        return self._get_webelement_text(selector=self._open_bet_draw_heading, context=self._we).lower()

    @property
    def draw_date(self):
        items_we = self._find_elements_by_selector(selector=self._open_bet_draw_date, context=self._we, timeout=self._timeout)
        self._logger.debug(f'*** Found {len(items_we)} lotto open bet draw date items')
        items_array = ', '.join(self._get_webelement_text(we=we).lower() for we in items_we if we.is_displayed())
        return items_array

    @property
    def open_bet_selected_numbers(self):
        items_we = self._find_elements_by_selector(selector=self._open_bet_selected_numbers, context=self._we,
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
    def total_stake_label(self):
        return self._get_webelement_text(selector=self._open_bet_total_stake_label, context=self._we)

    @property
    def total_stake_value(self):
        return self._get_webelement_text(selector=self._open_bet_total_stake_value, context=self._we).replace('£', "")

    @property
    def potential_returns_label(self):
        return self._get_webelement_text(selector=self._open_bet_est_returns_label, context=self._we)

    @property
    def potential_returns_value(self):
        return self._get_webelement_text(selector=self._open_bet_est_returns_value, context=self._we).replace('£', "")

    @property
    def ball(self):
        return Balls(selector=self._ball, context=self._we)

    @property
    def balls(self):
        return Balls(selector=self._balls, context=self._we)

    @property
    def draw_name(self):
        return self._get_webelement_text(selector=self._draw_name)

    @property
    def draw_name_alignment(self):
        return ComponentBase(selector=self._draw_name, context=self._we).css_property_value('text-align')

    @property
    def date(self):
        return self._get_webelement_text(selector=self._date)

    @property
    def status(self):
        return self._get_webelement_text(selector=self._status, context=self._we)

    @property
    def potential_returns(self):
        return ComponentBase(selector=self._open_bet_est_returns_value, context=self._we)

    @property
    def bet_details(self):
        return BetDetails(selector=self._bet_details, context=self._we)

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException,)):
        section = self._find_element_by_selector(
            selector="xpath=.//*[contains(@class,'myBetsAccordion-lads')] | .//*[contains(@class,'myBetsAccordion')]/*[@data-crlat='accordion']",
            context=self._we)
        result = wait_for_result(lambda: 'is-expanded' in section.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'"{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result

    @property
    def chevron_arrow(self):
        return ButtonBase(selector=self._chevron_arrow, context=self._we)

    @property
    def subscription_message(self):
        return self._get_webelement_text(selector=self._subscription_message, context=self._we)

    def has_bet_details(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._bet_details, timeout=timeout, context=self._we),
            name=f'Bet Details section shown status to be {expected_result}',
            expected_result=expected_result,
            timeout=timeout)
