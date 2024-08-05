from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.right_column_widgets.offers_widget_section import OffersWidgetSection
from voltron.pages.shared.components.right_column_widgets.offers_widget_section import OffersWidgetSectionItem
from voltron.pages.shared.components.right_column_widgets.offers_widget_section import OffersWidgetSectionItemSlide
from voltron.utils.waiters import wait_for_result


class CoralOffersWidgetSectionItem(OffersWidgetSectionItem, OffersWidgetSectionItemSlide):
    _inner_section = 'xpath=.//*[@data-crlat="accordion"]'

    @property
    def _section(self):
        return self._find_element_by_selector(selector=self._inner_section, context=self._we, timeout=2)

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException, )):
        result = wait_for_result(lambda: 'is-expanded' in self._section.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'"{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result


class CoralOffersWidgetSection(OffersWidgetSection):
    _list_item_type = CoralOffersWidgetSectionItem
    _inner_section = 'xpath=.//*[@data-crlat="accordion"]'

    @property
    def _section(self):
        return self._find_element_by_selector(selector=self._inner_section, context=self._we, timeout=2)

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException,)):
        result = wait_for_result(lambda: 'is-expanded' in self._section.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'"{self.__class__.__name__}" Group expanded status is "{result}"')
        return result
