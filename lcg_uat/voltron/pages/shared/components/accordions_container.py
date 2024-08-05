from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import IconBase
from selenium.common.exceptions import StaleElementReferenceException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class AccordionHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="containerHeader"]'
    _cash_out_mark = 'xpath=.//*[@data-crlat="labelCashout"]'

    @property
    def text(self):
        title = self._find_element_by_selector(self._title, timeout=1)
        if title is not None:
            text = self._get_webelement_text(we=title)
        else:
            text = self._get_webelement_text(we=self._we, timeout=2)
        return text

    @property
    def title_text(self):
        wait_for_result(lambda: self.text,
                        name='Header text is not empty',
                        timeout=5,bypass_exceptions=VoltronException)
        return self.text

    @property
    def cash_out_label(self):
        return IconBase(selector=self._cash_out_mark, context=self._we)

    def has_cash_out_mark(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._cash_out_mark,
                                                   timeout=0) is not None,
            name=f'Cash out mark status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class AccordionContent(ComponentBase):

    @property
    def text(self):
        return self._get_webelement_text(we=self._we, timeout=2)


class Accordion(ComponentBase):
    _header = 'xpath=.//*[@data-crlat="containerHeader"]'
    _header_type = AccordionHeader
    _content = 'xpath=.//*[@data-crlat="containerContent"]'
    _content_type = AccordionContent
    _chevron_arrow = 'xpath=.//*[@data-crlat="chevronArrow"] | .//*[contains(@class,"chevron-svg chevron-down")] | .//*[contains(@class,"chevron-svg")]'

    def is_expanded(self, timeout=1, expected_result=True, bypass_exceptions=(StaleElementReferenceException, )):
        result = wait_for_result(lambda: 'is-expanded' in self.get_attribute('class'),
                                 name=f'"{self.__class__.__name__}" Accordion to expand',
                                 expected_result=expected_result,
                                 bypass_exceptions=bypass_exceptions,
                                 timeout=timeout)
        result = result if result else False
        self._logger.debug(f'*** "{self.__class__.__name__}" Accordion expanded status is "{result}"')
        return result

    @property
    def section_header(self):
        return self._header_type(selector=self._header, context=self._we, timeout=4)

    @property
    def name(self):
        return self.section_header.text

    def expand(self):
        if self.is_expanded():
            title_text = self.name
            self._logger.warning(f'*** Bypassing accordion expand, since "{title_text}" already expanded')
        else:
            title_text = self.name
            self._logger.debug(f'*** Expanding "{title_text}"')

            self.section_header.click()
            wait_for_result(lambda: self.is_expanded(timeout=0),
                            name=f'"{self.__class__.__name__}" section to expand',
                            timeout=3)

    def collapse(self):
        title_text = self.name
        if not self.is_expanded():
            self._logger.warning(f'*** Bypassing accordion collapse, since "{title_text}" already collapsed')
        else:
            self._logger.debug(f'*** Collapsing "{title_text}"')
            self.section_header.click()
            wait_for_result(lambda: self.is_expanded(expected_result=False, timeout=0),
                            expected_result=False,
                            name=f'"{self.__class__.__name__}" section to collapse',
                            timeout=3)

    @property
    def content(self):
        return self._content_type(selector=self._content, context=self._we)

    # Present only on desktop
    @property
    def chevron_arrow(self):
        return ComponentBase(self._chevron_arrow, context=self._we, timeout=1)

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


class AccordionsContainer(ComponentBase):
    _container_items = 'xpath=.//section'
    _container_item_type = Accordion
