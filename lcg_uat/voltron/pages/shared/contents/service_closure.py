from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.primitives.radio_button import RadioButtonBase
from voltron.pages.shared.components.primitives.text_labels import TextBase
from voltron.utils.waiters import wait_for_result


class ServiceClosureRadioButton(RadioButtonBase):
    _name = 'xpath=.//*[@class="ng-star-inserted"]/label | .//label[contains(@for, "reason-service_closure")]'

    @property
    def name(self):
        return self._we.text

    def is_checked(self, timeout=1, expected_result=True):
        return wait_for_result(lambda: self.before_element(selector=self._name) == '"\ueb09"',
                               timeout=3,
                               name=f'"{self.name}" Radio button status to be {expected_result}',
                               expected_result=expected_result)


class ReasonServiceClosure(ComponentBase):
    _item = 'xpath=.//*[@class="form-element ng-star-inserted"] | .//*[@class="form-element"]'
    _list_item_type = ServiceClosureRadioButton


class DurationServiceClosure(ComponentBase):
    _item = 'xpath=.//*[@class="form-element ng-star-inserted"]/*[contains(@class, "ng-star-inserted")] | .//*[@class="form-element"]/div'
    _list_item_type = ServiceClosureRadioButton


class ServiceClosureContainer(ComponentBase):
    _close_button = 'xpath=.//*[contains(text(), "Close")]'
    _name = 'xpath=.//*[@class="closure-detail-product"]/b'
    _current_status = 'xpath=.//*[@class="closure-detail-status"]'

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=1)

    @property
    def current_status(self):
        return self._get_webelement_text(selector=self._current_status, context=self._we, timeout=1)


class ServiceClosure(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/en\/mobileportal\/serviceclosure?(.+)'
    _list_item_type = ServiceClosureContainer
    _item = 'xpath=.//*[@class="full-content-block closure-detail"]'
    _close_button = 'xpath=.//*[contains(text(), "Close")]'
    _selected_product = 'xpath=.//*[@class="products-to-close"]/li'
    _duration_item = 'xpath=.//*[@class="form-element pt-4"]'
    _duration_item_type = DurationServiceClosure
    _reason_item = 'xpath=.//*[@class="form-element pt-4"]/following-sibling::div'
    _reason_item_type = ReasonServiceClosure
    _continue_button = 'xpath=.//button[contains(text(), "Continue")]'
    _info_message = 'xpath=.//*[@class="cms-container"]'
    _close_all_button = 'xpath=.//*[contains(text(), "Close all")]'
    _warning_message = 'xpath=.//*[@id="service-closure"]'

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
    def info_message(self):
        return TextBase(selector=self._info_message, context=self._we, timeout=15)

    def has_warning_message_text(self, text, timeout=3):
        warning_message = self._find_element_by_selector(selector=self._warning_message, timeout=0)
        return wait_for_result(lambda: warning_message.text == text,
                               timeout=timeout,
                               name=f'Warning message: "{text}" to be shown')
