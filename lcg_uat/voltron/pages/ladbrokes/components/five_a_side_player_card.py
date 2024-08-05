from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import DefaultBetButton
from voltron.utils.waiters import wait_for_result


class AddPlayerButton(DefaultBetButton):
    _output_price = 'xpath=.//*[@data-crlat="value"]'


class MarketsDropDown(ComponentBase):
    _name = 'xpath=.//*[@class="menu-title"]'

    @property
    def name(self):
        return self._get_webelement_text(self._name, context=self._we)


class PlayerCard(ComponentBase):
    _item = 'xpath=.//*[contains(@class, "menu-item")]'
    _list_item_type = MarketsDropDown
    _add_player_button = 'xpath=.//*[@data-crlat="addPlayerBtn"]'
    _back_button = 'xpath=.//*[@class="btn-back"]'
    _player_name = 'xpath=.//*[@class="title-text"]'
    _team_name = 'xpath=.//*[@class="player-team"]'
    _selected_market = 'xpath=.//*[@class="label"] | .//*[@class="players-list-header"] | .//*[contains(@class, "players-list-header")]'
    _stat_value = 'xpath=.//*[@class="subtitle"]/span[@class="value"] | .//*[@class="subtitle"]/span[contains(@class, "value")]'
    _player_list = 'xpath=.//*[@class="player-label"]'
    _remove_selection = 'xpath=.//*[@class="remove-button"]'
    _market_drop_down = 'xpath=.//*[@class="dropdown-header"]'
    _update_player_button = 'xpath=.//*[@class="btn-odds updatePlayer"]'
    _player_odds = 'xpath=.// *[ @class ="odds-label"] // *[@ data-crlat="value"]'
    _minus_button = 'xpath=.//*[contains(@class,"round-button minus")]'
    _plus_button = 'xpath=.//*[contains(@class,"round-button plus")]'
    _step_value = 'xpath=.//div[@class="right-buttons"]//*[contains(@class,"value")]'
    _plus_button_disabled = 'xpath=.//*[@class="round-button plus disabled"]'
    _minus_button_disabled = 'xpath=.//*[@class="round-button minus disabled"]'

    @property
    def plus_button_is_enabled(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._plus_button_disabled, timeout=1),
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def minus_button_is_enabled(self, expected_result=True, timeout=2):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._minus_button_disabled, timeout=1),
                               expected_result=expected_result,
                               timeout=timeout)

    @property
    def minus_button(self):
        return self._find_element_by_selector(self._minus_button, context=self._we)

    @property
    def plus_button(self):
        return self._find_element_by_selector(self._plus_button, context=self._we)

    @property
    def step_value(self):
        return self._get_webelement_text(self._step_value, context=self._we)

    @property
    def back_button(self):
        return self._find_element_by_selector(self._back_button, context=self._we)

    @property
    def player_name(self):
        return self._find_element_by_selector(self._player_name, context=self._we)

    @property
    def team_name(self):
        return self._find_element_by_selector(self._team_name, context=self._we)

    @property
    def selected_market(self):
        return self._find_element_by_selector(self._selected_market, context=self._we)

    @property
    def stat_value(self):
        return self._find_element_by_selector(self._stat_value, context=self._we)

    @property
    def player_list(self):
        return self._find_elements_by_selector(self._player_list, context=self._we)

    @property
    def add_player_button(self):
        return AddPlayerButton(selector=self._add_player_button, context=self._we)

    @property
    def remove_selection(self):
        return self._find_element_by_selector(self._remove_selection, context=self._we)

    @property
    def market_drop_down(self):
        return self._find_element_by_selector(self._market_drop_down, context=self._we)

    @property
    def update_player_button(self):
        return self._find_element_by_selector(self._update_player_button, context=self._we)

    @property
    def player_odds(self):
        return self._find_element_by_selector(self._player_odds, context=self._we)
