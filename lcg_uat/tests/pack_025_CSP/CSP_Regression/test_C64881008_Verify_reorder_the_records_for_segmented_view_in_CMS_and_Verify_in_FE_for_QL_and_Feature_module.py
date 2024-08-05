import time
import pytest
import tests
import voltron.environments.constants as vec
from datetime import datetime
from random import choice
from time import sleep
from copy import copy
from faker import Faker
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@vtest
class Test_C64881008_Verify_reorder_the_records_for_segmented_view_in_CMS_and_Verify_in_FE(Common):
    """
    TR_ID: C64881008
    NAME: Verify reorder the records for segmented view in CMS and Verify in FE for QL and Featured module
    DESCRIPTION: This test case verifies for Segmented view records reordering.
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > /QL/Featured Module
    PRECONDITIONS: Create atleast a record in each module for universal and segment
    PRECONDITIONS: Create a record for Universal by selecting Universal Radio button.
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    PRECONDITIONS: (Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True
    homepage_id = {'homepage': 0}
    quick_link_name = 'auto ' + Faker().city()
    quick_link_name2 = 'auto ' + Faker().city()
    destination_url = f'https://{tests.HOSTNAME}/sport/football/matches'
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT

    def get_current_time(self):
        hours_delta = -10
        is_dst = time.localtime().tm_isdst
        hours_delta -= is_dst
        now = datetime.now()
        time_format = '%Y-%m-%dT%H:%M:%S.%f'
        current_time = self.get_date_time_formatted_string(date_time_obj=now, time_format=time_format, url_encode=False,
                                                           hours=hours_delta)[:-3] + 'Z'
        return current_time

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        sport_quick_links = self.get_initial_data_system_configuration().get('Sport Quick Links', {})
        if not sport_quick_links:
            sport_quick_links = self.cms_config.get_system_configuration_item('Sport Quick Links')
        if not sport_quick_links.get('maxAmount'):
            raise CmsClientException('Max number of quick links is not configured in CMS')
        date_from = self.get_current_time()
        self.cms_config.create_quick_link(title=self.quick_link_name,
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from,
                                          inclusionList=[self.segment],
                                          universalSegment=False)
        self.cms_config.create_quick_link(title=self.quick_link_name2,
                                          sport_id=self.homepage_id.get('homepage'),
                                          destination=self.destination_url,
                                          date_from=date_from)
        sleep(3)
        quick_links_statuses = self.cms_config.get_quick_links(sport_id='0', segment=self.segment)
        initial_markets_id_order = [quick_links['id'] for quick_links in quick_links_statuses]
        drag_panel_id = next((panel['id'] for panel in quick_links_statuses if panel['title'] == self.quick_link_name), '')

        new_order = copy(initial_markets_id_order)
        new_order.remove(drag_panel_id)
        new_order.insert(0, drag_panel_id)
        self.cms_config.set_quicklinks_ordering(new_order=new_order, moving_item=drag_panel_id,
                                                segmentName=self.segment)
        # featured Module:
        football_markets = [('last_goalscorer', {'cashout': True}),
                            ('extra_time_result', {'cashout': True})]

        if tests.settings.backend_env == 'prod':
            event = choice(self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id, all_available_events=True))
            type_id = event['event']['typeId']
            event = choice(self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id, all_available_events=True))
            race_type_id = event['event']['typeId']
        else:
            self.ob_config.add_autotest_premier_league_football_event(markets=football_markets)
            type_id = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
            self.ob_config.add_UK_racing_event(number_of_runners=1)
            race_type_id = self.ob_config.backend.ti.horse_racing.horse_racing_live.autotest_uk.type_id

        football_url = '/sport/football/matches'
        self.cms_config.add_featured_tab_module(select_event_by='Type',
                                                id=type_id,
                                                footer_link_url=football_url,
                                                show_all_events=True,
                                                events_time_from_hours_delta=-10,
                                                module_time_from_hours_delta=-10
                                                )

        race_url = '/horse-racing/featured'
        module_race_type = self.cms_config.add_featured_tab_module(select_event_by='RaceTypeId',
                                                                   id=race_type_id,
                                                                   footer_link_url=race_url,
                                                                   show_all_events=True,
                                                                   events_time_from_hours_delta=-10,
                                                                   module_time_from_hours_delta=-10,
                                                                   inclusionList=[self.segment],
                                                                   universalSegment=False
                                                                   )

        self.__class__.module_race_type_name = module_race_type['title'].upper()
        sleep(3)
        featured_events = self.cms_config.get_featured_events(segment=self.segment)
        initial_markets_id_order = [featured_event['id'] for featured_event in featured_events]
        drag_panel_id = next((panel['id'] for panel in featured_events if panel['title'] == self.module_race_type_name.title()), '')
        new_order = copy(initial_markets_id_order)
        new_order.remove(drag_panel_id)
        new_order.insert(0, drag_panel_id)
        self.cms_config.set_featured_events_ordering(new_order=new_order, moving_item=drag_panel_id,
                                                     segmentName=self.segment)

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        # covered in step1

    def test_003_select_any_segment_from_the_segment_dropdown(self):
        """
        DESCRIPTION: Select any segment from the Segment dropdown
        EXPECTED: Exisiting records for specific segment should display along with universal records
        EXPECTED: (Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
        """
        # covered in step1

    def test_004_reorder_the_records_by_drag_and_drop(self):
        """
        DESCRIPTION: Reorder the records by drag and drop
        EXPECTED: User should able to reorder the records
        """
        # covered in step1

    def test_005_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')

    def test_006_login_in_fe_with_segment_useras_per_preconditions(self):
        """
        DESCRIPTION: Login in FE with segment user(as per preconditions)
        EXPECTED: Order of the records should be as per CMS configurations.
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        quick_links = self.site.home.tab_content.quick_links.items_as_ordered_dict
        self.assertTrue(quick_links, msg='No quick links present on the page')
        actual_quick_link = []
        quick_links_statuses = self.cms_config.get_quick_links(sport_id='0', segment=self.segment)
        for quick_link in quick_links_statuses:
            if (quick_link['validityPeriodStart'] <= datetime.utcnow().isoformat() <= quick_link['validityPeriodEnd']) and quick_link['disabled'] is False:
                actual_quick_link.append(quick_link['title'])
        self.assertEquals(list(quick_links.keys()), actual_quick_link, msg='No quick links present on the page')
        self.assertEquals(list(quick_links.keys())[0], self.quick_link_name, msg='No quick links present on the page')
        featured_module = self.site.home.get_module_content(self.get_ribbon_tab_name(self.cms_config.constants.MODULE_RIBBON_INTERNAL_IDS.featured))
        section = featured_module.accordions_list.items_as_ordered_dict
        self.assertTrue(section, msg=f'Section is not found on FEATURED tab')
        self.assertEquals(list(section.keys())[0], self.module_race_type_name,
                          msg=f'{list(section.keys())[0]} section is not same as {self.module_race_type_name}')
