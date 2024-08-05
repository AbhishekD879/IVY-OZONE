import re
from collections import OrderedDict

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.odds_cards.base_odds_card_template import BaseOddsCardTemplate
from voltron.pages.shared.components.score_table import ScoreTable
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.contents.base_contents.common_base_components.promotion_icons import PromotionIcons
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


class SportTemplate(BaseOddsCardTemplate):
    _bet_button = 'xpath=.//button[not(contains(@class, "ng-hide"))]'

    _first_player_name = 'xpath=.//*[@data-crlat="EventFirstName"]'
    _second_player_name = 'xpath=.//*[@data-crlat="EventSecondName"]'

    _bet_buttons_section = 'xpath=.//*[@data-crlat="oddsBtnContent"]'
    _one_button_section = 'xpath=.//*[@data-crlat="oddsBtnWrapper"]'

    _single_event_name = 'xpath=.//*[@data-crlat="singleEventName" or @data-crlat="oddsNames"]'
    _players = 'xpath=.//*[@data-crlat="oddsNames"]'

    _markets_count = 'xpath=.//*[@data-crlat="marketsCount"]'
    _live_now_label = 'xpath=.//*[@data-crlat="liveLabel"]'
    _half_time_label = 'xpath=.//span[@event-clock="oddsCard.event.clock"]'
    _set_number = 'xpath=.//*[@data-crlat="oddsCardLabel"]'

    _promotion_icons = 'xpath=.//*[@data-crlat="promotionIcons"]'
    _byb_icon = 'xpath=.//*[@data-crlat="yourcallIcon"]'

    _serving_ball_icon = 'xpath=.//*[@data-crlat="oddsNames"]//*[@data-crlat="bIcon"]'

    _score_table = 'xpath=.//*[@data-crlat="scoreTable"]'

    _goals_count = 'xpath=.//*[@class="odds-next-score"] | .//*[@class="sport-card-next-score"]'
    _chevron = 'xpath=.//*[@data-crlat="oddsHeader"]'

    @property
    def event_name(self):
        first = self.first_player
        second = self.second_player
        if first != '' and second != '':
            return f'{first} {self.draw_label} {second}'
        elif self._get_single_event_name() != '':
            return self._get_single_event_name()
        else:
            return ''

    def _get_single_event_name(self):
        return self._get_webelement_text(selector=self._single_event_name, timeout=1)

    @property
    def event_name_we(self):
        return ComponentBase(selector=self._players, context=self._we)

    def click(self):
        return self.event_name_we.click()

    @property
    def first_player(self):
        return normalize_name(self._get_webelement_text(selector=self._first_player_name, timeout=1))

    def event_first_player(self):
        return self._find_element_by_selector(selector=self._first_player_name, timeout=1)

    @property
    def draw_label(self):
        return 'v'

    @property
    def second_player(self):
        return normalize_name(self._get_webelement_text(selector=self._second_player_name, timeout=1))

    def event_second_player(self):
        return self._find_element_by_selector(selector=self._second_player_name, timeout=1)

    @property
    def score_table(self):
        return ScoreTable(selector=self._score_table, context=self._we, timeout=2)

    def has_serving_ball_icon(self, expected_result=True, timeout=1):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._serving_ball_icon,
                                                   timeout=0) is not None,
            name=f'Serving ball status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_outcomes(self, expected_result=True, timeout=0.5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._bet_buttons_section,
                                                   timeout=0) is not None,
            name=f'Outcomes displayed status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def _get_bet_button_divs(self):
        all_bet_buttons_div_we = self._find_element_by_selector(self._bet_buttons_section, timeout=2)
        button_divs = self._find_elements_by_selector(self._one_button_section, context=all_bet_buttons_div_we,
                                                      timeout=2)
        if len(button_divs) == 0:
            self._logger.warning('*** No Place Bet button found team/player')
            return None
        else:
            return button_divs

    @property
    def first_player_bet_button(self):
        button_divs = self._get_bet_button_divs()
        if button_divs is None:
            self._logger.warning('*** No Place Bet button found for first team/player')
            return None
        if len(button_divs) > 0:
            button_we = self._find_element_by_selector(selector=self._bet_button, context=button_divs[0], timeout=1)
            if button_we:
                return BetButton(web_element=button_we)
            else:
                return None
        else:
            raise VoltronException(message='No active selections found in event')

    @property
    def draw_bet_button(self):
        button_divs = self._get_bet_button_divs()
        if button_divs is None:
            self._logger.warning('*** No Place Bet button found for Draw')
            return None
        if len(button_divs) > 2:
            button_we = self._find_element_by_selector(selector=self._bet_button, context=button_divs[1], timeout=1)
            if button_we:
                return BetButton(web_element=button_we)
            else:
                return None

    @property
    def second_player_bet_button(self):
        button_divs = self._get_bet_button_divs()
        if button_divs is None:
            self._logger.warning('*** No Place Bet button found for second team/player')
            return None
        button_we = self._find_element_by_selector(selector=self._bet_button, context=button_divs[-1], timeout=1)
        if button_we:
            return BetButton(web_element=button_we)
        else:
            return None

    def get_available_prices(self) -> OrderedDict:
        if self.first_player and self.second_player:
            return self.get_active_prices()
        elif self._get_single_event_name():
            return OrderedDict({self._get_single_event_name(): self.first_player_bet_button})

    def get_active_prices(self) -> OrderedDict:
        """
        Get all active selections
        :return: dictionary with active selections
        """
        active_prices = OrderedDict()
        if self.first_player_bet_button is not None and self.first_player_bet_button.is_enabled(timeout=0.5):
            active_prices[self.first_player] = self.first_player_bet_button
        if self.draw_bet_button is not None and self.draw_bet_button.is_enabled(timeout=0.5):
            active_prices['Draw'] = self.draw_bet_button
        if self.second_player_bet_button is not None and self.second_player_bet_button.is_enabled(timeout=0.5):
            active_prices[self.second_player] = self.second_player_bet_button

        return active_prices

    def get_all_prices(self) -> OrderedDict:
        """
        Get all selections, not only active
        :return: dictionary with all selections
        """
        first_player = wait_for_result(lambda: normalize_name(self._get_webelement_text(selector=self._first_player_name, timeout=2)), timeout=1)
        second_player = wait_for_result(lambda: normalize_name(self._get_webelement_text(selector=self._second_player_name, timeout=2)), timeout=1)
        active_prices = (
            (first_player, self.first_player_bet_button),
            ('Draw', self.draw_bet_button),
            (second_player, self.second_player_bet_button)
        )
        active_prices = OrderedDict(active_prices)
        return active_prices

    def get_selected_output_prices(self) -> OrderedDict:
        selected_prices = OrderedDict()
        if self.first_player_bet_button is not None and self.first_player_bet_button.is_selected():
            selected_prices[self.first_player] = self.first_player_bet_button
        elif self.draw_bet_button is not None and self.draw_bet_button.is_selected():
            selected_prices[self.draw_label] = self.draw_bet_button
        elif self.second_player_bet_button is not None and self.second_player_bet_button.is_selected():
            selected_prices[self.second_player] = self.second_player_bet_button
        return selected_prices

    def is_half_time_event(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._half_time_label,
                                                   timeout=0) is not None,
            name=f'Label status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_set_number(self, timeout=1, expected_result=True):  # for tennis in-play events
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._set_number,
                                                   timeout=1) is not None,
            name=f'Label status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def set_number(self):
        return normalize_name(self._get_webelement_text(selector=self._set_number, timeout=1))

    def get_markets_count(self):
        market_string = self.get_markets_count_string()
        if market_string:
            match = re.match(r'\D?([\d]*)', market_string)
            if match is not None:
                return int(match.group(1))
        return 0

    def get_markets_count_string(self):
        market_string = self._get_webelement_text(selector=self._markets_count, timeout=0)
        return market_string

    def has_markets(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._markets_count, timeout=0) is not None,
            name=f'Markets presence status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def more_markets_link(self):
        return LinkBase(selector=self._markets_count, context=self._we)

    @property
    def promotion_icons(self):
        return PromotionIcons(selector=self._promotion_icons, context=self._we)

    def has_watch_live_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._stream_link,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_byb_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._byb_icon,
                                                   timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def goal_number(self):
        return self._find_element_by_selector(selector=self._goals_count, timeout=3)

    @property
    def chevron(self):
        return self._find_element_by_selector(selector=self._chevron, timeout=1)


class AggregateMarket(ComponentBase):
    _bet_button = 'xpath=.//button[not(contains(@class, "ng-hide"))]'
    @property
    def get_bet_buttons(self):
        bet_button_elements = self._find_elements_by_selector(self._bet_button, timeout=2)
        bet_buttons_list = [BetButton(web_element=button) for button in bet_button_elements]
        button_names_with_buttons = OrderedDict()
        for button in bet_buttons_list:
            button_names_with_buttons.update({button.name : button})
        return button_names_with_buttons


class AggregateSportTemplate(SportTemplate):
    _market_type = AggregateMarket
    _market_section = 'xpath=.//*[@class="row"]/div'
    @property
    def get_aggregated_markets_count(self):
        markets = self._find_elements_by_selector(self._market_section, timeout=2)
        if not markets:
            return 0
        return len(markets)
    @property
    def get_market_sections(self):
        markets = self._find_elements_by_selector(self._market_section, timeout=2)
        converted_markets = [self._market_type(web_element=market) for market in markets]
        return converted_markets
