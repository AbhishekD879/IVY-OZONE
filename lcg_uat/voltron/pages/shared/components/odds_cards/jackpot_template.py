from voltron.pages.shared.components.odds_cards.base_odds_card_template import BaseOddsCardTemplate
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton


class JackpotBetButton(BetButton):

    @property
    def outcome_price_text(self):
        return self._get_webelement_text(we=self._we)


class JackpotTemplate(BaseOddsCardTemplate):
    _event_day = 'xpath=.//*[@data-crlat="eventEntity.startTime"]'
    _event_name = 'xpath=.//*[@data-crlat="eventEntity.name"]'
    _bet_buttons_section = 'xpath=.//*[@data-crlat="oddsRight"]'
    _one_button_section = 'xpath=.//*[@data-crlat="oddsBtnContent"]'
    _event_id = 'xpath=.//ancestor::div[contains(@data-crlat, "eventEntity")]'

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._event_name)

    @property
    def outcomes_list(self):
        all_bet_buttons_div_we = self._find_element_by_selector(self._bet_buttons_section, timeout=0)
        return self._find_elements_by_selector(self._one_button_section, context=all_bet_buttons_div_we, timeout=0)

    def _get_bet_button_we_by_id(self, button_id):
        button_div_we = self.outcomes_list[button_id]
        return self._find_element_by_selector(selector=self._bet_button, context=button_div_we, timeout=0)

    @property
    def first_player_bet_button(self):
        button_we = self._get_bet_button_we_by_id(0)
        return JackpotBetButton(web_element=button_we)

    @property
    def draw_bet_button(self):
        button_we = self._get_bet_button_we_by_id(1)
        return JackpotBetButton(web_element=button_we)

    @property
    def second_player_bet_button(self):
        button_we = self._get_bet_button_we_by_id(2)
        return JackpotBetButton(web_element=button_we)

    def get_available_prices(self):
        self.scroll_to_we()
        active_prices = []
        if self.first_player_bet_button is not None:
            active_prices.append(self.first_player_bet_button)
        if self.draw_bet_button is not None:
            active_prices.append(self.draw_bet_button)
        if self.second_player_bet_button is not None:
            active_prices.append(self.second_player_bet_button)

        return active_prices

    def get_all_prices(self):
        raise NotImplementedError(f'{__name__} not used for {self.__class__}')

    def get_markets_count(self):
        raise NotImplementedError(f'{__name__} not used for {self.__class__}')

    def get_active_prices(self):
        raise NotImplementedError(f'{__name__} not used for {self.__class__}')

    def get_selected_output_prices(self):
        raise NotImplementedError(f'{__name__} not used for {self.__class__}')

    @property
    def event_id(self) -> str:
        event = self._find_element_by_selector(selector=self._event_id, timeout=0)
        return event.get_attribute('data-eventid')
