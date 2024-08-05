from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase


class Description(ComponentBase):
    _cookie_policy = 'xpath=.//*'
    # data-crlat can't be added to those links as they build by CMS
    _privacy_policy_hyperlink = 'xpath=.//a[@title="privacy policy"]'
    _cookie_policy_hyperlink = 'xpath=.//a[@title="cookie policy"]'

    @property
    def text(self):
        return self._get_webelement_text(we=self._we)

    @property
    def cookie_policy(self):
        return self._find_element_by_selector(selector=self._cookie_policy)

    @property
    def privacy_policy_hyperlink(self):
        return LinkBase(selector=self._privacy_policy_hyperlink, context=self._we)

    @property
    def cookie_policy_hyperlink(self):
        return LinkBase(selector=self._cookie_policy_hyperlink, context=self._we)


class ButtonPanel(ComponentBase):
    _accept_and_close_btn = 'xpath=.//*[@data-crlat="acceptAndClose"]'
    _more_info = 'xpath=.//*[@data-crlat="more"]'

    @property
    def accept_and_close(self):
        return ButtonBase(selector=self._accept_and_close_btn)

    @property
    def more_info(self):
        return self._find_element_by_selector(selector=self._more_info)

    @property
    def more_info_hyperlink(self):
        return self.more_info.get_attribute('href')


class CookieBanner(ComponentBase):
    _description = 'xpath=.//*[@data-crlat="cookieDescription"] | .//*[@id="onetrust-group-container"]'
    _description_type = Description
    _button_panel = 'xpath=.//*[@data-crlat="panelButtons"] | .//*[@id="onetrust-button-group"]'
    _button_panel_type = ButtonPanel

    @property
    def description(self):
        return self._description_type(selector=self._description)

    @property
    def button_panel(self):
        return self._button_panel_type(selector=self._button_panel, timeout=1)
