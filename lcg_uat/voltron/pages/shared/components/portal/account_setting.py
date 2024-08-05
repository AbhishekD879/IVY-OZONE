import tests
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.text_labels import LinkBase, TextBase
from voltron.pages.shared.contents.change_password import ChangePasswordHeader
from collections import OrderedDict


class AccountSettingHeader(ChangePasswordHeader):
    pass


class SettingMenuItem(ComponentBase):
    _title = 'xpath=.//a[contains(@class,"nav-link")] | ./span[contains(@class,"menu-item-txt")]'
    _link = 'xpath=.//a[contains(@class,"menu-item-link")] | .//a[contains(@class,"nav-link")]'

    @property
    def name(self):
        return self.title.text

    @property
    def title(self):
        return TextBase(selector=self._title, context=self._we, timeout=2)

    @property
    def link(self):
        return LinkBase(selector=self._link, context=self._we)


class AccountSettingPage(ComponentBase):
    _setting_header = 'xpath=.//vn-header-bar'
    _list_item_type = SettingMenuItem

    @property
    def setting_header(self):
        return AccountSettingHeader(selector=self._setting_header, timeout=2)

    @property
    def items_as_ordered_dict(self) -> OrderedDict:
        _item = 'xpath=.//lh-navigation-layout-top-menu-v2//*[@class="navigation-layout-nav-items"]//*[contains(@class,"nav-item")]' \
            if tests.settings.device_type != 'mobile' else \
            'xpath=.//vn-am-menu-item/vn-menu-item/a[contains(@class,"menu-item-link")]'
        items_we = self._find_elements_by_selector(selector=_item, context=self._we, timeout=self._timeout)
        self._logger.debug(
            f'*** Found {len(items_we)} {self.__class__.__name__} - {self._list_item_type.__name__} items')
        items_ordered_dict = OrderedDict()
        for item_we in items_we:
            list_item = self._list_item_type(web_element=item_we)
            list_item.scroll_to()
            items_ordered_dict.update({item_we.text: list_item})
        return items_ordered_dict
