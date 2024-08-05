from collections import OrderedDict

from voltron.pages.shared.components.odds_cards.sport_template import SportTemplate
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.components.right_column_widgets.in_play_widget import InPlayCardBody


class LiveStreamWidgetEventCardBody(InPlayCardBody, SportTemplate):
    _name = 'xpath=.//*[@data-crlat="lsName"]'
    _match_scores = 'xpath=.//*[@data-crlat="lsScore"] | .//*[@class="ls-score"]'
    _bet_buttons_section = 'xpath=.//*[@class="ls-odds-btn"]'
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _point_scores = 'xpath=.//*[@data-crlat="lsScore"]/span[2]'
    _set_scores = 'xpath=.//*[@data-crlat="lsScore"]/span[1]'
    _live_now_label = 'xpath=.//*[@class="ls-status"]'

    @property
    def set_score_element(self):
        return self._find_element_by_selector(selector=self._set_scores, context=self._we,
                                              timeout=2)

    @property
    def point_score_element(self):
        return self._find_element_by_selector(selector=self._point_scores, context=self._we,
                                              timeout=2)

    @property
    def live_now_label(self):
        return self._get_webelement_text(selector=self._live_now_label, timeout=1)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=1)

    def event_name(self):
        return self._find_element_by_selector(selector=self._name, timeout=1)

    @property
    def match_scores(self):
        return TextBase(selector=self._match_scores, context=self._we).name

    def match_score_element(self):
        return self._find_element_by_selector(selector=self._match_scores, timeout=1)

    @property
    def point_score(self):
        return TextBase(selector=self._point_scores, context=self._we).name

    @property
    def left_score(self):
        return self.match_scores[0]

    @property
    def right_score(self):
        return self.match_scores[-1]

    def get_active_prices(self) -> OrderedDict:
        active_prices = OrderedDict()
        first_bet_button = self.first_player_bet_button
        draw_bet_button = self.draw_bet_button
        second_bet_button = self.second_player_bet_button
        if first_bet_button is not None and first_bet_button.is_enabled(timeout=0.5):
            active_prices[first_bet_button.name.split()[0]] = first_bet_button
        if draw_bet_button is not None and draw_bet_button.is_enabled(timeout=0.5):
            active_prices[draw_bet_button.name.split()[0]] = draw_bet_button
        if second_bet_button is not None and second_bet_button.is_enabled(timeout=0.5):
            active_prices[second_bet_button.name.split()[0]] = second_bet_button
        return active_prices

    def _get_bet_button_divs(self):
        all_bet_buttons = self._find_elements_by_selector(selector=self._bet_buttons_section, context=self._we,
                                                          timeout=2)
        if len(all_bet_buttons) == 0:
            self._logger.warning('*** No Place Bet button found team/player')
            return None
        else:
            return all_bet_buttons
