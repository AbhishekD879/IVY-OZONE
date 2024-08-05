import time
import tests
import pytest
import datetime
from crlat_cms_client.utils.date_time import get_date_time_as_string
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from faker import Faker
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create eventhub in prod/beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C9726400_Event_Hub_Expired_Quick_links(BaseFeaturedTest):
    """
    TR_ID: C9726400
    NAME: Event Hub: Expired Quick links
    DESCRIPTION: This test case verifies expiration of Quick links on Event Hub
    PRECONDITIONS: 1. Go to CMS -> Sport Pages->Event Hub -> Quick Links and configure a Quick link for Event Hub with Validity period End Date=current time +10 minutes. - (<Quick Link1>)
    PRECONDITIONS: 2. There should be no other active Quick links for Event Hub expect <Quick Link1>.
    PRECONDITIONS: 3. Go to Oxygen app and navigate to Event hub tab.
    PRECONDITIONS: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    """
    keep_browser_open = True
    quick_link_name = 'autotest ' + Faker().city()
    quick_link_name2 = 'auto2 ' + Faker().city()
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'

    def test_000_preconditions(self):
        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})
        if not sport_quick_links:
            sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')
        if not sport_quick_links.get('maxAmount'):
            raise CmsClientException('Max number of quick links is not configured in CMS')
        self.__class__.cms_number_of_quick_links = int(sport_quick_links['maxAmount'])

        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')

        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        self.__class__.index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=self.index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='QUICK_LINK')
        self.__class__.time_format = '%Y-%m-%dT%H:%M:%S.%f'
        fromdate = datetime.datetime.now() - datetime.timedelta(days=1)
        todate = datetime.datetime.now() + datetime.timedelta(minutes=1, seconds=40)
        ql_date_from = get_date_time_as_string(date_time_obj=fromdate, time_format=self.time_format, url_encode=False)[:-3] + 'Z'
        date_to = get_date_time_as_string(date_time_obj=todate, time_format=self.time_format, url_encode=False)[:-3] + 'Z'
        self.cms_config.create_quick_link(title=self.quick_link_name,
                                          sport_id=self.index_number,
                                          destination=self.destination_url,
                                          page_type='eventhub',
                                          date_from=ql_date_from, date_to=date_to)

        internal_id = f'tab-eventhub-{self.index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=self.index_number,
                                                                           display_date=True)

        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_verify_displaying_if_configured_quick_link_is_not_displayed_on_event_hub_tab(self):
        """
        DESCRIPTION: Verify displaying if configured Quick link is not displayed on Event Hub tab.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick link is displayed.
        """
        self.site.wait_content_state('homepage')
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No "Quick Links" present')
        self.verify_quick_link_displayed(name=self.quick_link_name)

    def test_002_go_to_cms___sport_pages_event_hub___quick_links_and_create_the_second_active_quick_link_with_validity_period_end_datecurrent_time_plus20_minutes_quick_link2(
            self):
        """
        DESCRIPTION: Go to CMS -> Sport Pages->Event Hub -> Quick Links and create the second active Quick link with Validity period End Date=current time +20 minutes. (<Quick Link2>)
        EXPECTED:
        """
        fromdate = datetime.datetime.now() - datetime.timedelta(days=1)
        todate = datetime.datetime.now() + datetime.timedelta(minutes=2, seconds=15)
        date_from = get_date_time_as_string(date_time_obj=fromdate, time_format=self.time_format, url_encode=False)[:-3] + 'Z'
        date_to = get_date_time_as_string(date_time_obj=todate, time_format=self.time_format, url_encode=False)[:-3] + 'Z'
        self.cms_config.create_quick_link(title=self.quick_link_name2,
                                          sport_id=self.index_number,
                                          destination=self.destination_url,
                                          page_type='eventhub',
                                          date_from=date_from,
                                          date_to=date_to)

    def test_003_go_to_oxygen_app_and_navigate_to_event_hub_tabverify_that_configured_quick_links_are_displayed_on_event_hub(
            self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Event Hub tab.
        DESCRIPTION: Verify that configured Quick links are displayed on Event Hub.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * Configured Quick Links are displayed.
        """
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No "Quick Links" present')
        quick_links.get(self.quick_link_name2)
        self.verify_quick_link_displayed(name=self.quick_link_name2)

    def test_004_wait_forquick_link1_to_get_expired_in_10_minutes(self):
        """
        DESCRIPTION: Wait for<Quick Link1> to get expired (in 10 minutes)
        EXPECTED:
        """
        self._logger.info(f'*** Waiting for 60 seconds to get expired Quick Link with name "{self.quick_link_name}"')
        time.sleep(80)

    def test_005_go_to_oxygen_app_and_navigate_to_event_hub_tabverify_that_configured_quick_link1_is_not_displayed_on_event_hub(
            self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Event Hub tab.
        DESCRIPTION: Verify that configured <Quick Link1> is not displayed on Event hub.
        EXPECTED: * Quick links container is displayed.
        EXPECTED: * <Quick Link1> is not displayed.
        EXPECTED: * <Quick Link2> is displayed
        """
        self.device.refresh_page()
        self.site.wait_content_state('homepage')
        self.site.home.get_module_content(self.event_hub_tab_name)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No "Quick Links" present')
        self.verify_quick_link_displayed(name=self.quick_link_name2)
        self.verify_quick_link_displayed(name=self.quick_link_name, expected_result=False)

    def test_006_wait_for_quick_link2_to_get_expired_in_20_minutes(self):
        """
        DESCRIPTION: Wait for <Quick Link2> to get expired (in 20 minutes)
        EXPECTED:
        """
        self._logger.info(f'*** Waiting for 60 seconds to get expired Quick Link with name "{self.quick_link_name2}"')
        time.sleep(30)

    def test_007_go_to_oxygen_app_and_navigate_to_event_hub_tabverify_that_configured_quick_link2_is_not_displayed_on_event_hub(
            self):
        """
        DESCRIPTION: Go to Oxygen app and navigate to Event Hub tab.
        DESCRIPTION: Verify that configured <Quick Link2> is not displayed on Event Hub
        EXPECTED: * Quick links container is not displayed.
        EXPECTED: * No Quick links are displayed.
        """
        self.device.refresh_page()
        self.site.wait_content_state('homepage')
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        sections = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertFalse(sections, msg='No "Quick Links" present')
        self.verify_quick_link_displayed(name=self.quick_link_name2, expected_result=False)
