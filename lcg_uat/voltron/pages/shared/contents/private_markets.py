from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.utils.helpers import cleanhtml


class PrivateMarketsStaticBlock(ComponentBase):
    _header = 'xpath=.//header'
    _content_text = 'xpath=.//*[contains(@class, "text-section")]'

    @property
    def header_text(self):
        return self._get_webelement_text(selector=self._header, timeout=0.2).strip()

    @property
    def content_text(self):
        text = self._get_webelement_text(selector=self._content_text, timeout=0.2).strip()
        return cleanhtml(text)

    @property
    def text(self):
        return f'{self.header_text.title()}\n{self.content_text}'


class PrivateMarketsTermsAndConditionsPage(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/private-markets\/terms-conditions'
    _static_block = 'xpath=.//*[@data-crlat="privateTerms"]'

    @property
    def static_block(self):
        return PrivateMarketsStaticBlock(selector=self._static_block, context=self._we)
