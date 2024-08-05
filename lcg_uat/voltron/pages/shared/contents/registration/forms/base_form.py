from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.pages.shared.components.content_header import HeaderLineBase
from voltron.utils.waiters import wait_for_result


class RegistrationHeader(HeaderLineBase):
    _brand_logo = 'xpath=.//div[contains(@class, "brand-logo")]'
    _close_button = 'xpath=.//*[contains(@class, "ui-close")]'

    @property
    def brand_logo(self):
        return ButtonBase(selector=self._brand_logo, context=self._we)

    @property
    def close_button(self):
        return ButtonBase(selector=self._close_button, context=self._we)


class RegistrationStepItem(ComponentBase):

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None) -> bool:
        if not name:
            name = f'"{self.__class__.__name__}" selected status is: {expected_result}'
        result = wait_for_result(lambda: 'stepper--pill' in self.get_attribute('class').strip(' '),
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 poll_interval=poll_interval,
                                 name=name)
        return result

    @property
    def name(self):
        return self.get_attribute('innerText')


class RegistrationSteps(ComponentBase):
    _item = 'xpath=.//*[contains(@class, "progress-pills__stepper")]'
    _list_item_type = RegistrationStepItem


class StepFormBase(ComponentBase):
    _submit_button = 'xpath=.//button[@id="continue"]'

    @property
    def step_button(self):
        return ButtonBase(selector=self._submit_button, context=self._we)

    def submit_form(self):
        self.step_button.click()
