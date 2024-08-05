from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.inputs import InputBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


class BetBuilderButtonBase(ButtonBase, TextBase):

    def click(self, scroll_to=True):
        self.scroll_to_we() if scroll_to else None
        self._logger.debug(
            f'*** User has clicked "{self._we.text}" button. Call "{self.__class__.__name__}.click" method'
        )
        click(self._we)


class BetBuilderSelection(ComponentBase):
    _leg_number = 'xpath=.//*[@class="label"]'
    _name = 'xpath=.//*[@class="value"]'
    _remove = 'xpath=.//*[@class="action remove"]'

    @property
    def leg_number(self):
        return self._get_webelement_text(selector=self._leg_number, context=self._we)

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)

    @property
    def remove(self):
        return ButtonBase(selector=self._remove, context=self._we)


class BetBuilderSelections(ComponentBase):
    _item = 'xpath=.//*[@class="dash-item"]'
    _list_item_type = BetBuilderSelection


class BetBuilderSummary(ComponentBase):
    _description = 'xpath=.//*[@data-crlat="descriptionTitle"]'
    _add_to_betslip = 'xpath=.//*[@data-crlat="addToBetslip"]'
    _clear_selection = 'xpath=.//*[@data-crlat="clearSelections"]'
    _no_lines = 'xpath=.//*[@data-crlat="description.infoBlock"]'
    _input = 'xpath=.//*[@data-crlat="enterAmount"]'
    _open = 'xpath=.//*[@class="open"]'

    @property
    def open(self):
        return self._find_element_by_selector(selector=self._open, context=self._we)

    @property
    def input(self):
        return InputBase(selector=self._input, context=self._we)

    @property
    def no_lines(self):
        return TextBase(selector=self._no_lines, context=self._we)

    @property
    def add_to_betslip_button(self):
        return BetBuilderButtonBase(selector=self._add_to_betslip, context=self._we)

    @property
    def clear_selection_button(self):
        return ButtonBase(selector=self._clear_selection, context=self._we)

    @property
    def description_title(self):
        return self._get_webelement_text(selector=self._description, timeout=2)


class UKToteBetBuilder(ComponentBase):
    _summary = 'xpath=.//*[@data-crlat="summary"]'
    _summary_type = BetBuilderSummary
    _selections = 'xpath=.//*[@class="selections"]'
    _selections_type = BetBuilderSelections

    def is_displayed(self, expected_result=True, timeout=1, poll_interval=0.5, name=None, scroll_to=True,
                     bypass_exceptions=(NoSuchElementException, StaleElementReferenceException)):
        if not name:
            name = f'"{self.__class__.__name__}" displayed status is: {expected_result}'
        result = wait_for_result(lambda: 'visible' in self.get_attribute('class'),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 bypass_exceptions=bypass_exceptions,
                                 name=name)
        return result

    @property
    def summary(self):
        return self._summary_type(selector=self._summary, context=self._we)

    def is_present(self, timeout=5, expected_result=True):
        return wait_for_result(lambda: 'visible' in self.get_attribute('class').strip(' ').split(' ') and
                                       self.is_displayed(expected_result=expected_result, timeout=0),
                               timeout=timeout,
                               expected_result=expected_result,
                               name='Bet builder shown status to be "%s"' % expected_result)

    @property
    def selections(self):
        return self._selections_type(selector=self._selections, context=self._we)
