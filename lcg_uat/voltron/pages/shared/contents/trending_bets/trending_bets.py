from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class TrendingBetCard(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="trending-bet-selection"]'
    _market_name = 'xpath=.//*[@data-crlat="trending-bet-market"]'
    _event_name = 'xpath=.//*[@data-crlat="trending-bet-event"]'
    _backed = 'xpath=.//*[@data-crlat="trending-bet-backed"]'
    _odd = 'xpath=.//*[@data-crlat="price-odd-container"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, timeout=5)

    @property
    def market_name(self):
        return self._get_webelement_text(selector=self._market_name, timeout=5)

    @property
    def event_name(self):
        return self._get_webelement_text(selector=self._event_name, timeout=5)

    @property
    def backed_text(self):
        return self._get_webelement_text(selector=self._backed, timeout=5)

    @property
    def odd(self):
        return ButtonBase(selector=self._odd, timeout=5, context=self._we)


class TrendingBets(ComponentBase):
    _header_title = 'xpath=.//*[@data-crlat="headerTitle.centerMessage"]'
    _chevron = 'xpath=.//*[@data-crlat="chevronArrow"]'
    _item = 'xpath=.//*[@data-crlat="trending-bet-card"]'
    _list_item_type = TrendingBetCard

    @property
    def header_title(self):
        return self._get_webelement_text(selector=self._header_title, timeout=10)

    @property
    def chevron_arrow(self):
        return ComponentBase(self._chevron, context=self._we, timeout=1)

    def is_chevron_up(self, expected_result=True, timeout=2):
        result = wait_for_result(lambda: 'chevron-up' in self.chevron_arrow.get_attribute('class'),
                                 expected_result=expected_result,
                                 name='Chevron arrow to point to the top',
                                 timeout=timeout)
        return result

    def is_chevron_down(self, expected_result=True, timeout=2):
        result = wait_for_result(lambda: 'chevron-down' in self.chevron_arrow.get_attribute('class'),
                                 expected_result=expected_result,
                                 name='Chevron arrow to point to the bottom',
                                 timeout=timeout)
        return result
