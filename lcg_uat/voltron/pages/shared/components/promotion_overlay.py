from voltron.pages.shared.components.accordions_container import Accordion
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class PromotionOverlayHeader(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="title"]'
    _close_button = 'xpath=.//*[@data-crlat="closeButton"]'

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)


class TermsAndConditionsSection(Accordion):
    _header = 'xpath=.//*[@data-crlat="containerHeader"]'
    _content = 'xpath=.//*[@data-crlat="containerContent"]'

    @property
    def content(self):
        return self._get_webelement_text(selector=self._content).replace('\n', '')


class PromotionOverlayDetails(ComponentBase):
    _image = 'xpath=.//*[@data-crlat="image"]'
    _short_description = 'xpath=.//*[@data-crlat="shortDescription"]'
    _description = 'xpath=.//*[@data-crlat="promoDescription"]'
    _terms_and_conditions_section = 'xpath=.//*[@data-crlat="accordion"]'
    _terms_and_conditions_section_type = TermsAndConditionsSection
    _bet_not_button = 'xpath=.//*[@data-crlat="betNow"]'

    def scroll_to_we(self, web_element=None):
        """
        Bypassing scroll as element in a view
        """
        pass

    @property
    def image_source(self):
        return ComponentBase(selector=self._image, context=self._we, timeout=5).get_attribute('src')

    @property
    def short_description(self):
        return self._get_webelement_text(selector=self._short_description, timeout=0.5)

    @property
    def bet_now_button(self):
        return ButtonBase(selector=self._bet_not_button, context=self._we)

    @property
    def description(self):
        return self._get_webelement_text(selector=self._description).replace('\n', '')

    @property
    def terms_and_conditions(self):
        return self._terms_and_conditions_section_type(selector=self._terms_and_conditions_section, context=self._we)


class PromotionOverlay(ComponentBase):
    _header = 'xpath=.//*[@data-crlat="header"]'
    _header_type = PromotionOverlayHeader
    _details = 'xpath=.//*[@data-crlat="details"]'
    _details_type = PromotionOverlayDetails

    @property
    def header(self):
        return self._header_type(selector=self._header, context=self._we)

    @property
    def details(self):
        return self._details_type(selector=self._details, context=self._we)
