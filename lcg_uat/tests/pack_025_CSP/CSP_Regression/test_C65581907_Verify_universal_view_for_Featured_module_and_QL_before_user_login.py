import pytest
import time
import tests
from datetime import datetime
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from tests.base_test import vtest


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C65581907_Verify_universal_view_for_Featured_module_and_QL_before_user_login(BaseFeaturedTest):
    """
    TR_ID: C65581907
    NAME: Verify universal view for Featured Module and QL before user login.
    DESCRIPTION: This testcases verifies Universal view before user login
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > Surface bet/HC
    PRECONDITIONS: Create atleast a record in each module
    PRECONDITIONS: Select Universal Radio button while creating record.
    PRECONDITIONS: For Universal,There is atleast one record for each module added to the Homepage in CMS
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
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > sports pages > Surface bet/Highlight carousel
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            eventID = event['event']['id']
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            eventID = event.event_id

        if not self.is_quick_links_enabled():
            raise CmsClientException('"Quick links" module is disabled')
        if self.is_quick_link_disabled_for_sport_category(sport_id=self.homepage_id.get('homepage')):
            raise CmsClientException('"Quick links" module is disabled for homepage')
        self.__class__.quick_link_title = 'Autotest_' + 'C65581907'
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

    def test_001_launch_the_application(self):
        """
        DESCRIPTION: Launch the application.
        EXPECTED: Application should launch successfully.
        """
        # Covered in above step

    def test_002_navigate_to_homepage(self):
        """
        DESCRIPTION: Navigate to Homepage
        EXPECTED: Home page should be opened.
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_003_verify_universal_view_by_default_before_login(self):
        """
        DESCRIPTION: Verify universal view (by default) before login
        EXPECTED: User should able to view Universal records for each module (Surface bet/HC) as configured in CMS.
        """
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No Quick links found on the page')
        quick_link = quick_links.get(self.quick_link_title)
        self.assertTrue(quick_link, msg=f'Quick link "{self.quick_link_title}" not found')
        module = self.wait_for_featured_module(name=self.module_name)
        self.assertTrue(module, msg=f'"{self.module_name}" module is not found')
