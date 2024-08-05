from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.content_header import HeaderLine


class BetSlipUnavailable(ComponentBase):
    _selections_unavailable_label = 'xpath=.//*[@data-crlat="labelRemotePatternErrorMsg"]'
    _header_line = 'xpath=.//*[@data-crlat="topBarBmaError"]'
    _header_line_type = HeaderLine

    @property
    def selections_unavailable_message(self):
        return self._get_webelement_text(selector=self._selections_unavailable_label, timeout=1)

    @property
    def header_line(self):
        return self._header_line_type(selector=self._header_line)
