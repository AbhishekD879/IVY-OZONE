from collections import OrderedDict
from voltron.pages.shared.components.odds_cards.base_odds_card_template import BaseOddsCardTemplate
from voltron.utils.waiters import wait_for_result


class OutrightTemplate(BaseOddsCardTemplate):
    _event_name = 'xpath=.//*[@data-crlat="couponName"]'
    _live_now_label = 'xpath=.//*[@data-crlat="oddsLive" or @data-crlat="liveLabel"]'
    _event_id = 'xpath=.//*[@data-crlat="eventId"]'
    _stream_icon = 'xpath=.//*[@data-crlat="streamIcon" or @data-crlat="oddsIconStream"]'
    _markets_count = 'xpath=.//*[@data-crlat="marketsCount"]'

    @property
    def event_id(self):
        return self.get_attribute('data-eventid')

    @property
    def event_date(self):
        return 'Outright event does not have date'

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._event_name, timeout=0)

    @property
    def has_show_all_button(self):
        return False

    @property
    def has_set_number(self):
        return False

    @property
    def is_half_time_event(self):
        return False

    def get_all_prices(self):
        return OrderedDict()

    def has_markets(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._markets_count, timeout=0) is not None,
            name=f'Markets presence status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def get_active_prices(self):
        return OrderedDict()

    def get_markets_count(self):
        return 0

    def get_available_prices(self):
        return OrderedDict()

    def get_selected_output_prices(self):
        return OrderedDict()
