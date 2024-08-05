from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import scroll_to_center_of_element
from voltron.utils.waiters import wait_for_result


class GroupingSelectionButtons(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="buttonSwitch"]'
    _list_item_type = ButtonBase
    _fade_out_overlay = True

    @property
    def current(self) -> str:
        scroll_to_center_of_element(self._we)
        active_button_name = wait_for_result(lambda: next((button_name for button_name, button in self.items_as_ordered_dict.items()
                                                           if button.is_selected(timeout=0.5)), ''),
                                             name=f'{self.__class__.__name__} - {self._list_item_type.__name__} to be active',
                                             timeout=1.5)
        self._logger.debug(f'*** Active {self.__class__.__name__} - {self._list_item_type.__name__} name is "{active_button_name}"')
        return active_button_name

    def click_button(self, button_name: str, timeout: float = 2) -> bool:
        selection_buttons = self.items_as_ordered_dict
        if button_name not in selection_buttons:
            raise VoltronException(f'Tab name "{button_name}" is not available, one of {list(selection_buttons.keys())} expected')
        scroll_to_center_of_element(selection_buttons[button_name]._we)
        if selection_buttons[button_name].is_selected(timeout=0.5):
            return True
        else:
            selection_buttons[button_name].click()
            return wait_for_result(lambda: self.current == button_name,
                                   name=f'Button: "{button_name}" to become active"',
                                   timeout=timeout,
                                   bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException))
