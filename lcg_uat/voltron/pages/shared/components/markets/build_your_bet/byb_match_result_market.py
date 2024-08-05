from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from collections import OrderedDict
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.components.markets.match_result_market import MatchResultMarket, MarketOutcomesList, Outcome
from voltron.utils.js_functions import scroll_to_center_of_element
from voltron.utils.waiters import wait_for_result


class BYBBetButton(BetButton):

    def wait_for_betslip_animation_disappear(self):
        """
        Bypassing wait for Betslip animation as it\'s not present for Build Your Bet
        """
        pass


class BYBOutcome(Outcome):
    _output_price_button = 'xpath=.//*[@class="switcher-name"] | .//*[@data-crlat="betButton"]'

    @property
    def outcome_name(self):
        return self._get_webelement_text(selector=self._output_price_button)

    @property
    def bet_button(self):
        return BYBBetButton(selector=self._output_price_button, context=self._we)
    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        result = wait_for_result(lambda: 'active' in self.get_attribute('class'),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result


class BYBMarketOutcomesList(MarketOutcomesList):
    _item = 'xpath=.//*[@id="switch-custom"]'
    _list_item_type = BYBOutcome

    @property
    def current(self) -> str:
        scroll_to_center_of_element(self._we)
        active_button_name = wait_for_result(
            lambda: next((button_name for button_name, button in self.items_as_ordered_dict.items()
                          if button.is_selected(timeout=0.5)), ''),
            name=f'{self.__class__.__name__} - {self._list_item_type.__name__} to be active',
            timeout=1.5)
        self._logger.debug(
            f'*** Active {self.__class__.__name__} - {self._list_item_type.__name__} name is "{active_button_name}"')
        return active_button_name


class BYBMatchResultMarket(MatchResultMarket):
    _outcomes_list = 'xpath=.//*[@class="switchers-container"]'
    _time_period_outcomes = 'xpath=.//byb-custom-component//byb-custom-component//*[@class="switchers-container"]'
    _add_to_betslip_btn = 'xpath=.//*[@class="btn-group btn btn-active" or @class="btn-group btn btn-active-lads"]'
    _outcomes_list_type = BYBMarketOutcomesList
    _verify_spinner = True

    def _wait_active(self, timeout=0):
        if self.is_expanded(timeout=0):
            wait_for_result(lambda: (self._find_element_by_selector(selector=self._outcomes_list, timeout=0) and
                                     self._find_element_by_selector(selector=self._outcomes_list, timeout=0).is_displayed()),
                            timeout=0.5,
                            name=f'{self._outcomes_list_type.__name__} to load in {self.__class__.__name__}',
                            bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, AttributeError))

    @property
    def time_period_outcomes_list(self):
        return self._outcomes_list_type(selector=self._time_period_outcomes, context=self._we)

    def set_market_selection(self, time=False, **kwargs):
        """
        :param kwargs: Prioritized market selection parameters:
          - add selection outcome by name  if 'selection_name' specified;
          - add selection outcome by index if 'selection_index' specified;
          - add specified selections count is 'count' specified;
          - add all market selections if **kwargs empty
        :return: selection_names: List of added selections names
        """
        if time:
            wait_for_result(lambda: len(self.time_period_outcomes_list.items_as_ordered_dict.keys()) > 1,
                            name=f'"{self.name} – {self.__class__.__name__}" - "{self._outcomes_list_type.__name__}" to load',
                            timeout=3)
            selections_list = self.time_period_outcomes_list.items_as_ordered_dict
        else:
            wait_for_result(lambda: len(self.outcomes.items_as_ordered_dict.keys()) > 1,
                            name=f'"{self.name} – {self.__class__.__name__}" - "{self._outcomes_list_type.__name__}" to load',
                            timeout=3)
            selections_list = self.outcomes.items_as_ordered_dict
        selection_index = kwargs.get('selection_index', None)
        count = kwargs.get('count', None)
        selection_names = list(selections_list.keys())[:count] if count else list(selections_list.keys())

        selection_name = kwargs.get('selection_name',
                                    str(list(selections_list.keys())[selection_index - 1])
                                    if selection_index
                                    else selection_names)

        if isinstance(selection_name, str):
            selection_names = [selection_name, ]

        for name in selection_names:
            selections_list[name].bet_button.click()
            self._logger.info(f'*** Selected selection is: "{name}"')
        return selection_names


class BYBMatchResultMarketSwitcher(BYBMatchResultMarket):
    _grouping_selection_buttons = 'xpath=.//*[@data-crlat="switchers"]'
    _grouping_selection_buttons_type = GroupingSelectionButtons


class BYBTotalGoalsMarketOutcomesList(MarketOutcomesList):
    _item = 'xpath=.//*[@id="switch-custom"]'
    _list_item_type = BYBOutcome

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        items_we = self._find_elements_by_selector(selector=self._item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            items_ordered_dict.update({item_we.text: list_item})
        return items_ordered_dict


class BYBTotalGoalsMarket(BYBMatchResultMarket):
    _time_period_outcomes = 'xpath=.//byb-teamname-component//byb-timeline//*[@class="switchers-container"]'
    _outcomes_list_type = BYBTotalGoalsMarketOutcomesList
    _goals_outcomes = 'xpath=.//byb-increment//*[@class="btn-group"]'
    _increment = 'xpath=.//byb-counter//*[@class="sign-button sign-disabled"][2]'

    @property
    def goals_outcomes_list(self):
        return self._outcomes_list_type(selector=self._goals_outcomes, context=self._we)

    def goal_increment_by_value(self, value=1):
        we = self._find_element_by_selector(selector=self._increment)
        Flag = True
        while Flag:
            if we.text == value:
                Flag = False
            else:
                we.click()
