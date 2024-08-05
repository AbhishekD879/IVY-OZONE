from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent


class BaseDesktopModule(ComponentBase):
    _header = 'tag=header'
    _header_type = TextBase
    _content = 'xpath=.//*[contains(@data-crlat, "tab.show")]'
    _content_type = TabContent

    @property
    def name(self)->str:
        return self._header_type(selector=self._header, context=self._we).text

    @property
    def tab_content(self) -> TabContent:
        return self._content_type(selector=self._content, context=self._we)
