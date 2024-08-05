from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class DateTab(GroupingSelectionButtons):
    _today = 'xpath=.//*[@data-crlat="buttonSwitch" and contains(text(), "Today")]'
    _tomorrow = 'xpath=.//*[@data-crlat="buttonSwitch" and contains(text(), "Tomorrow")]'
    _future = 'xpath=.//*[@data-crlat="buttonSwitch" and contains(text(), "Future")]'
    _current_tab = 'xpath=.//*[@data-crlat="buttonSwitch" and contains(@class, "active")]'

    @property
    def today(self):
        return ButtonBase(selector=self._today, context=self._we)

    @property
    def tomorrow(self):
        return ButtonBase(selector=self._tomorrow, context=self._we)

    @property
    def future(self):
        return ButtonBase(selector=self._future, context=self._we)

    @property
    def current_date_tab(self):
        return self._get_webelement_text(selector=self._current_tab, timeout=1)
