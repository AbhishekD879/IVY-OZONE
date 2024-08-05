from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.bet_button import BetButton
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup


class SportEnhancedMultiplesEvent(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="enhancedSportNameTitle"]'
    _header = 'xpath=.//*[@data-crlat="enhancedSlideHeaderContainer"]'
    _event_name = 'xpath=.//*[@data-crlat="enhancedTitleEventName"]'
    _outcome_name = 'xpath=.//*[@data-crlat="outcomeName"]'
    _bet_button = 'xpath=.//*[@data-crlat="betButton"]'
    _start_time = 'xpath=.//*[contains(@class, "enhanced-slide-time")]/time'

    @property
    def start_time(self):
        return self._find_element_by_selector(selector=self._start_time, context=self._we, timeout=1)

    @property
    def header(self):
        return TextBase(selector=self._header, context=self._we, timeout=1)

    @property
    def name(self):
        return TextBase(selector=self._name, context=self._we, timeout=1)

    @property
    def outcome_name(self):
        return TextBase(selector=self._outcome_name, context=self._we, timeout=1)

    @property
    def bet_button(self):
        return BetButton(selector=self._bet_button, context=self._we)

    @property
    def event_name(self):
        return self._find_element_by_selector(selector=self._event_name, context=self._we, timeout=1)


class SportEnhancedMultiples(EventGroup):
    _item = 'xpath=.//*[@data-crlat="raceCard.event"]'
    _list_item_type = SportEnhancedMultiplesEvent
