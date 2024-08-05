from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.js_functions import click


class FanzoneComingBack(Dialog):
    _default_action = 'close_button_click'
    _name = 'xpath=.//*[@class="FCB-Popup-title"]'
    _fanzone_coming_back_footer_button = 'xpath=.//*[@class="FCB-Popup-button_okCTA button"]'
    _fanzone_description_text = 'xpath=.//*[@class="FCB-Popup-text"]'
    _fanzone_coming_back_image = 'xpath=.//*[@class="FCB-Popup-img_svg"]'
    _close_button = 'xpath=.//*[@data-uat="popUpCloseButton"]'

    @property
    def fanzone_description_text(self):
        return self._get_webelement_text(selector=self._fanzone_description_text, context=self._we)

    @property
    def fanzone_coming_back_footer_button(self):
        return ButtonBase(selector=self._fanzone_coming_back_footer_button, context=self._we)

    def close_button_click(self):
        close_btn = self._find_element_by_selector(selector=self._close_button, context=self._we)
        click(close_btn)

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=3)

    @property
    def fanzone_coming_back_image(self):
        return self._find_elements_by_selector(selector=self._fanzone_coming_back_image, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self)