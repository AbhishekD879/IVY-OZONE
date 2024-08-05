import pytest
import tests
import time
from datetime import datetime
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C64881014_Verify_universal_view_for_user_without_segmentation(BaseFeaturedTest):
    """
    TR_ID: C64881014
    NAME: Verify universal view for user without segmentation
    DESCRIPTION: This test case verifies user without segmentation
    PRECONDITIONS: User should not mapped to any segment
    """
    keep_browser_open = True
    destination_url = f'https://{tests.HOSTNAME}//sport/football/matches'
    homepage_id = {'homepage': 0}

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: User should not mapped to any segment
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            eventID = event['event']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            eventID = event.event_id

        self.__class__.quick_link_title = 'Autotest_' + 'C64881014'
        date_from = self.get_current_time()
        self.cms_config.create_quick_link(title=self.quick_link_title,
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from,
                                          universalSegment=True)

        self.__class__.module_name = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                                             id=eventID,
                                                                             universalSegment=True,
                                                                             events_time_from_hours_delta=-10,
                                                                             module_time_from_hours_delta=-10
                                                                             )['title'].upper()

    def test_001_launch_coral_and_lads_appmobile_web_and_verify_universal_view(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web and verify universal view
        EXPECTED: Home page should load with as per CMS universal config
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(self.quick_link_title)
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_title}" not found')
        module = self.wait_for_featured_module(name=self.module_name)
        self.assertTrue(module, msg=f'"{self.module_name}" module is not found')

    def test_002_login_with_user_as_preconditions(self):
        """
        DESCRIPTION: Login with user as preconditions
        EXPECTED: Universal view should displayed as there is no congifuration for specific segement.
        """
        self.site.login()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(self.quick_link_title)
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_title}" not found')
        module = self.wait_for_featured_module(name=self.module_name)
        self.assertTrue(module, msg=f'"{self.module_name}" module is not found')
