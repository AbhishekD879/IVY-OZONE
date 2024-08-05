from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenu, TabsMenuItem
from voltron.utils.waiters import wait_for_result


class PlayerItem(ComponentBase):
    _item_name = 'xpath=.//*[@data-crlat="playerName"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._item_name)


class PlayersList(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="playerCard"]'
    _list_item_type = PlayerItem

    _player_name = 'xpath=.//*[@data-crlat="playerName"]'
    _stats_label = 'xpath=.//*[@class="stats"]'
    _team_name = 'xpath=.//*[@class="team-name"]'

    @property
    def player_name(self):
        return self._find_element_by_selector(self._player_name, context=self._we)

    @property
    def player_names(self):
        return self._find_elements_by_selector(self._player_name, context=self._we)

    @property
    def stats_label(self):
        return self._find_element_by_selector(self._stats_label, context=self._we)

    @property
    def team_name(self):
        return self._find_element_by_selector(self._team_name, context=self._we)

    @property
    def team_names(self):
        return self._find_elements_by_selector(self._team_name, context=self._we)


class SwitchersMenuItem(TabsMenuItem):
    _item_name = 'xpath=.//*[@data-crlat="switcher.name"]'

    def is_selected(self, expected_result=True, timeout=5, poll_interval=0.5, name=None):
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        return wait_for_result(lambda: 'active' in self.get_attribute('class'),
                               expected_result=expected_result,
                               timeout=timeout,
                               poll_interval=poll_interval,
                               name=name)


class SwitchersMenu(TabsMenu):
    _item = 'xpath=.//*[@data-crlat="buttonSwitch"]'
    _list_item_type = SwitchersMenuItem


class PlayersOverlay(ComponentBase):
    _player_list = 'xpath=.//*[@data-crlat="playerList"]'
    _switchers_menu = 'xpath=.//*[@data-crlat="switchers"]'
    _back_button = 'xpath=.//*[@class="btn-back"]'
    _title = 'xpath=.//*[@class="title-text"]'
    _sub_title = 'xpath=.//*[@class="subtitle"] | .//*[contains(@class,"players-list-header")]'
    _market_drop_down = 'xpath=.//*[@class="dropdown-header"]'
    _dropdown_menu = 'xpath=.//*[@class="dropdown-menu"]'

    @property
    def back_button(self):
        return self._find_element_by_selector(self._back_button, context=self._we)

    @property
    def title(self):
        return self._find_element_by_selector(self._title, context=self._we)

    @property
    def sub_title(self):
        return self._find_element_by_selector(self._sub_title, context=self._we)

    @property
    def players_list(self):
        return PlayersList(selector=self._player_list, context=self._we)

    @property
    def switchers(self):
        return SwitchersMenu(selector=self._switchers_menu, context=self._we)

    @property
    def market_dropdown(self):
        return self._find_element_by_selector(selector=self._market_drop_down, context=self._we, timeout=2)

    @property
    def dropdown_menu(self):
        return self._find_element_by_selector(selector=self._dropdown_menu, context=self._we, timeout=2)
