from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.checkboxes import CheckBoxBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.utils.exceptions.voltron_exception import VoltronException


class SelfExclusion(BaseContent):
    _url_pattern = r'^http[s]?:\/\/.+\/selfexclusion'
    _self_exclusion = 'xpath=.//*[contains(@class, "link") and contains(text(), "Self-exclusion")]'
    _continue_button = 'xpath=.//*[contains(text(), "Continue")]'
    _duration_options = 'xpath=.//*[@class="form-element"]/div'
    _reason_options = 'xpath=.//*[@name="reason"]'
    _self_exclusion_title = 'xpath=.//*[@data-crlat="headerTitle.leftMessage"]'
    _self_exclusion_content = 'xpath=.//*[@data-crlat="cmsContent"]'
    _cancel_button = 'xpath=.//button[contains(text(),"Cancel")]'
    _reason_options_list = 'xpath=.//*[contains(@class,"link-element")]'
    _duration_options_btn = 'xpath=.//*[@name="durationOpt"]'
    _take_short_time_out = 'xpath=.//*[contains(text(),"Take a short time-out")]'
    _consequences_desription = 'xpath=.//*[contains(@class,"closure-details")]'
    _consequences_info_message = 'xpath=.//*[@class="cms-container"]'
    _customer_service_team_link = 'xpath=.//*[contains(@class,"closure-details")]//a'
    _date_time = 'xpath=.//*[@id="self-exclusion"]//p[2]//b'

    @property
    def self_exclusion_link(self):
        return ButtonBase(selector=self._self_exclusion, context=self._we)

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)

    @property
    def duration_options(self):
        return self._find_elements_by_selector(selector=self._duration_options, context=self._we)

    @property
    def reason_options(self):
        return self._find_elements_by_selector(selector=self._reason_options, context=self._we)

    @property
    def self_exclusion_title(self):
        return self._find_element_by_selector(selector=self._self_exclusion_title, context=self._we)

    @property
    def self_exclusion_content(self):
        return self._find_element_by_selector(selector=self._self_exclusion_content, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def reason_options_list(self):
        return self._find_elements_by_selector(selector=self._reason_options_list, context=self._we)

    @property
    def duration_options_btn(self):
        return self._find_elements_by_selector(selector=self._duration_options_btn, context=self._we)

    @property
    def take_short_time_out(self):
        return ButtonBase(selector=self._take_short_time_out, context=self._we)

    @property
    def consequences_desription(self):
        return TextBase(selector=self._consequences_desription, context=self._we, timeout=3)

    @property
    def consequences_info_message(self):
        return TextBase(selector=self._consequences_info_message, context=self._we, timeout=15)

    @property
    def customer_service_team_link(self):
        return self._find_elements_by_selector(selector=self._customer_service_team_link, context=self._we)

    @property
    def date_time(self):
        return TextBase(selector=self._date_time, context=self._we, timeout=15)


class SelfExclusionSelection(SelfExclusion):
    _url_pattern = r'^http[s]?:\/\/.+\/selfexclusion\/selection'
    _image = 'xpath=.//*[@class="tab-tile-image"]'
    _choose_button = 'xpath=.//button[contains(text(), "Choose")]'

    @property
    def image(self):
        return self._find_elements_by_selector(selector=self._image, context=self._we, timeout=3)

    @property
    def choose_button(self):
        return ButtonBase(selector=self._choose_button, context=self._we)


class SelfExclusionOptions(SelfExclusion):
    _url_pattern = r'^http[s]?:\/\/.+\/selfexclusion\/options'
    _brand = 'xpath=.//*[@name="brand"]'
    _password_input = 'xpath=.//*[contains(@type,"password")]'
    _self_exclude_btn = 'xpath=.//*[contains(text(),  "Self exclude ")]'
    _info_message = 'xpath=.//*[@class="cms-container"]'
    _date_time = 'xpath=.//*[@id="self-exclusion"]//p[2]//b'
    _confirm = 'xpath=.//*[@class="dialog-content confirm-content"]/div//input'
    _header = 'xpath=.//*[contains(@class, "header-ctrl-txt")]'
    _consequences = 'xpath=.//*[@id="self-exclusion"]//fieldset[1]/legend'
    _after_confirmation = 'xpath=.//*[@id="self-exclusion"]//fieldset[2]/legend'
    _cancel_btn = 'xpath=//*[@id="self-exclusion"]//button[contains(text(),"Cancel")]'

    @property
    def brand(self):
        return self._find_element_by_selector(selector=self._brand, context=self._we)

    @property
    def password_field(self):
        return self._find_element_by_selector(selector=self._password_input, context=self._we)

    def password_input(self, value):
        we = self._find_element_by_selector(selector=self._password_input, context=self._we)
        if we is None:
            raise VoltronException('No Password field is not present')
        we.clear()
        we.send_keys(value)

    @property
    def self_exclude_button(self):
        return ButtonBase(selector=self._self_exclude_btn, context=self._we)

    @property
    def info_message(self):
        return TextBase(selector=self._info_message, context=self._we, timeout=15)

    @property
    def header(self):
        return TextBase(selector=self._header, context=self._we)

    @property
    def date_time(self):
        return TextBase(selector=self._date_time, context=self._we, timeout=15)

    @property
    def password_input_field(self):
        return self._find_element_by_selector(selector=self._password_input, context=self._we)

    @property
    def consequences(self):
        return TextBase(selector=self._consequences, context=self._we)

    @property
    def after_confirmation(self):
        return TextBase(selector=self._after_confirmation, context=self._we)

    @property
    def cancel_btn(self):
        return ButtonBase(selector=self._cancel_btn, context=self._we)


class SelfExclusionDialog(ComponentBase):
    _confirm_checkbox = 'xpath=.//*[@class="form-element"][.//input[@id="confirm"]]'
    _understand_checkbox = 'xpath=.//*[@class="form-element"][.//input[@id="understand"]]'
    _yes = 'xpath=.//*[contains(text(), "YES")]'

    @property
    def yes(self):
        return self._find_element_by_selector(selector=self._yes, context=self._we)

    @property
    def confirm_checkbox(self):
        return CheckBoxBase(selector=self._confirm_checkbox, context=self._we)

    @property
    def understand_checkbox(self):
        return CheckBoxBase(selector=self._understand_checkbox, context=self._we)
