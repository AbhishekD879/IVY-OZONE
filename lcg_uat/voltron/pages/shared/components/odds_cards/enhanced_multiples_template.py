from collections import OrderedDict

from voltron.pages.shared.components.odds_cards.base_odds_card_template import BaseOddsCardTemplate
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton


class EnhancedMultiplesTemplate(BaseOddsCardTemplate):
    _event_time = 'xpath=.//*[@data-crlat="eventDay" or @data-crlat="eventTime"]'

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._whole_event_name, context=self._we, timeout=0)

    @property
    def bet_button(self):
        return BetButton(self._bet_button, context=self._we, timeout=0)

    def get_available_prices(self):
        return self.get_active_prices()

    def get_active_prices(self):
        active_prices = OrderedDict()
        if self.event_name is not None and (not self.bet_button or self.bet_button.is_enabled(timeout=0.5)):
            active_prices[self.event_name] = self.bet_button
        return active_prices

    def get_all_prices(self):
        return self.get_active_prices()

    def get_selected_output_prices(self):
        selected_prices = OrderedDict()
        if self.event_name is not None and self.bet_button.is_selected():
            selected_prices.update({self.event_name: self.bet_button})
        return selected_prices

    def is_half_time_event(self):
        return False

    def has_markets(self):
        return False

    @property
    def has_stream(self):
        return False

    def has_set_number(self):  # for tennis in-play events
        return False

    @property
    def is_live_now_event(self):
        return False

    def get_markets_count(self):
        return 0
