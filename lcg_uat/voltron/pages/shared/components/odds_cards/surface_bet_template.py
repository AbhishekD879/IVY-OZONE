import tests
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.odds_cards.base_odds_card_template import BaseOddsCardTemplate
from voltron.pages.shared.components.primitives.buttons import IconBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.utils.waiters import wait_for_result


class SurfaceBetHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="surfaceBetCard.title"]'
    _icon = 'xpath=.//*[@data-crlat="surfaceBetCard.icon"]'
    _icon_value = 'xpath=.//*[@data-crlat="surfaceBetCard.icon"]/*/*'


    @property
    def title(self):
        title_we = self._find_element_by_selector(selector=self._title, timeout=0.5)
        title = self._get_webelement_text(we=title_we)
        return title if title else title_we.get_attribute('innerHTML').upper()

    def is_title_truncated(self):
        return self.is_truncated(selector=self._title)

    def has_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._icon, timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def icon(self):
        return IconBase(selector=self._icon, context=self._we)

    @property
    def icontext(self):
        return self._find_element_by_selector(selector=self._icon_value).get_attribute('xlink:href')


class SurfaceBetOldPrice(TextBase):

    @property
    def text(self):
        return f'{self.label} {self.value}'

    @property
    def is_strike_through(self):
        price = ComponentBase(selector=self._value, context=self._we, timeout=1)
        return 'line-through' in price.css_property_value('text-decoration').strip(' ').split(' ') \
            if tests.settings.brand == 'bma' else self.css_property_value('text-decoration').strip(' ').split(' ')


class SurfaceBetTemplate(BaseOddsCardTemplate):
    _header = 'xpath=.//*[@data-crlat="surfaceBetCard.header"]'
    _header_type = SurfaceBetHeader
    _content = 'xpath=.//*[@data-crlat="surfaceBetCard.content"]'
    _content_header = 'xpath=.//*[@data-crlat="surfaceBetCard.contentHeader"]'
    _old_price = 'xpath=.//*[@data-crlat="surfaceBetCard.oldPrice"]'

    @property
    def header(self):
        return self._header_type(selector=self._header, context=self._we, timeout=1)

    @property
    def name(self):
        return self.header.title

    @property
    def content(self):
        return self._get_webelement_text(selector=self._content)

    @property
    def content_header(self):
        return self._find_element_by_selector(selector=self._content_header).text

    def is_content_truncated(self):
        return self.is_truncated(selector=self._content)

    def has_bet_button(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._bet_button, context=self._we,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Bet button shown status to be {expected_result}')

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)

    def is_old_price_present(self, expected_result=True, timeout=5):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._old_price, timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Old price shown status to be {expected_result}')

    @property
    def old_price(self):
        return SurfaceBetOldPrice(selector=self._old_price, context=self._we, timeout=2)

    @property
    def event_name(self):
        raise NotImplementedError(f'{__name__} not used for {self.__class__}')

    def get_all_prices(self):
        raise NotImplementedError(f'{__name__} not used for {self.__class__}')

    def get_markets_count(self):
        raise NotImplementedError(f'{__name__} not used for {self.__class__}')

    def get_active_prices(self):
        raise NotImplementedError(f'{__name__} not used for {self.__class__}')

    def get_selected_output_prices(self):
        raise NotImplementedError(f'{__name__} not used for {self.__class__}')

    def get_available_prices(self):
        raise NotImplementedError(f'{__name__} not used for {self.__class__}')
