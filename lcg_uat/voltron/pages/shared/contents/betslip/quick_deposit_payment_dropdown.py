from voltron.pages.shared.components.primitives.selects import SelectBase


class PaymentAccountDropDown(SelectBase):
    _options = 'xpath=.//option'

    def select_account(self, account_name):
        self.click()
        options = self._find_elements_by_selector(selector=self._options)
        for option in options:
            if account_name in option.text:
                return option.click()

    def get_available_accounts(self):
        return self.available_options

    @property
    def current_account(self):
        return self.selected_item
