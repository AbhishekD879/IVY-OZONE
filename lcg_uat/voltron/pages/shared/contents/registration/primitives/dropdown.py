from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.selects import SelectBase
from voltron.utils.waiters import wait_for_result


class RegistrationDropdown(ComponentBase):
    _dropdown = 'xpath=.//select'
    _dropdown_type = SelectBase
    _validation_message = 'xpath=//*[contains(@class,"m2-validation-message")]'

    @property
    def dropdown(self):
        return self._dropdown_type(selector=self._dropdown, context=self._we)

    def has_error_message(self, expected_result=True, timeout=3):
        return wait_for_result(lambda: self._find_element_by_selector(self._validation_message, timeout=0) is not None,
                               timeout=timeout,
                               expected_result=expected_result,
                               name=f'Error message to be {expected_result}')
