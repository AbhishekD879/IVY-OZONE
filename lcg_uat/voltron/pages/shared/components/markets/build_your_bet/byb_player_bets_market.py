from collections import namedtuple

from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.selects import SelectBase, BYBSelectBase
from voltron.pages.shared.components.markets.market_section_base import MarketSection
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.waiters import wait_for_result


class TeamStatsIncrement(ComponentBase):
    _decrease = 'xpath=.//*[@class="alignment1"]/preceding-sibling::button[@class="alignment"]'
    _score = 'xpath=.//*[@class="alignment1"]'
    _increase = 'xpath=.//*[@class="alignment1"]/following-sibling::button[@class="alignment"]'

    @property
    def selected_item(self):
        select_score = self._find_element_by_selector(selector=self._score, timeout=5, context=self._we)
        return select_score.get_attribute('innerText')

    @property
    def stat_value_decrease(self):
        return ButtonBase(selector=self._decrease, timeout=5, context=self._we)

    @property
    def stat_value_increase(self):
        return ButtonBase(selector=self._increase, timeout=5, context=self._we)


class PlayerBetEventGroup(ComponentBase):
    _item = 'xpath=.//*[@class="byb-player-name"]'
    _show_stats = 'xpath=.//*[@class="byb-stats"]'
    _team_stat_values = 'xpath=.//*[@class="btn-group1"]'
    _add_to_betslip_btn = 'xpath=.//*[@id="add-to-bb"]'

    @property
    def add_to_betslip_button(self):
        return ButtonBase(selector=self._add_to_betslip_btn, context=self._we)

    @property
    def team_stat_values(self):
        return TeamStatsIncrement(self._team_stat_values, context=self._we)

    @property
    def show_stats_link(self):
        return ButtonBase(selector=self._show_stats, context=self._we)

    @property
    def name(self):
        result = wait_for_result(lambda: self._get_webelement_text(selector=self._item),
                                 name="Tab to have visible name",
                                 timeout=5)
        return result if result else ''


class PlayersBetList(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"outer-rectangle")]/accordion'
    _list_item_type = PlayerBetEventGroup

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException,)):
        we = self._find_element_by_selector(selector=self._item, timeout=timeout)
        result = wait_for_result(lambda: 'is-expanded' in we.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'"{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result


class BYBPlayerBetsMarket(MarketSection):
    _select_player_label = 'xpath=.//*[@data-crlat="playerBets.selectPlayerText"]'
    _select_player_drop_down = 'xpath=.//*[@data-crlat="playerBets.selectPlayerSelect"]'
    _select_statistic_label = 'xpath=.//*[@data-crlat="playerBets.selectStatisticText"]'
    _select_statistic_drop_down = 'xpath=.//*[@data-crlat="playerBets.selectStatistic"]'
    _select_stat_value_drop_down = 'xpath=.//*[@data-crlat="playerBets.selectStatistic.value"]'
    _add_to_bet_button = 'xpath=.//*[@id="add-to-bb"]'
    _fade_out_overlay = True
    _verify_spinner = True
    _display_players = 'xpath=.//*[contains(@class,"display-players")]'
    _players_list_type = PlayersBetList
    _show_more = 'xpath=.//*[@class="byb-show"]'

    @property
    def display_players(self):
        return self._players_list_type(self._display_players, context=self._we)

    def has_show_more_players_button(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._show_more, timeout=2) is not None,
            name=f'"Show More Leagues" button in "{self.__class__.__name__}" shown status to be "{expected_result}"',
            timeout=timeout,
            expected_result=expected_result)

    @property
    def show_more_players_button(self):
        return ButtonBase(selector=self._show_more, context=self._we)

    def has_select_player_label(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._select_player_label,
                                                                      timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Select Player label status to be "{expected_result}"')

    def has_select_player_drop_down(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._select_player_drop_down,
                                                                      timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Select Player drop down status to be "{expected_result}"')

    def has_select_statistic_label(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._select_statistic_label,
                                                                      timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Select Statistic Label status to be "{expected_result}"')

    def has_select_statistic_drop_down(self, expected_result=True, timeout=10):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._select_statistic_drop_down,
                                                                      timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Select Statistic drop down status to be "{expected_result}"')

    def has_select_stat_value_drop_down(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._select_stat_value_drop_down,
                                                                      timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Select Stat Value drop down status to be "{expected_result}"')

    def has_add_to_bet_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._add_to_bet_button,
                                                                      timeout=0) is not None,
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Add to bet Button status to be "{expected_result}"')

    @property
    def add_to_bet_button(self):
        return ButtonBase(selector=self._add_to_bet_button, context=self._we)

    @property
    def select_statistic_value_drop_down(self):
        try:
            element = self._find_element_by_selector(selector=self._select_stat_value_drop_down, timeout=2)
            wait_for_result(
                lambda: self._find_elements_by_selector(selector='xpath=.//option', context=element, timeout=0),
                name='Statistic value dropdown options to show up',
                timeout=1)
            return BYBSelectBase(self._select_stat_value_drop_down, context=self._we)
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself(timeout=3)
            return SelectBase(self._select_stat_value_drop_down, context=self._we, timeout=5)

    @property
    def select_statistic_label(self):
        return self._get_webelement_text(selector=self._select_statistic_label, timeout=2)

    @property
    def select_statistic_drop_down(self):
        try:
            element = self._find_element_by_selector(selector=self._select_statistic_drop_down, timeout=0)
            wait_for_result(
                lambda: element != self._find_element_by_selector(selector=self._select_statistic_drop_down, timeout=0),
                name='Statistic dropdown to refresh',
                timeout=1)
            return BYBSelectBase(self._select_statistic_drop_down, context=self._we)
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself(timeout=3)
            return SelectBase(self._select_statistic_drop_down, context=self._we, timeout=5)

    @property
    def select_player_drop_down(self):
        try:
            element = self._find_element_by_selector(selector=self._select_player_drop_down, timeout=0)
            wait_for_result(
                lambda: element != self._find_element_by_selector(selector=self._select_player_drop_down, timeout=0),
                name='Player dropdown to refresh',
                timeout=1)
            return BYBSelectBase(self._select_player_drop_down, context=self._we)
        except StaleElementReferenceException:
            self._logger.debug(f'*** Overriding StaleElementReferenceException in {self.__class__.__name__}')
            self._we = self._find_myself(timeout=3)
            return SelectBase(self._select_player_drop_down, context=self._we, timeout=5)

    @property
    def select_player_label(self):
        return self._get_webelement_text(selector=self._select_player_label, timeout=2)

    def get_player_bet_selection(self, player_name=None, player_statistic=None, player_value=None):
        self.select_player_drop_down.value = player_name if player_name else self.select_player_drop_down.selected_item
        self.select_statistic_drop_down.value = player_statistic if player_statistic else self.select_statistic_drop_down.selected_item

        self.select_statistic_value_drop_down.value = player_value if player_value else \
            self.select_statistic_value_drop_down.options[-1].text
        promotion_parameters = namedtuple("player_bet_info", ["player_name", "player_statistic", "statistic_value"])
        player_bet_params = promotion_parameters(self.select_player_drop_down.selected_item,
                                                 self.select_statistic_drop_down.selected_item,
                                                 self.select_statistic_value_drop_down.selected_item)
        return player_bet_params

    def set_player_bet_selection(self, **kwargs):
        self.select_player_drop_down.value = kwargs.get('player_name',
                                                        self.select_player_drop_down.available_options[
                                                            kwargs['player_index'] if kwargs.get('player_index') else 1
                                                        ])
        self.select_statistic_drop_down.value = kwargs.get('statistic_name',
                                                           self.select_statistic_drop_down.available_options[
                                                               kwargs['statistic_index'] if kwargs.get(
                                                                   'statistic_index') else 1
                                                           ])
        self.select_statistic_value_drop_down.value = kwargs.get('statistic_value_name',
                                                                 self.select_statistic_value_drop_down.available_options[
                                                                     kwargs['statistic_value_index'] if kwargs.get(
                                                                         'statistic_value_index') else 1
                                                                 ])
        return self.get_player_bet_selection()


class PlayerStatsDialog(Dialog):
    _player_name = 'xpath=.//*[@class="title-text"]'
    _player_team = 'xpath=.//*[@class="player-team"]'
    _player_stats_title = 'xpath=.//*[@class="displaySub"]'
    _back_button = 'xpath=.//*[@class="btn-back"]'

    @property
    def back_button(self):
        return ButtonBase(selector=self._back_button, context=self._we, timeout=3)

    @property
    def player_name(self):
        return self._find_element_by_selector(selector=self._player_name)

    @property
    def player_team(self):
        return self._find_element_by_selector(selector=self._player_team)

    @property
    def player_stats_title(self):
        return self._find_element_by_selector(selector=self._player_stats_title)
