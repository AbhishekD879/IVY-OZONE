from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

from voltron.pages.shared.components.breadcrumbs import Breadcrumbs
from voltron.pages.shared.contents.base_contents.common_base_components.event_group import EventGroup
from voltron.pages.shared.contents.base_contents.common_base_components.tabs_menu import TabsMenu
from voltron.pages.shared.contents.base_contents.sport_base import SportRacingPageBase
from voltron.pages.shared.contents.base_contents.common_base_components.tab_content import TabContent
from voltron.pages.shared.components.base import ComponentBase
from voltron.pages.shared.components.primitives.buttons import ButtonBase
from voltron.utils.waiters import wait_for_result


class PromoShortDescription(ComponentBase):
    _button = 'xpath=.//a[contains(@class,"btn")]'

    @property
    def text(self):
        return self._get_webelement_text(we=self._we, timeout=2)

    @property
    def has_3_lines(self):
        return self.css_property_value('-webkit-line-clamp') == '3'

    def has_button(self, timeout=1, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._button, context=self._we,
                                                   timeout=0) is not None,
            name=f'Button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class PromotionsSection(EventGroup):
    _more_info_button = 'xpath=.//*[@data-crlat="moreInfo"]'
    _short_description = 'xpath=.//*[@data-crlat="shortDescription"]'
    _image = 'xpath=.//*[@data-crlat="uriMedium"]'
    _name = 'xpath=.//*[@data-crlat="promotion.title"]'

    @property
    def name(self):
        return self._get_webelement_text(selector=self._name)

    @property
    def more_info_button(self):
        return ButtonBase(selector=self._more_info_button, context=self._we)

    @property
    def short_description(self):
        return PromoShortDescription(selector=self._short_description, context=self._we)

    @property
    def image(self):
        return self._find_element_by_selector(selector=self._image, timeout=2)

    def has_image(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._image,
                                                   timeout=0) is not None,
            name=f'Image status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)

    def has_more_info(self, timeout=2, expected_result=True):
        return wait_for_result(
            lambda: self._find_element_by_selector(selector=self._more_info_button,
                                                   timeout=0) is not None,
            name=f'More info button status to be "{expected_result}"',
            expected_result=expected_result,
            timeout=timeout)


class PromoTabContent(TabContent):
    _item = 'xpath=.//*[@data-crlat="promotion"]'
    _list_item_type = PromotionsSection

    def _wait_active(self, timeout=15):
        try:
            self._find_element_by_selector(selector=self._item, context=self._context,
                                           bypass_exceptions=(NoSuchElementException,))
        except StaleElementReferenceException:
            self._we = self._find_myself()


class Promotions(SportRacingPageBase):
    _url_pattern = r'^http[s]?:\/\/.+\/promotions'
    _tab_content_type = PromoTabContent
    _tabs_menu = 'xpath=.//*[@data-crlat="panel.tabs"]'
    _tabs_menu_type = TabsMenu
    _breadcrumbs = 'xpath=.//*[@data-crlat="breadcrumbsContainer"]'
    _breadcrumbs_type = Breadcrumbs

    def _wait_active(self, timeout=5):
        self._we = self._find_myself()
        try:
            self._find_element_by_selector(selector=self._tab_content, bypass_exceptions=(NoSuchElementException,),
                                           timeout=timeout)
        except StaleElementReferenceException:
            self._logger.debug('*** Overriding StaleElementReferenceException in %s' % self.__class__.__name__)
            self._we = self._find_myself()

    @property
    def breadcrumbs(self):
        return self._breadcrumbs_type(selector=self._breadcrumbs, context=self._we)
