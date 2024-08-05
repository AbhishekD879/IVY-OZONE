from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.exceptions.voltron_exception import VoltronException


class CoralAccountClosureContainer(ComponentBase):
    _name = 'xpath=.//*[@class="custom-control-label"]'

    @property
    def name(self):
        return self._wait_for_not_empty_web_element_text(selector=self._name, context=self._we, timeout=1)


class CoralAccountClosure(ComponentBase):
    _url_pattern = r'^http[s]?:\/\/.+\/accountclosure'
    _continue_button = 'xpath=.//button[contains(text(), "Continue")]'
    _cancel_button = 'xpath=.//*[contains(text(), "Cancel")]'
    _list_item_type = CoralAccountClosureContainer
    _item = 'xpath=.//*[contains(@class, "form-element")]'

    @property
    def continue_button(self):
        return ButtonBase(selector=self._continue_button, context=self._we)

    def select_option(self, option_name):
        for opt_name, opt in self.items_as_ordered_dict.items():
            if option_name in opt_name:
                opt.click()
                return opt_name
        raise VoltronException(f'Can not select option name "{option_name}" from "{list(self.items_as_ordered_dict.keys())}"')
