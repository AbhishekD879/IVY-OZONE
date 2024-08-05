from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
import tests
from voltron.pages.shared.components.offer_section import OffersSection
from voltron.pages.shared.components.banner_section import BannerSection
from voltron.pages.shared.components.aem_banner_section import AEMBannerSection
from voltron.pages.shared.components.grouping_buttons import GroupingSelectionButtons
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.base_contents.common_base_components.date_tab import DateTab
from voltron.pages.shared.contents.base_contents.common_base_components.sport_enhanced_multiples import \
    SportEnhancedMultiples
from voltron.utils.waiters import wait_for_result


class SportRacingPageBase(BaseContent):
    _tabs_menu = 'xpath=.//*[@data-crlat="switchers" and contains(@class, "scrollable-switchers")]'
    _tabs_menu_type = GroupingSelectionButtons
    _date_tab = 'xpath=.//*[contains(@data-crlat, "switchers") and not(contains(@class, "scrollable-switchers"))]'
    _date_tab_type = DateTab
    _banner_section = 'xpath=.//*[@data-crlat="sectionBanner"]'
    _banner_section_type = BannerSection
    _aem_banner_section = 'xpath=.//*[contains(@class, "swiper-container-horizontal")]'
    _aem_banner_section_type = AEMBannerSection
    _offers_section = 'xpath=.//*[@data-crlat="offerSlide"]'
    _offers_section_type = OffersSection
    _enhanced_multiples_carousel = 'xpath=.//*[@data-crlat="race.enhancedMultiplesCarousel"]'
    _enhanced_multiples_carousel_type = SportEnhancedMultiples
    _context_timeout = 5
    _right_arrow = 'xpath=.//*[contains(@class, "action-arrow right")]'
    _left_arrow = 'xpath=.//*[contains(@class, "action-arrow left")]'

    def _wait_active(self, timeout=_context_timeout):
        self._we = self._find_myself(timeout=timeout)
        try:
            self._find_element_by_selector(selector=self._tab_content,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=3)
            self._find_element_by_selector(selector=self._tabs_menu,
                                           bypass_exceptions=(NoSuchElementException,),
                                           timeout=1.5)
        except StaleElementReferenceException:
            self._logger.debug('*** Overriding StaleElementReferenceException in %s' % self.__class__.__name__)

    @property
    def banner_section(self):
        return self._banner_section_type(selector=self._banner_section, context=self._we, timeout=3)

    @property
    def has_aem_banners(self):
        return self._find_element_by_selector(selector=self._aem_banner_section, timeout=1) is not None

    @property
    def aem_banner_section(self):
        return self._aem_banner_section_type(context=self._we, timeout=10)

    @property
    def offers_section(self):
        return self._offers_section_type(selector=self._offers_section, context=self._we, timeout=3)

    @property
    def sport_enhanced_multiples_carousel(self):
        return self._enhanced_multiples_carousel_type(selector=self._enhanced_multiples_carousel, context=self._we, timeout=1)

    @property
    def tabs_menu(self):
        if tests.settings.brand == 'ladbrokes':
            return self._tabs_menu_type(selector=self._tabs_menu, timeout=5)
        else:
            return self._tabs_menu_type(selector=self._tabs_menu, context=self._we, timeout=5)


    def has_tabs_menu(self, expected_result=True, timeout=1):
        return wait_for_result(lambda: self._find_element_by_selector(selector=self._tabs_menu,
                                                                      timeout=0),
                               expected_result=expected_result,
                               timeout=timeout,
                               name=f'Has tabs menu status to be {expected_result}')

    @property
    def date_tab(self):
        return self._date_tab_type(selector=self._date_tab, context=self._we)

    @property
    def right_arrow(self):
        return self._find_element_by_selector(selector=self._right_arrow, timeout=1)

    @property
    def left_arrow(self):
        return self._find_element_by_selector(selector=self._left_arrow, timeout=1)

    @property
    def has_right_arrow(self):
        return self._find_element_by_selector(selector=self._right_arrow, timeout=1) is not None

    @property
    def has_left_arrow(self):
        return self._find_element_by_selector(selector=self._left_arrow, timeout=1) is not None
