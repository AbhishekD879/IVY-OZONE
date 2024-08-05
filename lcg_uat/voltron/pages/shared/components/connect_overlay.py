from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class ConnectOverlay(ComponentBase):
    _close_button = 'xpath=.//*[@data-crlat="overlayCloseBtn"]'
    _arrow_text = 'xpath=.//*[@data-crlat="arrowText"]'
    _swipe_arrow = 'xpath=.//*[@data-crlat="swipeArrow"]'
    _connect_icon = 'xpath=.//*[@data-crlat="connectIcon"]'
    _text = 'xpath=.//*[@data-crlat="overlayTextPanel"]'
    _navigate_to_connect = 'xpath=.//*[@data-crlat="navigateToConnect"]'
    _do_not_show = 'xpath=.//*[@data-crlat="dontShowOverlay"]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def arrow_text(self):
        return self._get_webelement_text(selector=self._arrow_text, context=self._we)

    @property
    def overlay_text(self):
        return self._get_webelement_text(selector=self._text, context=self._we)

    @property
    def swipe_arrow(self):
        return ComponentBase(selector=self._swipe_arrow, context=self._we)

    @property
    def connect_icon(self):
        return ButtonBase(selector=self._connect_icon, context=self._we)

    @property
    def navigate_to_connect(self):
        return ButtonBase(selector=self._navigate_to_connect, context=self._we)

    @property
    def do_not_show(self):
        return ButtonBase(selector=self._do_not_show, context=self._we)
