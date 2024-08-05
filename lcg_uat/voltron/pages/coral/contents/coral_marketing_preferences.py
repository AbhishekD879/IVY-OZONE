from voltron.pages.shared.contents.change_password import ChangePasswordHeader
from voltron.pages.shared.contents.marketing_preferences import MarketingPreferences, MarketingPreferencesCheckBox
from voltron.pages.shared.components.primitives.text_labels import LinkBase


class CoralMarketingPreferencesHeader(ChangePasswordHeader):
    pass


class CoralMarketingPreferencesCheckBox(MarketingPreferencesCheckBox):
    _input = 'xpath=.//input[@type="checkbox"]'

    @property
    def name(self):
        return self._get_webelement_text(we=self._we, timeout=0.5)


class CoralMarketingPreferences(MarketingPreferences):
    # todo:     VOL-5537  CoralMarketingPreferences should be moved to shared and renamed
    _item = 'xpath=.//div[contains(@class, "preference-type")]/div[not(@style="display: none;")]'
    _list_item_type = CoralMarketingPreferencesCheckBox
    _submit_button = 'xpath=.//button[contains(text(),"Save")]'
    _header_type = CoralMarketingPreferencesHeader
    _header = 'xpath=.//vn-header-bar'
    _validation_text = 'xpath=.//div[contains(@class,"cms-container")]'
    _close_button = 'xpath=.//*[contains(@class, "header-ctrl-r")]/span'
    _privacy_notice = 'xpath=.//*[contains(text(), "Privacy Notice")]'
    _back_button = 'xpath=.//div[contains(@class,"header-ctrl-l")]'

    @property
    def privacy_notice(self):
        return LinkBase(selector=self._privacy_notice, context=self._we)

    @property
    def header(self):
        return self._header_type(selector=self._header, context=self._we)

    @property
    def save_button(self):
        return self._find_element_by_selector(selector=self._submit_button, context=self._we)

    @property
    def back_button(self):
        return self._find_element_by_selector(selector=self._back_button, context=self._we)

    @property
    def validation_message(self):
        return self._find_element_by_selector(selector=self._validation_text, context=self._we)

    @property
    def close_icon(self):
        return self._find_element_by_selector(selector=self._close_button, context=self._we)


class CoralMarketingPreferencesDesktop(CoralMarketingPreferences):
    _title = 'xpath=.//h2[contains(@style,"display: block;")] | .//*[contains(text(), "Preferences")]'

    @property
    def title(self):
        return self._get_webelement_text(selector=self._title, timeout=2)
