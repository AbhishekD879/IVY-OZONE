from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class ButtonsArrayBase(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="toggleButton"]'
    _list_item_type = ButtonBase

    @property
    def available_options(self):
        return list(self.items_as_ordered_dict.keys())

    @property
    def value(self):
        return self.get_attribute('selected-btn')

    @value.setter
    def value(self, value):
        self._logger.debug(
            f'*** User has set "{value}" on toggleButton. Call of "{self.__class__.__name__}"'
        )
        self.click_item(value)
