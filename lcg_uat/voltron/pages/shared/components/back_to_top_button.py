from voltron.pages.shared.components.primitives.buttons import ButtonBase


class BackToTopButton(ButtonBase):
        _icon = 'xpath=.//*[@data-crlat="upArrow"]'

        @property
        def icon(self):
            return ButtonBase(selector=self._icon, context=self._we)
