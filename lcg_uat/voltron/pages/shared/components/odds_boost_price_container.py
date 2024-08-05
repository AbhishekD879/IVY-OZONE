from voltron.pages.shared.components.base import ComponentBase


class OddsBoostPriceContainer(ComponentBase):
    _odds_boost_price_component = 'xpath=.//*[@data-crlat="item"]'

    @property
    def price_value(self):
        value = ''
        price_components = self._find_elements_by_selector(selector=self._odds_boost_price_component)
        for component in price_components:
            if self._find_element_by_selector(selector='xpath=.//*', context=component, timeout=1):
                value += self._get_webelement_text(selector='xpath=.//li[1]', context=component)
            else:
                value += self._get_webelement_text(we=component)
        return value
