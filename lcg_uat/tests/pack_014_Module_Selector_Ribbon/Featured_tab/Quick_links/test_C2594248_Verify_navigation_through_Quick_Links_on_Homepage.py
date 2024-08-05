import tests
import pytest
import time
from datetime import datetime
from faker import Faker
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # we can not create quick links on prod
# @pytest.mark.hl
@pytest.mark.cms
@pytest.mark.mobile_only
@pytest.mark.quick_links
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C2594248_Verify_navigation_through_Quick_Links_on_Homepage(BaseFeaturedTest):
    """
    TR_ID: C2594248
    NAME: Verify navigation through Quick Links on Homepage
    DESCRIPTION: This test case verifies navigation through Quick Links on Homepage
    PRECONDITIONS: 1. Go to CMS -> Sport Pages->Homepage and configure active Quick link for current Time period on Homepage
    PRECONDITIONS: 2. Load oxygen application and navigate to Featured tab
    PRECONDITIONS: Design for Coral (now its matching Ladbrokes, i.e. quick links are stacked in a vertical list): https://jira.egalacoral.com/browse/BMA-52016
    PRECONDITIONS: **After BMA-57288** QL designs will be using grid layout:
    PRECONDITIONS: https://app.zeplin.io/project/5d35b6cdddc2c6b23c97d022?seid=5f6b29fe592de41478c4667b
    PRECONDITIONS: https://app.zeplin.io/project/5b2bb55ca6aa69a10d44e4e9/dashboard?seid=5e5d0dd9898f0b6861bce496
    """
    keep_browser_open = True
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst

        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def navigate_to_homepage_featured_tab(self):
        """
        This method navigates to Homepage and checks if the Featured tab selected
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Home')

        selected_tab = self.site.home.module_selection_ribbon.tab_menu.current
        self.assertEqual(selected_tab, self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured),
                         msg=f'Selected tab is: "{selected_tab}" '
                         f'instead of: "{self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured)}"')

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
        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})
        if not sport_quick_links:
            sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')
        if not sport_quick_links.get('maxAmount'):
            raise CmsClientException('Max number of quick links is not configured in CMS')
        cms_number_of_quick_links = int(sport_quick_links['maxAmount'])
        self.__class__.quick_link_names = ['Autotest ' + Faker().city() for _ in range(0, cms_number_of_quick_links)]

        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        date_from = self.get_current_time()
        self.cms_config.create_quick_link(title=self.quick_link_names[0],
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from)
        self.navigate_to_homepage_featured_tab()

    def test_001_verify_navigation_to_other_links_by_swiping_updown(self):
        """
        DESCRIPTION: Verify navigation to other links by swiping up/down.
        EXPECTED: * Quick links are displayed as fixed vertical list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        EXPECTED: * User is able to navigate to the other quick links by swiping up/down.
        EXPECTED: **After BMA-57288** QL designs will be using grid layout
        """
        self.wait_for_quick_link(name=self.quick_link_names[0])
        self.verify_quick_link_displayed(name=self.quick_link_names[0])
