from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.menu_carousel import MenuCarouselItem
from voltron.pages.shared.components.primitives.text_labels import LinkBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class SportMenuGroupedItem(MenuCarouselItem):
    _title_text = 'xpath=.//*[@data-crlat="menuItemTitle"] | .//*[@data-crlat="favouriteItem.link"]'
    _link = 'xpath=.//*[@data-crlat="menuItem.link"]'
    _favourite_checkbox = 'xpath=.//*[@data-crlat="favouriteCheckbox"]'
    _link_item_type = LinkBase

    @property
    def link(self):
        return self._link_item_type(selector=self._link, context=self._we, timeout=1)

    @property
    def favourite_checkbox(self):
        return ButtonBase(selector=self._favourite_checkbox, context=self._we)

    def has_favourite_checkbox(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._favourite_checkbox,
                                                   timeout=0) is not None,
            name=f'favourite checkbox status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class SportMenuItemsGroup(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="menuItem"]'
    _group_name = 'xpath=//*[@data-crlat="columnTitle"]'  # DO NOT ADD PERIOD(.) IN THE XPATH
    _list_item_type = SportMenuGroupedItem

    @property
    def name(self):
        return self._get_webelement_text(selector=self._group_name)

class FavouriteSportMenuItemsGroup(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="favouriteItem"]'
    _group_name = 'xpath=//*[@data-crlat="favouriteTitle"]'  # DO NOT ADD PERIOD(.) IN THE XPATH
    _list_item_type = SportMenuGroupedItem

    @property
    def name(self):
        return self._get_webelement_text(selector=self._group_name)

class SportLeftMenuItem(ComponentBase):
    _title = 'xpath=.//*[@data-crlat="menuItemTitle"]'

    def _wait_active(self, timeout=0):
        """
        Override wait active
        """
        pass

    @property
    def name(self):
        return self._get_webelement_text(selector=self._title, timeout=1).strip()


class DesktopLeftSportMenu(ComponentBase):
    _favourite_group = 'xpath=//*[@data-crlat="favouriteTitle"]/following-sibling::ul'
    _main_group = 'xpath=.//*[@data-crlat="leftColumnSection"]'
    _top_group = 'xpath=.//*[@data-crlat="topSportsItems"]'  # TODO not sure what is that for
    _az_group = 'xpath=//*[@data-crlat="columnTitle"]/following-sibling::nav/ul'
    _menu_groups = {'Main': _main_group, 'Top': _top_group, 'AZ': _az_group}
    _item = 'xpath=.//*[@data-crlat="menuItem.link"]'
    _list_item_type = SportLeftMenuItem
    _sport_menu_items_group = SportMenuItemsGroup

    def sport_menu_items_group(self, group_name):
        return SportMenuItemsGroup(selector=self._menu_groups[group_name])

    def has_favourite_sport_menu_items_group(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._favourite_group,
                                                   timeout=0) is not None,
            name=f'favourite sport menu items group status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def favourite_sport_menu_items_group(self):
        return FavouriteSportMenuItemsGroup(selector=self._favourite_group)