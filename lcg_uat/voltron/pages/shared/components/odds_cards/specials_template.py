import re
from voltron.pages.shared.components.odds_cards.outright_template import OutrightTemplate
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton


class SpecialsTemplate(OutrightTemplate):
    _event_name = 'xpath=.//*[@data-crlat="oddsNames"]'
    _bet_button = 'xpath=.//*[@data-crlat="oddsPrice"]'
    _event_time = 'xpath=.//*[@class="odds-left"]/span'
    _was_price = 'xpath=.//*[@class="was-price"]'

    @property
    def event_name(self):
        event_name = self._get_webelement_text(selector=self._event_name)
        return re.sub('.([(]Was \d/\d[)])', "", event_name)

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)

    @property
    def event_time(self):
        return self._get_webelement_text(selector=self._event_time)

    @property
    def was_price(self):
        return self._get_webelement_text(selector=self._was_price)
