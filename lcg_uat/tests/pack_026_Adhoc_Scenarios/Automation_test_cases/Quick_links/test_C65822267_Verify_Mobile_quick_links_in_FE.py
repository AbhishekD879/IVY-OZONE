import pytest
import tests
from faker import Faker
from datetime import datetime
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from crlat_cms_client.utils.date_time import get_date_time_as_string

from voltron.utils.exceptions.failure_exception import TestFailure
from voltron.utils.waiters import wait_for_haul


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.adhoc_suite
@pytest.mark.hl
@pytest.mark.cms
@pytest.mark.mobile_only
@pytest.mark.quick_links
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C65822267_Verify_Mobile_quick_links_in_FE(BaseFeaturedTest):
    """
    TR_ID: C65822267
    NAME: Verify Mobile quick links in FE
    DESCRIPTION: - The objective of this test cases is to validate quick link in FE which is created in CMS
    DESCRIPTION: **Note :** Mobile Quick links are applicable only for mobile apps and web but not for desktop view.
    For desktop, we have other test case.
    PRECONDITIONS: - create quick link test case must execute before this test case
    PRECONDITIONS: - https://ladbrokescoral.testrail.com/index.php?/cases/view/65783512
    """
    keep_browser_open = True
    device_name = tests.mobile_default
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'
    now = datetime.now()
    time_format = '%Y-%m-%dT%H:%M:%S.%f'
    date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                        days=-1,
                                        minutes=-1)[:-3] + 'Z'
    date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,days=1,
                                      minutes=40)[:-3] + 'Z'

    def navigate_to_homepage(self):
        """
        This method navigates to Homepage and checks if the Featured tab selected
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Home')

    def verify_redirection_from_quick_link(self):
        """
        This method checks redirection from Quick link
        """
        self.site.wait_content_state('football')
        current_url = self.device.get_current_url()
        self.assertEqual(current_url, self.destination_url,
                         msg=f'Current url: "{current_url}" is not the same as expected: "{self.destination_url}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Configure 1 active Quick link for Homepage
        DESCRIPTION: Load Oxygen application and navigate to Featured tab
        """
        if not self.is_quick_links_enabled():
            self.cms_config.update_system_configuration_structure(config_item='Sport Quick Links',
                                                                      field_name="enabled",
                                                                      field_value=True)
        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})
        if not sport_quick_links:
            sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')
        if not sport_quick_links.get('maxAmount'):
            raise CmsClientException('Max number of quick links is not configured in CMS')
        self.__class__.cms_number_of_quick_links = int(sport_quick_links['maxAmount'])
        if self.cms_number_of_quick_links <=1:
            raise CmsClientException(f'"Quick links" module max count is only "{self.cms_number_of_quick_links}"for homepage as required more than 1 ')
        self.__class__.quick_link_names = ['Auto' + Faker().city() for _ in range(2)]

        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        self.cms_config.create_quick_link(title=self.quick_link_names[0],
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=self.date_from, date_to=self.date_to)

    def test_001_launch_chrome_browseraccess_ladbrokes_url_in_mobile_viewenv_must_be_sync_with_test_case_65783512(self):
        """
        DESCRIPTION: Launch Chrome browser
        DESCRIPTION: Access Ladbrokes url in mobile view
        DESCRIPTION: Env must be sync with test case 65783512
        EXPECTED: Ladbrokes application should be loaded in mobile view
        """
        self.navigate_to_homepage()
        self.device.refresh_page()
        for i in range(5):
            try:
                self.verify_quick_link_displayed(name=self.quick_link_names[0])
                break
            except TestFailure:
                self.device.refresh_page()
                wait_for_haul(10)
        else:
            self.verify_quick_link_displayed(name=self.quick_link_names[0])
    def test_002_verify_home_page_module_order_in_fe(self):
        """
        DESCRIPTION: Verify home page module order in FE
        EXPECTED: Home page module should be displayed in below order
        EXPECTED: vanilla header
        EXPECTED: sports ribbon
        EXPECTED: Banners
        EXPECTED: Module ribbon tab
        EXPECTED: banners (Fanzone, freeride etc. ) if active
        EXPECTED: Super button if created and active
        EXPECTED: quick links (As per test case 65783512 )
        """
        sports_ribbon = self.site.home.menu_carousel.items_as_ordered_dict
        self.assertTrue(sports_ribbon, msg='Sports Menu Ribbon does not have any items')
        module_ribbon_tab = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
        self.assertTrue(module_ribbon_tab, msg=f'Module ribbon tab is not displayed')
        self.__class__.quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(self.quick_links, msg='No Quick links found on the page')
        banners = self.site.home.aem_banner_section.items_as_ordered_dict
        self.assertTrue(banners, msg=f'Banners is not Displayed')

    def test_003_read_the_active_quick_links_in_cms_as_per_test_case_65783512_step7(self):
        """
        DESCRIPTION: read the active quick links in CMS as per test case 65783512 step7
        EXPECTED: active quick links should store in temp variable
        """
        self.__class__.quick_link = self.quick_links.get(self.quick_link_names[0])

    def test_004_verify_quick_link_display_in_fe_which_are_active_in_cms(self):
        """
        DESCRIPTION: Verify quick link display in FE which are active in CMS
        EXPECTED: All the active quick links should display in FE
        EXPECTED: If there is only one active QL should display in List view
        EXPECTED: If there are even no of active QLs, those should display in grid view
        EXPECTED: if there are odd no of quick links greater than 1, first even no of QL should display in grid
        view and other one should display in list view
        EXPECTED: for e.g. if there are 5 active quick links, first 4 should display in grid
        view and other one should display in list view
        """
        self.assertTrue(self.quick_link, msg=f'Quick link "{self.quick_link_names[0]}" not found')
        self.quick_link.click()
        self.verify_redirection_from_quick_link()
        self.cms_config.create_quick_link(title=self.quick_link_names[1],
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=self.date_from, date_to=self.date_to
                                          )
        self.navigate_to_homepage()
        self.device.refresh_page()
        self.verify_quick_link_displayed(name=self.quick_link_names[0])
        for i in range(5):
            try:
                self.verify_quick_link_displayed(name=self.quick_link_names[1])
                break
            except TestFailure:
                self.device.refresh_page()
                wait_for_haul(10)
        else:
            self.verify_quick_link_displayed(name=self.quick_link_names[1])
        actual_quick_links = []
        fe_quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(fe_quick_links, msg='No Quick links found on the page')
        for quick_link in fe_quick_links:
            actual_quick_links.append(quick_link.upper().strip())
        expected_quick_links = []
        cms_quick_links = self.cms_config.get_quick_links(sport_id=self.homepage_id.get('homepage'))
        for cms_quick_link in cms_quick_links:
            if (cms_quick_link['validityPeriodStart'] <= datetime.utcnow().isoformat() <= cms_quick_link['validityPeriodEnd']) and cms_quick_link['disabled'] is False:
                expected_quick_links.append(cms_quick_link['title'].upper().strip())
        for fe_ql_name in expected_quick_links:
            status = next((True for ql_name in actual_quick_links if
                           ql_name == fe_ql_name or (ql_name[-3:] == '...' and fe_ql_name[:len(ql_name) - 3] + '...' == ql_name)),
                          False)
            self.assertTrue(status,
                             msg=f'Actual Quicklink from frontend:"{fe_ql_name}" are not in expected Quicklink from CMS:{expected_quick_links}')
