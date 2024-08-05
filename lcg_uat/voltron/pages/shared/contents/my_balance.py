from voltron.pages.shared.menus.right_menu import RightMenuItem
from voltron.pages.shared.contents.base_content import BaseContent


class MyBalanceMenuItem(RightMenuItem):
    pass


class MyBalance(BaseContent):
    _item = 'xpath=.//*[contains(@class, "list-nav-link")]'
    _list_item_type = MyBalanceMenuItem
    _my_balance_footer = 'xpath=.//vn-am-bonus-balance'

    @property
    def my_balance_footer_items(self):
        return self._find_element_by_selector(selector=self._my_balance_footer)
