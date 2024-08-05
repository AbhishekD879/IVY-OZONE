from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.buttons_array import ButtonsArrayBase


class ButtonsArrayBaseLadbrokes(ButtonsArrayBase):
    _item = 'xpath=.//*[contains(@class, "fn-title-button")]'
    _active_item = 'xpath=.//*[@class="fn-title-button active"]'
    _list_item_type = ButtonBase

    @property
    def available_options(self):
        return list(self.items_as_ordered_dict.keys())

    @property
    def value(self):
        return ButtonBase(selector=self._active_item)

    @value.setter
    def value(self, value):
        self._logger.debug(
            f'*** User has set "{value}" on toggleButton. Call of "{self.__class__.__name__}"'
        )
        self.click_item(value)
