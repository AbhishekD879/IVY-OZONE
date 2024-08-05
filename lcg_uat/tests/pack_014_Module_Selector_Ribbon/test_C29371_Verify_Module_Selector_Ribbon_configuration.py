from collections import OrderedDict

import pytest
from crlat_ob_client.utils.date_time import get_date_time_as_string
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.prod
@pytest.mark.cms
@pytest.mark.module_ribbon
@pytest.mark.homepage
@pytest.mark.low
@pytest.mark.featured
@pytest.mark.mobile_only
@pytest.mark.login
@vtest
class Test_C29371_Verify_Module_Selector_Ribbon_configuration(BaseBanachTest):
    """
    TR_ID: C29371
    VOL_ID: C9698355
    NAME: Verify Module Selector Ribbon configuration
    PRECONDITIONS: Data for 'ID' and 'URL' parameters for Module Ribbon Tabs in CMS https://confluence.egalacoral.com/display/SPI/Data+for+%27ID%27+and+%27URL%27+parameters+for+Module+Ribbon+Tabs+in+CMS
    """
    keep_browser_open = True
    tabs_cms = []
    tabs_bma = OrderedDict()
    new_tab_title = None
    new_tab_directive = 'Multiples'
    new_tab_internal_id = None
    new_tab_url = ''
    tabs_urls_cms = {}
    proxy = None

    def test_001_get_order_of_module_ribbon_tabs_on_cms_page(self):
        """
        DESCRIPTION: Get order of tabs on CMS Module Ribbon page
        EXPECTED: Ordered dictionary with tabs names created
        """
        module_ribbon_tabs = self.cms_config.module_ribbon_tabs.all_tabs_data
        self.__class__.tabs_cms = [tab['title'].upper() for tab in module_ribbon_tabs if
                                   tab['visible'] is True and tab['universalSegment'] is True and
                                   (tab['displayTo'] is None or tab['displayTo'] > get_date_time_as_string(
                                       time_format="%Y-%m-%dT%H:%M:%S"))]
        self.__class__.tabs_urls_cms = {tab['title'].upper(): tab['url'] for tab in module_ribbon_tabs}
        if self.brand == 'bma' and vec.siteserve.EXPECTED_MARKET_TABS.build_your_bet in self.tabs_cms:
            try:
                self.get_ob_event_with_byb_market()
            except SiteServeException:
                del self.tabs_cms[self.tabs_cms.index(vec.siteserve.EXPECTED_MARKET_TABS.build_your_bet)]

        self.__class__.one_two_free_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.one_two_free, raise_exceptions=False)
        if not self.one_two_free_tab_name:
            self._logger.warning(f'Can\'t found "{self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.one_two_free}"')

    def test_002_check_module_selector_ribbon(self):
        """
        DESCRIPTION: On Invictus home page check Module Selector Ribbon
        EXPECTED: Module Selector Ribbon positioned below the Promotions Banner Carousel
        EXPECTED: 'Featured' tab is selected by default ('Your Enhanced Multiples' - for logged in users who have private markets available)
        """
        self.site.login()
        module_selection_ribbon = self.site.home.module_selection_ribbon
        self.__class__.tabs_bma = module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertTrue(self.tabs_bma, msg='Cannot found tabs on Oxygen Module Selector Ribbon')
        self.assertTrue(self.tabs_bma[self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)].is_selected(),
                        msg='Featured tab is not selected by default')

    def test_003_click_on_module_ribbon_tabs_and_verify_url(self):
        """
        DESCRIPTION: Click on tabs and verify url is the same as configured in CMS
        EXPECTED: Url of each tab is the same as configured in CMS
        """
        if self.tabs_bma.get(self.one_two_free_tab_name):
            tab = self.tabs_bma.get(self.one_two_free_tab_name)
            tab.click()
            self.site.wait_content_state('1-2-free', timeout=3)
            url = self.device.get_current_url()
            expected_1_2_free_url = self.tabs_urls_cms.get(self.one_two_free_tab_name)
            self.assertIn(expected_1_2_free_url, url,
                          msg=f'Url of 1-2-FREE page on Oxygen "{expected_1_2_free_url}" '
                              f'is not the same as the one configured in CMS "{url}"')

            self.navigate_to_page('/')

        for i in reversed(range(len(self.tabs_bma.items()))):
            tabs = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(tabs, msg='Tabs are not available in module ribbon section')
            tab_name, tab = list(tabs.items())[i]
            if tab_name != self.one_two_free_tab_name:
                expected_tab_url = self.tabs_urls_cms.get(tab_name)
                tab.click()
                self.site.wait_content_state_changed()
                if "home" in expected_tab_url:
                    self.site.wait_content_state('Homepage', timeout=3)
                    current_tab = wait_for_result(lambda: self.site.home.module_selection_ribbon.tab_menu.current,
                                                  timeout=5,
                                                  name='Tab menu to be loaded',
                                                  bypass_exceptions=(
                                                      NoSuchElementException, StaleElementReferenceException,
                                                      VoltronException))
                    self.assertEqual(tab_name, current_tab,
                                     msg=f'Tab "{tab_name}" is not selected after click. Selected tab is "{current_tab}"')
                    url = self.device.get_current_url()
                    self.assertIn(expected_tab_url, url,
                                  msg=f'Url of tab on Oxygen "{expected_tab_url}" '
                                      f'is not the same as the one configured in CMS "{url}"')
                elif tab_name == "GREYHOUNDS":
                        self.site.wait_content_state('greyhound-racing')
                        current_tab = wait_for_result(lambda: self.site.greyhound.header_line.page_title.title,
                                                      timeout=5,
                                                      name='Tab menu to be loaded',
                                                      bypass_exceptions=(
                                                          NoSuchElementException, StaleElementReferenceException,
                                                          VoltronException))
                        self.assertEqual(tab_name, current_tab.upper(),
                                         msg=f'Tab "{tab_name}" is not selected after click. Selected tab is "{current_tab}"')
                        url = self.device.get_current_url()
                        self.assertIn(expected_tab_url, url,
                                      msg=f'Url of tab on Oxygen "{expected_tab_url}" '
                                          f'is not the same as the one configured in CMS "{url}"')
                self.device.go_back()
                self.site.wait_content_state("HomePage")

    def test_004_verify_order_of_tabs_on_module_selector_ribbon(self):
        """
        DESCRIPTION: Verify order of tabs on Module Selector Ribbon
        EXPECTED: Order of buttons corresponds to the order in CMS ('Module Ribbon Tabs' tab)
        """
        self.assertListEqual(list(self.tabs_bma.keys()), self.tabs_cms,
                             msg=f'List of tabs on UI \n"{list(self.tabs_bma.keys())}" '
                                 f'do not match with list of active tabs in CMS \n"{self.tabs_cms}"')

    def test_005_create_new_module_ribbon_tab(self):
        """
        DESCRIPTION: Create new module ribbon tab: Fill all required fields by correct data. Please note that 'ID' and 'URL' fields should be filled according to the selected 'Directive Name'
        DESCRIPTION: https://confluence.egalacoral.com/display/SPI/Data+for+%27ID%27+and+%27URL%27+parameters+for+Module+Ribbon+Tabs+in+CMS
        EXPECTED: New module with name containing "Autotest" is created
        """
        # note: it can only be tested by autotest on invictus + dev cms
        if 'dev' in tests.settings.cms_env:
            module_ribbon_tab = self.cms_config.module_ribbon_tabs.create_tab(directive_name=self.new_tab_directive)
            self.__class__.new_tab_title, self.__class__.new_tab_internal_id, self.__class__.new_tab_url = \
                module_ribbon_tab.title, module_ribbon_tab.internal_id, module_ribbon_tab.url

    def test_006_verify_new_tab_presence(self):
        """
        DESCRIPTION: Verify tab presence
        EXPECTED: Tab is shown
        """
        if 'dev' in tests.settings.cms_env:
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            module_selection_ribbon = self.site.home.module_selection_ribbon
            tabs = module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(tabs, msg='Cannot found tabs on Module Ribbon Selector')
            tab_title = self.new_tab_title.upper()
            self.assertTrue(tab_title in tabs.keys(),
                            msg=f'Added tab "{tab_title}" is not present on Module Ribbon tabs "{tabs.keys()}"')
