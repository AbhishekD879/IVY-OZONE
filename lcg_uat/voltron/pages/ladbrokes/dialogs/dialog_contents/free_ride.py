from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.pages.shared.components.primitives.buttons import ButtonBase


class FreeRideDialog(Dialog):
    _welcome_message = 'xpath=.//*[@class="subHeading"]'
    _sound_switch = 'xpath=.//*[@class="slider round"]'
    _CTA_button = 'xpath=.//*[@class="freeRideButton"]'
    _terms_and_conditions_text = 'xpath=.//*[@class="tnCText"]/span'
    _terms_and_conditions = 'xpath=.//*[@class="tnCLink"]'
    _close_icon = 'xpath=.//*[@class="btn-close closePopup"]'
    _free_ride_text_image = 'xpath=.//*[@class="imgContainer"]'

    @property
    def welcome_message(self):
        return self._get_webelement_text(selector=self._welcome_message, timeout=5)

    @property
    def sound_switch(self):
        return self._find_element_by_selector(selector=self._sound_switch, timeout=5)

    @property
    def cta_button(self):
        return ButtonBase(selector=self._CTA_button, timeout=5)

    @property
    def cta_button_text(self):
        return self._get_webelement_text(selector=self._CTA_button, timeout=5)

    @property
    def terms_and_conditions_text(self):
        return self._get_webelement_text(selector=self._terms_and_conditions_text, timeout=5)

    @property
    def terms_and_conditions(self):
        return self._find_element_by_selector(selector=self._terms_and_conditions, timeout=5)

    @property
    def close_icon(self):
        return self._find_element_by_selector(selector=self._close_icon, timeout=2)

    @property
    def free_ride_text_image(self):
        return self._find_element_by_selector(selector=self._free_ride_text_image, timeout=2)
