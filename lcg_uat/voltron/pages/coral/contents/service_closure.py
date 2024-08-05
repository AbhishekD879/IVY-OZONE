from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.radio_button import RadioButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.waiters import wait_for_result


class ServiceClosureRadioButton(RadioButtonBase):
    _name = 'xpath=.//*[@class="form-element"]/div/label | .//label[contains(@for, "reason-service_closure")]'
    _input = 'xpath=.//input'

    @property
    def name(self):
        return self._get_webelement_text(we=self._we)

    @property
    def input(self):
        return ComponentBase(selector=self._input, context=self._we, timeout=1)

    def is_checked(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self.input._we.is_selected(),
                               timeout=timeout,
                               name=f'{self.__class__.__name__} Radio button status to be {expected_result}',
                               expected_result=expected_result)


class ReasonServiceClosure(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"form-element")][.//input[@name="reasonOpt"]]'
    _list_item_type = ServiceClosureRadioButton


class DurationServiceClosure(ComponentBase):
    _item = 'xpath=.//*[contains(@class,"form-element")][.//input[@name="durationOpt"]]'
    _list_item_type = ServiceClosureRadioButton


class CoralServiceClosureContainer(ComponentBase):
    _close_button = 'xpath=.//*[contains(text(), "Close")]'
    _open_button = 'xpath=.//*[contains(text(), "Open")]'
    _name = 'xpath=.//*[@class="closure-detail-product"]/b'
    _current_status = 'xpath=.//*[@class="closure-detail-status"]'
    _play_button = 'xpath=.//*[contains(@class,"playbutton")]'
    _locked_button = 'xpath=.//*[contains(@class,"locked-i")]'
    _closed_date_time = 'xpath=.//*[contains(text(), "Closed until")]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def open_button(self):
        return ButtonBase(selector=self._open_button, context=self._we)

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=1)

    @property
    def current_status(self):
        return self._get_webelement_text(selector=self._current_status, context=self._we, timeout=1)

    @property
    def play_button(self):
        return self._find_element_by_selector(selector=self._play_button, context=self._we)

    @property
    def play_button_sign(self):
        return self.before_element(selector=self._play_button, context=self._we)

    @property
    def locked_button(self):
        return self._find_element_by_selector(selector=self._locked_button, context=self._we)

    @property
    def locked_button_sign(self):
        return self.before_element(selector=self._locked_button, context=self._we)

    @property
    def closed_date_time(self):
        return self._get_webelement_text(selector=self._closed_date_time, context=self._we, timeout=1)


class Consequences(ComponentBase):
    _items = 'xpath=.//*[@class="full-content-block"]//*[@class="theme-locked-i"]'

    @property
    def consequences_list(self):
        return self._find_elements_by_selector(selector=self._items, timeout=3)


class Reopening(ComponentBase):
    _items = 'xpath=.//*[@class="content-block"]//*[@class="theme-unlocked-i"]'

    @property
    def reopening_list(self):
        return self._find_elements_by_selector(selector=self._items, timeout=3)


class CoralServiceClosure(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/en\/mobileportal\/serviceclosure?(.+)'
    _list_item_type = CoralServiceClosureContainer
    _item = 'xpath=.//section[contains(@class, "closure-detail")]'
    _close_button = 'xpath=.//*[contains(text(), "Close")]'
    _selected_product = 'xpath=.//*[@class="products-to-close"]/li'
    _duration_item = 'xpath=.//*[@class="form-element pt-4"]'
    _duration_item_type = DurationServiceClosure
    _reason_item = 'xpath=.//*[@class="form-element pt-4"]/following-sibling::div'
    _reason_item_type = ReasonServiceClosure
    _continue_button = 'xpath=.//button[contains(text(), "Continue")]'
    _cancel_button = 'xpath=.//button[contains(text(), "Cancel")]'
    _info_message = 'xpath=.//*[@class="cms-container"]'
    _close_all_button = 'xpath=.//*[contains(text(), "Close all")]'
    _warning_message = 'xpath=.//*[@id="service-closure"]'
    _content_block_message = 'xpath=.//*[@class="content-block"]'
    _consequence_item_type = Consequences
    _reopening_item_type = Reopening
    _consequences_and_reopening = 'xpath=.//*[contains(@class, "closure-details no-list-icons")]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def close_all_button(self):
        return ButtonBase(selector=self._close_all_button, context=self._we)

    @property
    def selected_product(self):
        return self._get_webelement_text(selector=self._selected_product, context=self._we, timeout=1)

    @property
    def duration_options(self):
        return self._duration_item_type(selector=self._duration_item, context=self._we, timeout=3)

    @property
    def reason_options(self):
        return self._reason_item_type(selector=self._reason_item, context=self._we, timeout=3)

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)

    @property
    def cancel_button(self):
        return ButtonBase(selector=self._cancel_button, context=self._we)

    @property
    def info_message(self):
        return TextBase(selector=self._info_message, context=self._we, timeout=15)

    def has_warning_message_text(self, text, timeout=3):
        warning_message = self._find_element_by_selector(selector=self._warning_message, timeout=0)
        return wait_for_result(lambda: warning_message.text == text,
                               timeout=timeout,
                               name=f'Warning message: "{text}" to be shown')

    @property
    def control_section_message(self):
        return self._get_webelement_text(selector=self._content_block_message)

    @property
    def consequences(self):
        return self._consequence_item_type(selector=self._consequences_and_reopening, context=self._we)

    @property
    def reopening(self):
        return self._reopening_item_type(selector=self._consequences_and_reopening, context=self._we)
