import pytest
import tests
import datetime
from time import sleep
from faker import Faker
from tests.base_test import vtest
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # can not create quick links on prod
# @pytest.mark.hl
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9726401_Event_Hub_Verify_navigation_through_Quick_Links_on_Event_Hub(BaseFeaturedTest):
    """
    TR_ID: C9726401
    NAME: Event Hub: Verify navigation through Quick Links on Event Hub
    DESCRIPTION: This test case verifies navigation through Quick Links on Event hub
    PRECONDITIONS: 1. Go to CMS -> Sport Pages->Event Hub and configure 5 active Quick links for current Time period on Event hub in order to have more Quick links than the screen can feet.
    PRECONDITIONS: 2. Load oxygen application and navigate to Event hub tab
    PRECONDITIONS: Quick Link designs can be found here: https://jira.egalacoral.com/browse/BMA-34140
    """
    keep_browser_open = True
    homepage_id = {'homepage': 0}
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'

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
        self.__class__.cms_number_of_quick_links = int(sport_quick_links['maxAmount'])
        self.__class__.quick_link_names = ['Autotest ' + Faker().city() for _ in range(0, self.cms_number_of_quick_links)]

        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        self.__class__.index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=self.index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=self.index_number, module_type='QUICK_LINK')
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        fromdate = datetime.datetime.now() - datetime.timedelta(days=1)
        todate = datetime.datetime.now() + datetime.timedelta(minutes=1, seconds=40)
        ql_date_from = get_date_time_as_string(date_time_obj=fromdate, time_format=time_format, url_encode=False)[:-3] + 'Z'
        date_to = get_date_time_as_string(date_time_obj=todate, time_format=time_format, url_encode=False)[:-3] + 'Z'
        for i in range(0, self.cms_number_of_quick_links):
            self.cms_config.create_quick_link(title=self.quick_link_names[i],
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

    def test_001_coral_verify_navigation_to_other_links_by_swiping_through(self):
        """
        DESCRIPTION: **[CORAL]** Verify navigation to other links by swiping through.
        EXPECTED: * Quick links are displayed in a Carousel as separate blocks.
        EXPECTED: * Quick links containers have a flexible width
        EXPECTED: * Quick links that don't fit the width of the screen are cut off
        EXPECTED: * User is able to navigate to the other quick links by swiping through
        """
        self.site.wait_content_state('homepage')
        sleep(5)
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No "Quick Links" present')
        for i in range(0, self.cms_number_of_quick_links):
            self.verify_quick_link_displayed(name=self.quick_link_names[i])

    def test_002_ladbrokes_verify_navigation_to_other_links_by_swiping_updown(self):
        """
        DESCRIPTION: **[LADBROKES]** Verify navigation to other links by swiping up/down.
        EXPECTED: * Quick links are displayed as fixed vertical list.
        EXPECTED: * Quick links are stretched to fit the width of the screen.
        EXPECTED: * User is able to navigate to the other quick links by swiping up/down.
        """
        # covered in above step
