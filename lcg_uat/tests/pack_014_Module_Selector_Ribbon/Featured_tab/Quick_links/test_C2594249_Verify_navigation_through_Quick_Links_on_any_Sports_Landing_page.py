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
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C2594249_Verify_navigation_through_Quick_Links_on_any_Sports_Landing_page(BaseFeaturedTest):
    """
    TR_ID: C2594249
    NAME: Verify navigation through Quick Links on any Sports Landing page
    DESCRIPTION: This test case verifies navigation through Quick Links on any Sport landing page
    """
    keep_browser_open = True
    quick_link_names = ['Autotest ' + Faker().city() for _ in range(0, 3)]

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst

        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1. Go to CMS and configure active Quick link for current Time period for any <Sport name> landing page
        PRECONDITIONS: 2. Load oxygen application and navigate to first <Sport name> landing page.
        PRECONDITIONS: <Sport name> - any sport with following tabs: "Matches", "Events", "Fights" available in oxygen application
        PRECONDITIONS: Design for Coral(now its matching Ladbrokes, i.e. quick links are stacked in a vertical list): https://jira.egalacoral.com/browse/BMA-52016
        PRECONDITIONS: **After BMA-57288** QL designs will be using grid layout:
        PRECONDITIONS: https://app.zeplin.io/project/5d35b6cdddc2c6b23c97d022?seid=5f6b29fe592de41478c4667b
        PRECONDITIONS: https://app.zeplin.io/project/5b2bb55ca6aa69a10d44e4e9/dashboard?seid=5e5d0dd9898f0b6861bce496
        """
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')

        football_page_id = {'football': self.ob_config.backend.ti.football.category_id}
        if self.is_quick_link_disabled_for_sport_category(sport_id=football_page_id.get('football')):
            raise CmsClientException('"Quick links" module is disabled for football')

        self.navigate_to_page(name='sport/football')
        self.site.wait_content_state(state_name='football')
        date_from = self.get_current_time()
        self.cms_config.create_quick_link(title=self.quick_link_names[1],
                                          sport_id=football_page_id.get('football'), date_from=date_from)

    def test_001_verify_navigation_to_other_links_by_swiping_updown(self):
        """
        DESCRIPTION: Verify navigation to other links by swiping up/down.
        EXPECTED: * Quick links are displayed as raws in the list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        EXPECTED: * User is able to navigate to the other quick links by swiping up/down.
        EXPECTED: **After BMA-57288** QL designs will be using grid layout
        """
        self.wait_for_quick_link(name=self.quick_link_names[1], delimiter='42/16,')
        self.verify_quick_link_displayed(name=self.quick_link_names[1], page_name='football')
