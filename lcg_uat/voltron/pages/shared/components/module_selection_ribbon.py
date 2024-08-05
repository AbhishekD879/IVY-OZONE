from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import scroll_to_center_of_element


class ModuleSelectionRibbonGroupingSelectionButtons(GroupingSelectionButtons):

    def click_button(self, button_name: str, timeout: float = 2) -> bool:
        # overriding click_button from GroupingSelectionButtons
        # as it make no sense to wait_for_result for self.current == button_name due to StaleElement on Module change
        selection_buttons = self.items_as_ordered_dict
        if button_name not in selection_buttons:
            raise VoltronException(f'Tab name "{button_name}" is not available, one of {list(selection_buttons.keys())} expected')
        scroll_to_center_of_element(selection_buttons[button_name]._we)
        if selection_buttons[button_name].is_selected(timeout=0.5):
            return True
        else:
            selection_buttons[button_name].click()


class ModuleSelectionRibbon(ComponentBase):
    _tabs_menu = 'xpath=.//*[@data-crlat="switchers" and contains(@class, "scrollable-switchers")]'
    _tabs_menu_type = ModuleSelectionRibbonGroupingSelectionButtons

    @property
    def tab_menu(self):
        return self._tabs_menu_type(selector=self._tabs_menu, context=self._we)
