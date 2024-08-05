from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from voltron.pages.shared.components.aem_banner_section import AEMBannerSection
from voltron.pages.shared.components.banner_section import BannerSection
from voltron.pages.shared.components.byb_widget import BYBContainer
from voltron.pages.shared.components.home_page_components.desktop.base_desktop_module import BaseDesktopModule
from voltron.pages.shared.components.home_page_components.desktop.desktop_home_modules import DesktopHomeModules
from voltron.pages.shared.components.home_page_components.home_page_byb_tab import BYBTabContent
from voltron.pages.shared.components.home_page_components.home_page_coupons_tab import HomePageCouponsTabContent
from voltron.pages.shared.components.home_page_components.home_page_enhanced_multiples_tab import \
    EnhancedMultiplesTabContent
from voltron.pages.shared.components.home_page_components.home_page_featured_tab import HomePageFeaturedTabContent
from voltron.pages.shared.components.home_page_components.home_page_inplay_tab import HomeInPlayTabContent
from voltron.pages.shared.components.home_page_components.home_page_live_stream_tab import LiveStreamTabContent
from voltron.pages.shared.components.home_page_components.home_page_next_races_tab import HomePageNextRacesTabContent
from voltron.pages.shared.components.home_page_components.home_page_private_markets_tab import PrivateMarketsTabContent
from voltron.pages.shared.components.home_page_components.home_page_top_bets_tab import TopBetsTabContent
from voltron.pages.shared.components.menu_carousel import MenuCarousel
from voltron.pages.shared.components.module_selection_ribbon import ModuleSelectionRibbon
from voltron.pages.shared.components.offer_section import OffersSection
from voltron.pages.shared.contents.base_content import BaseContent
from voltron.pages.shared.contents.inplay_watchlive import InPlayWatchLiveTabContent
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.pages.ladbrokes.contents.base_contents.racing_base_components.next_races import LadbrokesNextRaces


class HomePage(BaseContent):
    _module_selection_ribbon = 'xpath=.//*[@data-crlat="moduleRibbon"]'
    _back_button = 'xpath=.//*[@data-crlat="btnBack"]'
    _aem_banner_section = 'xpath=.//*[@data-crlat="bannersSection"] | .//*[@data-crlat="sectionBanner"]'
    _offers_section = 'xpath=.//offers//section'
    _menu_carousel = 'xpath=.//*[@data-uat="mainNav"]'
    _local_spinner = 'xpath=.//*[not(contains(@class, "container-inner-content")) and contains(@data-crlat, "spinner.loader") or contains(@class, "spinner-loader")]'

    _tab_content = 'xpath=.//*[contains(@data-crlat, "tab.show")][*]'
    _next_races_tab_content = 'tag=next-races-home-tab'
    _tab_content_featured_type = HomePageFeaturedTabContent
    _tab_content_in_play_type = HomeInPlayTabContent
    _tab_content_live_stream_type = LiveStreamTabContent
    _tab_content_enhanced_multiples_type = EnhancedMultiplesTabContent
    _tab_content_coupons_type = HomePageCouponsTabContent
    _tab_content_top_bets_type = TopBetsTabContent
    _tab_content_private_markets_type = PrivateMarketsTabContent
    _tab_content_byb_type = BYBTabContent
    _tab_content_next_races_type = HomePageNextRacesTabContent
    _tab_content_watch_live_type = InPlayWatchLiveTabContent
    _bet_button = 'xpath=.//*[@data-crlat="oddsPrice"]'
    _acca_bet_button = 'xpath=//button[@class="btn-bet"]//span[@data-crlat="oddsPrice"]'
    _acca_price_bar = 'xpath=//*[@id="footer"]/div/acca-notification/div'
    _acca_price_bar_bettype = 'xpath=//*[@id="footer"]/div/acca-notification/div/span[@data-crlat="betType"]'
    _acca_price_bar_price = 'xpath=//*[@id="footer"]/div/acca-notification/div/span[@data-crlat="accaPrice"]'
    _next_races = LadbrokesNextRaces
    _byb_widget_container = 'xpath=.//*[@data-crlat="byb-widget-container"]'
    _byb_widget_container_type = BYBContainer

    @property
    def has_byb_widget(self):
        return self._find_element_by_selector(selector=self._byb_widget_container, timeout=1) is not None

    @property
    def byb_widget(self):
        return self._byb_widget_container_type(selector=self._byb_widget_container, context=self._we)

    @property
    def next_races(self):
        return self._next_races(selector=self._selector, web_element=self._we)

    @property
    def bet_buttons(self):
        return self._find_elements_by_selector(selector=self._bet_button, context=self._we)

    @property
    def acca_bet_buttons(self):
        return self._find_elements_by_selector(selector=self._acca_bet_button, context=self._we)

    @property
    def acca_price_bar(self):
        return self._find_element_by_selector(selector=self._acca_price_bar, context=self._we, timeout=3)

    @property
    def acca_price_bar_bettype(self):
        return self._find_element_by_selector(selector=self._acca_price_bar_bettype, context=self._we, timeout=3)

    @property
    def acca_price_bar_price(self):
        return self._find_element_by_selector(selector=self._acca_price_bar_price, context=self._we, timeout=3)

    def _wait_active(self, timeout=0):
        try:
            self._find_element_by_selector(selector=self._tab_content, context=self._context,
                                           bypass_exceptions=(NoSuchElementException,), timeout=2)
        except StaleElementReferenceException:
            self._logger.debug('*** Overriding StaleElementReferenceException in %s' % self.__class__.__name__)
            self._we = self._find_myself()

    @property
    def menu_carousel(self):
        return MenuCarousel(selector=self._menu_carousel, context=self._we)

    @property
    def module_selection_ribbon(self):
        return ModuleSelectionRibbon(selector=self._module_selection_ribbon, context=self._we, timeout=1)

    @property
    def back_button(self):
        raise VoltronException('There is no Back button on Home page')

    def back_button_click(self):
        raise VoltronException('There is no Back button on Home page')

    @property
    def banner_section(self):
        return BannerSection(selector=self._aem_banner_section, context=self._we, timeout=10)

    @property
    def has_aem_banners(self):
        return self._find_element_by_selector(selector=self._aem_banner_section, timeout=1) is not None

    @property
    def aem_banner_section(self):
        return AEMBannerSection(selector=self._aem_banner_section, timeout=10)

    @property
    def offers(self):
        return OffersSection(selector=self._offers_section)

    @property
    def tabs_menu(self):
        return self.module_selection_ribbon.tab_menu

    @property
    def _tab_content_attribute_types(self) -> dict:
        return {
            'tab.showFeaturedContent': self._tab_content_featured_type,
            'tab.showInPlayModule': self._tab_content_in_play_type,
            'tab.showInplay': self._tab_content_in_play_type,
            'tab.showWatchLiveContent': self._tab_content_live_stream_type,
            'tab.showEnhancedMultiplesModule': self._tab_content_enhanced_multiples_type,
            'tab.showEnhancedMultiples': self._tab_content_enhanced_multiples_type,
            'tab.showCouponsModule pageContainer': self._tab_content_coupons_type,
            'tab.showTopBetsModule': self._tab_content_top_bets_type,
            'tab.showPrivateMarketsModule': self._tab_content_private_markets_type,
            'tab.showBYB': self._tab_content_byb_type
        }

    @property
    def _tab_content_type(self):
        tab_content_attribute = self._find_element_by_selector(selector=self._tab_content, timeout=1)
        if not tab_content_attribute:
            if self._find_element_by_selector(selector=self._next_races_tab_content, timeout=1):
                return self._tab_content_next_races_type
            self._logger.warning('*** As template type is not recognized suppose it is Featured Tab')
            tab_content_type = self._tab_content_featured_type
        else:
            tab_content_type = self._tab_content_attribute_types[tab_content_attribute.get_attribute('data-crlat')]
            self._logger.debug(
                '*** Recognized "%s" type on "%s"' % (tab_content_type.__name__, self.__class__.__name__))
        return tab_content_type

    @property
    def tab_content(self):
        self._spinner_wait()
        if self._tab_content_type == self._tab_content_next_races_type:
            return self._tab_content_next_races_type(selector=self._next_races_tab_content, context=self._we)
        return self._tab_content_type(selector=self._tab_content, context=self._we)

    def get_module_content(self, module_name: str):
        if self.tabs_menu.current != module_name:
            self.tabs_menu.click_button(module_name, timeout=0)
            if not wait_for_result(lambda: self.tabs_menu.current == module_name,
                                   name=f'Tab: "{module_name}" to become active"',
                                   timeout=5,
                                   bypass_exceptions=(
                                   NoSuchElementException, StaleElementReferenceException, VoltronException)):
                raise VoltronException(f'"{module_name}" is not selected after click')
        return self.tab_content


class HomePageDesktop(HomePage):

    @property
    def tab_content(self):
        raise NotImplementedError(
            'Tab content cannot be used for Desktop homepage. Please use get_module_content() instead')

    @property
    def desktop_modules(self):
        return DesktopHomeModules(web_element=self._we)

    def get_module_content(self, module_name: str):
        module = self.desktop_modules.items_as_ordered_dict.get(module_name)
        if isinstance(module, BaseDesktopModule):
            return module.tab_content
        raise VoltronException('Desktop Module "%s" was not found' % module_name)
