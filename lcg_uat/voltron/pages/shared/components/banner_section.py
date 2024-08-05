from voltron.pages.shared import get_driver
from voltron.pages.shared.components.base import ComponentBase
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.js_functions import click
from voltron.utils.waiters import wait_for_result


class Banner(ComponentBase):
    _banner_name = 'xpath=.//*[@data-crlat="bannerName"]'

    @property
    def name(self):
        return self._find_element_by_selector(selector=self._banner_name, timeout=5).get_attribute('title')

    def click(self):
        we = self._find_element_by_selector(selector=self._banner_name, timeout=0)
        self.scroll_to_we(web_element=we)
        click(we)


class BannerSection(ComponentBase):
    _item = 'xpath=.//*[@data-crlat="slide" and not(contains(@class, "copy"))]'
    _list_item_type = Banner
    banner_index = None

    def __init__(self, selector='xpath=.//*[@data-crlat="sectionBanner"]', *args, **kwargs):
        super(BannerSection, self).__init__(selector=selector, *args, **kwargs)

    def wait_for_banners(self):
        return wait_for_result(lambda: len(self._find_elements_by_selector(selector=self._item, timeout=0)) > 0,
                               name='Banners displaying',
                               timeout=60)

    @property
    def banners(self):
        self.wait_for_banners()
        items_we = self._find_elements_by_selector(selector=self._item, timeout=0)
        self._logger.debug(f'*** Found {len(items_we)} {self.__class__.__name__} – {self._list_item_type.__name__} items')
        items_array = []
        for item_we in items_we:
            item_component = self._list_item_type(web_element=item_we)
            items_array.append(item_component)
        return items_array

    @property
    def banners_names(self):
        names_array = []
        for banner in self.banners:
            names_array.append(banner.name)
        return names_array

    @property
    def number_of_banners(self):
        return len(self.banners)

    @property
    def _active_banner_tuple(self):
        if len(self.banners) == 0:
            raise VoltronException('No banners are displayed')
        for i, banner in enumerate(self.banners):
            from time import sleep
            sleep(0.5)
            if get_driver().execute_script(
                    'return (arguments[0].getBoundingClientRect().x === 0);', banner._we
            ):
                return i, banner
        raise VoltronException('Active banner not found.')

    @property
    def active_banner(self):
        return self._active_banner_tuple[1]

    @property
    def active_banner_index(self):
        return self._active_banner_tuple[0] + 1

    @property
    def active_banner_name(self):
        return self.active_banner.name

    def wait_for_active_banner_to_change(self, timeout=10, expected_result=True):
        """Waits for currently active banner to be rotated"""
        current_active_banner = self.active_banner_index
        timeout *= self.number_of_banners
        if self.number_of_banners > 1:
            return wait_for_result(lambda: current_active_banner != self.active_banner_index,
                                   name='Start banner index: %s, current banner index: %s'
                                        % (current_active_banner, self.active_banner_index),
                                   timeout=timeout,
                                   expected_result=expected_result
                                   )
        else:
            self._logger.warning('*** Banners amount: %s not enough for rotation' % self.number_of_banners)
            return expected_result
