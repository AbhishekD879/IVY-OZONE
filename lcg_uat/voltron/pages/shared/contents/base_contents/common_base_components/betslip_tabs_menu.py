from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenuItem, TabsMenu
from voltron.utils.waiters import wait_for_result


class BetslipTabsMenuItem(TabsMenuItem):

    @property
    def name(self):
        result = wait_for_result(lambda: self._get_webelement_text(we=self._we),
                                 name="Tab to have visible name",
                                 timeout=5)
        return result if result else ''

    def click(self):
        self.scroll_to_we()
        self.perform_click()

    def is_selected(self, expected_result=True, timeout=2, poll_interval=0.5, name=None):
        if not name:
            name = '"%s" selected status is: %s' % (self.__class__.__name__, expected_result)
        return wait_for_result(lambda: 'active' in self._we.get_attribute('class'),
                               expected_result=expected_result,
                               timeout=timeout,
                               poll_interval=poll_interval,
                               name=name)


class BetslipTabsMenu(TabsMenu):
    _item = 'xpath=.//*[@data-crlat="bsTab"]'
    _list_item_type = BetslipTabsMenuItem
