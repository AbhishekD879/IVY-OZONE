from selenium.common.exceptions import WebDriverException
from selenium.webdriver import ActionChains

from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.contents.virtuals.racing_tab_content import VirtualTabsMenu
from voltron.pages.shared.contents.virtuals.racing_tab_content import VirtualTabsMenuItem
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


class VirtualSportsTabIconContent(ComponentBase):
    _sport_icon_link = 'css=use'

    def has_link(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._sport_icon_link, timeout=0, context=self._we)
                        .get_attribute('xlink:href') is not None,
            name=f'Link status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class VirtualSportsCarouselItem(VirtualTabsMenuItem):
    _sport_icon = 'xpath=.//*[@data-crlat="svg"]'
    _icon_content_type = VirtualSportsTabIconContent

    @property
    def name(self):
        return self.get_attribute('title')

    def click(self):
        self.scroll_to_we()
        try:
            self.perform_click()
        except WebDriverException as e:
            raise VoltronException(f'Can not click on {self.__class__.__name__}. {e}')

    def has_icon(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._sport_icon, context=self._we, timeout=0) is not None,
            name=f'Icon status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    @property
    def icon(self):
        return self._icon_content_type(selector=self._sport_icon, context=self._we)

    def click_sport_icon(self):
        we = self._find_element_by_selector(selector=self._sport_icon)
        self.scroll_to_we(we)
        ActionChains(get_driver()).move_to_element(we).click(we).perform()


class VirtualSportsCarousel(VirtualTabsMenu):
    _item = 'xpath=.//*[@data-crlat="item"]'
    _list_item_type = VirtualSportsCarouselItem
    _active_tab = 'xpath=.//*[@data-crlat="item" and contains(@class, "active")]'

    @property
    def current(self):
        button = self._find_element_by_selector(selector=self._active_tab, context=self._we, timeout=3)
        if button:
            return button.get_attribute('title')
        else:
            raise VoltronException("No sport tab is selected")
