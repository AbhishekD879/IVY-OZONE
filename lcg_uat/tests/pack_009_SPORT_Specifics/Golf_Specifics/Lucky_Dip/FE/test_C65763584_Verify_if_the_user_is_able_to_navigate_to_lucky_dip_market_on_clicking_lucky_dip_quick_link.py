import pytest
import tests
from tests.base_test import vtest
from datetime import datetime
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C65763584_Verify_if_the_user_is_able_to_navigate_to_lucky_dip_market_on_clicking_lucky_dip_quick_link(BaseGolfTest, BaseFeaturedTest):
    """
    TR_ID: C65763584
    NAME: Verify if the  user is able to navigate to lucky dip market on clicking lucky dip quick link
    DESCRIPTION: This test case verifies if the content user is able to navigate to lucky dip market on clicking lucky dip quick link
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Lucky Dip should be configured in CMS
    PRECONDITIONS: Lucky dip market should be configured in a Golf event
    PRECONDITIONS: Quick link with event id which has lucky dip market should be configured
    """
    keep_browser_open = True
    sport_id = {'homepage': 0}
    quick_link_title = 'Autotest_luckydip' + 'C65763584'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        # Check if Lucky Dip is enabled in CMS
        cms_config_lucky_dip = self.cms_config.get_system_configuration_item('LuckyDip')
        if len(cms_config_lucky_dip) == 0 or not cms_config_lucky_dip.get('enabled'):
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')

        # Check if Lucky Dip is enabled in OB
        all_lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        event = all_lucky_dip_events[0]
        self.__class__.eventID = event['event']['id']
        self.assertTrue(self.eventID, msg="Lucky Dip Event Not Available")

        # Creating Destination URL for quick-link
        category_name = event['event']['categoryName']
        class_name = event['event']['className']
        type_name = event['event']['typeName']
        event_name = event['event']['name']
        destination_url = f'https://{tests.HOSTNAME}/event/{category_name}/{class_name}/{type_name}/{event_name}/{self.eventID}/all-markets'

        # Check if  Quick Link Is Configured in CMS
        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.sport_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')

        # Create New quicklink with Title 'Autotest_luckydip C65763584'
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                            days=-1,
                                            minutes=-1)[:-3] + 'Z'
        date_to = get_date_time_as_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                          days=3)[:-3] + 'Z'
        self.cms_config.create_quick_link(title=self.quick_link_title,
                                          sport_id=self.sport_id.get('homepage'),
                                          destination=destination_url,
                                          date_from=date_from, date_to=date_to,
                                          )

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to ladbrokes application
        EXPECTED: User logs in successfully
        """
        # Login
        self.site.login()

    def test_002_check_whether_the_quick_link_which_is_configured_with_lucky_dip_market_is_displayed_in_fe(self):
        """
        DESCRIPTION: Check whether the quick link which is configured with lucky dip market is displayed in FE
        EXPECTED: Quick link should be displayed in FE
        """
        # Check if Autotest_luckydip C65763584 is present in quick-link(HomePage)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertIn(self.quick_link_title, list(quick_links.keys()), msg=f'Can not find "{self.quick_link_title}" in "{list(quick_links.keys())}"')

        # Pick Autotest_luckydip C65763584 Quick-Link
        self.__class__.quick_link = quick_links.get(self.quick_link_title)
        self.assertTrue(self.quick_link, msg=f'quicklink is not present in home page')

    def test_003_verify_if_the_user_is_navigated_to_lucky_dip_market_on_clicking_the_quick_link(self):
        """
        DESCRIPTION: Verify if the user is navigated to lucky dip market on clicking the quick link
        EXPECTED: User should be navigated to lucky dip market on clicking quick link
        """
        #  Click on the quick link
        self.quick_link.click()
        self.site.wait_content_state_changed()

        # Verify that the user is navigated to lucky dip market on clicking the quick link
        self.actual_url = self.device.get_current_url()
        self.assertIn(self.eventID, self.actual_url, msg=f'User is not able to navigate to LuckyDip market')


