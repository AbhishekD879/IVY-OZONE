from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class MenuItem(ComponentBase):
    _name = 'xpath=.//*[@data-crlat="menuItemTitle"]'
    _indicator = 'xpath=.//*[@data-crlat="itemText"] | .//*[contains(@class,"menu-item-sub-icon")]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name, context=self._we)

    @property
    def indicator_content(self):
        return ComponentBase(selector=self._indicator, context=self._we)

    @property
    def indicator(self):
        indicator = self._get_webelement_text(selector=self._indicator, context=self._we)
        if self.after_element(selector=self._indicator, context=self._we):
            plus_sign = self.after_element(selector=self._indicator, context=self._we).strip('"')
            if plus_sign != 'none':
                return f'{indicator}{plus_sign}'
        return indicator if indicator else '0'

    def has_indicator(self, expected_result=True, timeout=5):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._indicator, timeout=0) is not None,
            timeout=timeout,
            expected_result=expected_result,
            name=f'Footer item indicator presence status to be {expected_result}')


class FooterNavigationMenu(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="menuItem"]'
    _list_item_type = MenuItem

    def _wait_active(self, timeout=2):
        self._we = self._find_myself()
        wait_for_result(lambda: all(self.items_as_ordered_dict),
                        name=f' {self.__class__.__name__} – {self._list_item_type.__name__} to load',
                        timeout=timeout)

    def get_footer_menu_item(self, name: str) -> object:
        """
        DESCRIPTION: This method get footer menu items based on it name
        :param name: Required menu item name
        :return: Instance of MenuItem class
        """
        if name in self.items_as_ordered_dict:
            return self.items_as_ordered_dict[name]
        else:
            raise VoltronException(f'Footer menu item: "{name}" '
                                   f'not found in menu items: {list(self.items_as_ordered_dict.keys())}, '
                                   f'please check if it configured in CMS')
