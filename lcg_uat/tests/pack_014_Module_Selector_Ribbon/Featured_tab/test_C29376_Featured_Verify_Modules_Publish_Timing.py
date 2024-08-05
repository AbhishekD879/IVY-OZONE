import datetime
import pytest
from time import sleep
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from crlat_cms_client.utils.date_time import get_date_time_as_string


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  cannot create featured module in prod cms.
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.homepage_featured
@vtest
class Test_C29376_Featured_Verify_Modules_Publish_Timing(BaseFeaturedTest):
    """
    TR_ID: C29376
    NAME: Featured: Verify Modules Publish Timing
    DESCRIPTION: This test case verifies Modules Publish Timing on Featured tab.
    PRECONDITIONS: 1) At least 1 Featured Module is created in CMS
    PRECONDITIONS: 2)
    PRECONDITIONS: *   Publish Timing corresponds to values set in 'Visible from', 'Visible to' fields in CMS
    PRECONDITIONS: ('displayFrom', 'displayTo' attributes)
    PRECONDITIONS: *   It is possible to set time and dates manually or with buttons 'Today' (set current day's date) and 'Tomorrow' (set the next day's date)
    PRECONDITIONS: 3) CMS: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: (check **CMS_ENDPOINT **via ***devlog ***function)
    PRECONDITIONS: **NOTE:** For caching needs Akamai service is used, so after saving changes in CMS there could be **delay up to 5-10 mins** before they will be applied and visible on the front end.
    """
    keep_browser_open = True
    time_format = '%Y-%m-%dT%H:%M:%S.%f'

    def update_values(self, fromdate =None, todate=None):

        fromdate = get_date_time_as_string(date_time_obj=fromdate, time_format=self.time_format, url_encode=False,
                                           minutes=-2)[:-3] + 'Z'
        todate = get_date_time_as_string(date_time_obj=todate, time_format=self.time_format, url_encode=False
                                         )[:-3] + 'Z'
        self.cms_config.update_featured_tab_module(module_id=self.featured_module['id'], date_from=fromdate,
                                                   date_to=todate)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage')
        featured_module = self.site.home.get_module_content(
            self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        featured_module.scroll_to()

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create Football event and featured tab with event type
        """
        event = self.ob_config.add_autotest_premier_league_football_event()
        eventID = event.event_id
        self.__class__.featured_module = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=eventID,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10, show_expanded=False,
            show_all_events=True)

        self.__class__.featured_module_name = self.featured_module['title'].upper()
        self.site.wait_content_state('homepage')
        sleep(3)
        self.wait_for_featured_module(name=self.featured_module_name)

    def test_001_setvisible_from_visible_to_fields_in_cms_for_verified_module_from_the_past(self):
        """
        DESCRIPTION: Set 'Visible from', 'Visible to' fields in CMS  for verified Module from the Past
        EXPECTED: Verified Module is not shown on the Featured tab
        """
        fromdate = datetime.datetime.now() - datetime.timedelta(days=3)
        todate = datetime.datetime.now() - datetime.timedelta(days=2)
        self.update_values(fromdate=fromdate, todate=todate)
        featured_module = self.get_section(self.featured_module_name, timeout=10, expected_result=False)
        self.assertFalse(featured_module,
                         msg=f'Module "{self.featured_module_name}" is found in FEATURED tab section, whereas it should not appear')

    def test_002_setvisible_from_visible_to_fields_in_cms_for_verified_module_from_the_future(self):
        """
        DESCRIPTION: Set 'Visible from', 'Visible to' fields in CMS  for verified Module from the Future
        EXPECTED: Verified Module is not shown on the Featured tab
        """
        fromdate = datetime.datetime.now() + datetime.timedelta(days=3)
        todate = datetime.datetime.now() + datetime.timedelta(days=4)
        self.update_values(fromdate=fromdate, todate=todate)
        featured_module = self.get_section(self.featured_module_name, timeout=10, expected_result=False)
        self.assertFalse(featured_module,
                         msg=f'Module "{self.featured_module_name}" is found in FEATURED tab section, whereas it should not appear')

    def test_003_setvisible_from_visible_to_fields_in_cms_for_verified_module_with_current_day_within_this_time_interval(self):
        """
        DESCRIPTION: Set 'Visible from', 'Visible to' fields in CMS  for verified Module with **current day** within this time interval
        EXPECTED: Verified Module is shown on the Featured tab
        """
        fromdate = datetime.datetime.now() - datetime.timedelta(hours=2)
        todate = datetime.datetime.now() + datetime.timedelta(hours=2, minutes=15)
        self.update_values(fromdate=fromdate, todate=todate)
        featured_module = self.get_section(self.featured_module_name, timeout=10)
        self.assertTrue(featured_module, msg=f'Module "{self.featured_module_name}" is not found in FEATURED tab section, whereas it should appear')

    def test_004_set_visible_from_in_x_minutes_from_now_and_verify_it_on_front_end(self):
        """
        DESCRIPTION: Set 'Visible from' in x minutes from now and verify it on front end
        EXPECTED: Module will appear on front end in x minutes
        """
        fromdate = datetime.datetime.now() - datetime.timedelta(minutes=58)
        todate = datetime.datetime.now() + datetime.timedelta(hours=24)
        self.update_values(fromdate=fromdate, todate=todate)
        featured_module = self.get_section(self.featured_module_name, timeout=10)
        self.assertTrue(featured_module, msg=f'Module "{self.featured_module_name}" is not found in FEATURED tab section, whereas it should appear')

    def test_005_set_visible_from_in_the_past_visible_to_x_minutes_in_future_and_verify_it_on_front_end(self):
        """
        DESCRIPTION: Set 'Visible from' in the past, 'Visible to' x minutes in future and verify it on front end
        EXPECTED: Module will disappear from front end in x minutes
        """
        fromdate = datetime.datetime.now() - datetime.timedelta(days=3, hours=5, minutes=30)
        todate = datetime.datetime.now() - datetime.timedelta(minutes=59)
        self.update_values(fromdate=fromdate, todate=todate)
        featured_module = self.get_section(self.featured_module_name, timeout=10, expected_result=False)
        self.assertFalse(featured_module, msg=f'Module "{self.featured_module_name}" is found in FEATURED tab section, whereas it should not appear')
