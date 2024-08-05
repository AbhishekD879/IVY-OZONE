from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.dialogs.dialog_base import Dialog
from voltron.utils.js_functions import click


class OddsBoostOnLogin(Dialog):
    _default_action = 'click_thanks_link'
    _name = 'xpath=.//*[@data-crlat="dTitle"]'
    _thanks_link = 'xpath=.//*[@class="thanks"]'
    _show_more_button = 'xpath=.//button[contains(@class,"btn btn-style")]'
    _odd_boost_logo = 'xpath=.//*[@class="boost-icon"]'
    _dont_show_this_again_checkbox = 'xpath=.//*[contains(@class,"show-toggle")]'

    @property
    def description(self):
        return self._get_webelement_text(selector=self._dialog_content, context=self._we)

    @property
    def thanks_link(self):
        return ButtonBase(selector=self._thanks_link, context=self._we)

    def click_thanks_link(self):
        thanks_link = self._find_element_by_selector(selector=self._thanks_link, context=self._we)
        click(thanks_link)

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=3)

    @property
    def show_more_button(self):
        return ButtonBase(selector=self._show_more_button, context=self._we)

    @property
    def odd_boost_logo(self):
        return self._find_elements_by_selector(selector=self._odd_boost_logo, context=self._we)

    @property
    def dont_show_this_again_checkbox(self):
        return CheckBoxBase(selector=self._dont_show_this_again_checkbox, context=self._we)
