from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.bet_filter.horseracing_bet_filter import HorseRacingBetFilterPage
from voltron.utils.waiters import wait_for_result
from voltron.utils.js_functions import click
from voltron.utils.exceptions.voltron_exception import VoltronException


class LadbrokesBetFinderTextBase(TextBase):

    @property
    def is_bold(self):
        return self.css_property_value('font-weight') == '500'


class LadbrokesHorseRacingBetFilterPage(HorseRacingBetFilterPage):
    _header_message = 'xpath=.//*[@data-crlat="title"]'
    _meetings_drop_down = 'xpath=.//*[@data-crlat="dropDownCont"]'
    _fade_out_overlay = True

    @property
    def header_message(self):
        return LadbrokesBetFinderTextBase(selector=self._header_message)

    @property
    def meetings_drop_down(self):
        return LadbrokesMeetingsDropDown(selector=self._meetings_drop_down, context=self._we)


class MarketSelectorOption(ComponentBase):

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)


class LadbrokesMeetingsDropDown(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="item"]'
    _list_item_type = MarketSelectorOption
    _selected_item = 'xpath=.//*[@data-crlat="selItem"]'
    _drop_down = 'xpath=.//*[@data-crlat="dropDown"]'

    @property
    def drop_down(self):
        return ComponentBase(selector=self._drop_down, context=self._we)

    def select_value(self, text):
        if not self.is_selected():
            click(self.drop_down._we)
            self.is_selected(timeout=30)
        items = self.items_as_ordered_dict
        if text in items.keys():
            item = items.get(text)
            click(item._we)
        else:
            raise VoltronException(f'"{text}" is not present in the list of available markets {list(items.keys())}')

    def is_option_selected(self, option):
        self.scroll_to_we()
        return wait_for_result(lambda: self._get_webelement_text(selector=self._selected_item, context=self._we) == option,
                               name=f'Option "{option}" to be selected',
                               timeout=5)

    @property
    def available_options(self):
        click(self.drop_down._we)
        self.is_selected(timeout=5)
        option_values = list(self.items_as_ordered_dict.keys())
        return option_values

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        result = wait_for_result(lambda: 'active-dropdown' in self.get_attribute('class').strip(' ').split(' '),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result
