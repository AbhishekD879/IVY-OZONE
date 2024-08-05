from voltron.pages.shared.components.base import ComponentBase


class AccaInsuranceOffer(ComponentBase):
    _text = 'xpath=.//p'

    @property
    def text(self):
        text = ''
        paragraphs = self._find_elements_by_selector(selector=self._text)
        for p in paragraphs:
            text += '%s ' % p.text
        return text.rstrip()
