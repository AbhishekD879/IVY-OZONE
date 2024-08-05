import pytest
from faker import Faker

import tests
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


# @pytest.mark.prod # we can not create quick links on prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.hl
@pytest.mark.cms
@pytest.mark.module_ribbon
@pytest.mark.quick_links
@pytest.mark.mobile_only
@pytest.mark.featured
@pytest.mark.high
@vtest
class Test_C2543779_Verify_adding_removing_Quick_links_on_Homepage(BaseFeaturedTest):
    """
    TR_ID: C2543779
    VOL_ID: C43885004
    NAME: Verify adding/removing Quick links on Homepage
    DESCRIPTION: This test case verifies adding of Quick links to Homepage and All Sports Landing pages
    PRECONDITIONS: 1. There should be no active Quick links for Homepage in CMS
    PRECONDITIONS: 2. Go to Oxygen app and navigate to Homepage.
    PRECONDITIONS: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    """
    keep_browser_open = True
    sport_id = {'homepage': 0}
    quick_link_name = 'autotest ' + Faker().city()
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'
    quick_link_object = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Quick links module is enabled in CMS
        DESCRIPTION: Go to CMS -> Sport Pages->Homepage -> Quick Links and configure one Quick Link for Homepage
        """
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.sport_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        self.__class__.quick_link_object = self.cms_config.create_quick_link(title=self.quick_link_name,
                                                                             sport_id=self.sport_id.get('homepage'),
                                                                             destination=self.destination_url)

    def test_001_verify_displaying_of_quick_link_container(self):
        """
        DESCRIPTION: Verify displaying of Quick link container
        EXPECTED: * Quick links container is not displayed
        EXPECTED: * No Quick Links are displayed
        """
        # Can not automate. We don't disable/remove existing Quick Link module.

    def test_002_go_to_oxygen_application_and_navigate_to_featured_tab_verify_that_configured_quick_link_is_displayed(self):
        """
        DESCRIPTION: Go to Oxygen application and navigate to Featured tab.
        DESCRIPTION: Verify that configured Quick link is displayed.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick link is displayed in Feature tab on Homepage.
        EXPECTED: * Quick link is stretched to fit the width of the screen.
        """
        selected_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(selected_tab, self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured),
                         msg=f'Selected tab is "{selected_tab}" instead of "'
                             f'{self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)}" tab')
        self.wait_for_quick_link(name=self.quick_link_name)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertIn(self.quick_link_name, quick_links,
                      msg=f'Can not find "{self.quick_link_name}" in "{quick_links}"')
        quick_links.get(self.quick_link_name).click()

    def test_003_click_anywhere_on_the_quick_linkverify_redirection_to_url_previously_configured_in_cms_within_the_application(self):
        """
        DESCRIPTION: Click anywhere on the quick link
        DESCRIPTION: Verify redirection to URL previously configured in CMS within the application
        EXPECTED: * User is redirected to specific page(URL) previously configured in Quick link CMS configuration.
        EXPECTED: * Page is opened within the application.
        """
        self.site.wait_content_state('football')
        current_url = self.device.get_current_url()

        self.assertEqual(current_url, self.destination_url,
                         msg=f'Current url "{current_url}" is not equal to expected "{self.destination_url}"')

    def test_004_select_any_other_tab_on_homepage_in_play_coupons_next_races_build_your_bet_etcverify_displaying_of_quick_links_on_other_tabs(self):
        """
        DESCRIPTION: Select any other tab on Homepage(In-Play, Coupons, Next races, Build your bet, etc.)
        DESCRIPTION: Verify displaying of Quick links on other tabs.
        EXPECTED: * Configured Quick links are displayed only on Featured tab.
        EXPECTED: * Quick links container is NOT displayed on other Homepage tabs.
        EXPECTED: * Configured Quick links are NOT displayed on other Homepage tabs.
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('Homepage')
        inplay_featured_tab_name = self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.in_play)
        self.site.home.module_selection_ribbon.tab_menu.click_button(inplay_featured_tab_name)
        if self.site.home.tab_content.has_quick_links(timeout=5):
            quick_links = self.site.home.tab_content.quick_links
            self.assertNotIn(self.quick_link_name, quick_links.keys(),
                             msg=f'Quick links module {self.quick_link_name} is shown '
                                 f'on Homepage {inplay_featured_tab_name} tab')

    def test_005_go_to_any_sport_page_eg_football_tennis_and_observe_quick_links_sectionverify_displaying_of_homepage_configured_quick_link_on_any_sport_landing_page(self):
        """
        DESCRIPTION: Go to any Sport page (e.g. Football, Tennis) and observe Quick links section.
        DESCRIPTION: Verify displaying of Homepage configured Quick link on any Sport landing page
        EXPECTED: * Configured Quick link for Homepage is not displayed on other Sport pages.
        EXPECTED: **Only quick links that are configured for Sport landing page are shown (if there are any).
        EXPECTED: **Quick links container and links are not displayed If no quick links are configured for Sport pages.
        """
        # suprise, suprise! pages can have quick links added by someone else
        self.navigate_to_page(name='horse-racing')
        self.site.wait_content_state('Horseracing')
        tab_content = self.site.horse_racing.tab_content
        if tab_content.has_quick_links(timeout=5):
            quick_links = tab_content.quick_links.items_as_ordered_dict
            self.assertNotIn(self.quick_link_name, quick_links.keys(),
                             msg=f'Found quick link "{self.quick_link_name}" created for Homepage in "{quick_links}" on Horseracing page')

        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state('basketball')
        tab_content = self.site.basketball.tab_content
        if tab_content.has_quick_links(timeout=5):
            quick_links = tab_content.quick_links.items_as_ordered_dict
            self.assertNotIn(self.quick_link_name, quick_links.keys(),
                             msg=f'Found quick link "{self.quick_link_name}" created for Homepage in "{quick_links}" on Basketball page')

    def test_006_go_to_cms_sport_pages_homepage_quick_links_and_set_active_inactive_flag_for_configured_quick_link_for_homepage_to_inactive(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages->Homepage -> Quick Links and set "Active/ Inactive" flag for configured quick link for Homepage to 'Inactive'.
        """
        self.cms_config.change_quick_link_state(active=False, quick_link_object=self.quick_link_object)

    def test_007_go_to_oxygen_app_and_navigate_to_featured_tab_on_homepage_verify_that_quick_link_is_no_longer_displayed(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Featured tab on Homepage.
        DESCRIPTION: Verify that Quick link is no longer displayed.
        EXPECTED: * Quick links container is not displayed.
        EXPECTED: * Quick link is no longer displayed.
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state('Homepage')
        self.wait_for_quick_link(name=self.quick_link_name, expected_result=False, timeout=10)
        self.verify_quick_link_displayed(name=self.quick_link_name, expected_result=False)

    def test_008_go_to_cms_sport_pages_homepage_quick_links_and_set_active_inactive_flag_for_configured_quick_link_for_homepage_to_active(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages->Homepage -> Quick Links and set "Active/ Inactive" flag for configured quick link for Homepage to 'Active'.
        """
        self.cms_config.change_quick_link_state(active=True, quick_link_object=self.quick_link_object)

    def test_009_go_to_oxygen_app_and_navigate_to_featured_on_homepage_verify_that_quick_link_is_displayed(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Featured on Homepage.
        DESCRIPTION: Verify that Quick link is displayed.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick link is displayed on Homepage.
        EXPECTED: * Quick link is stretched to fit the width of the screen.
        """
        self.site.wait_content_state('Homepage')
        self.wait_for_quick_link(name=self.quick_link_name)
        self.verify_quick_link_displayed(name=self.quick_link_name)

    def test_010_go_to_cms_sport_pages_homepage_quick_links_and_remove_previously_created_quick_link(self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages->Homepage -> Quick Links and remove previously created Quick link
        """
        quick_link_id = self.quick_link_object.get('id')
        self.cms_config.delete_quick_link(quick_link_id=quick_link_id)
        self.cms_config._created_quick_links.remove(quick_link_id)

    def test_011_go_to_oxygen_app_and_navigate_to_featured_tab_on_homepageverify_that_quick_link_is_no_longer_displayed(self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Featured tab on Homepage.
        DESCRIPTION: Verify that Quick link is no longer displayed.
        EXPECTED: * Quick links container is not displayed.
        EXPECTED: * Quick link is no longer displayed.
        """
        self.wait_for_quick_link(name=self.quick_link_name, expected_result=False)
        self.verify_quick_link_displayed(name=self.quick_link_name, expected_result=False)
