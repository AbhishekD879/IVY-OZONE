import pytest
import tests
import voltron.environments.constants as vec
from faker import Faker
from tests.Common import Common
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.csp
@pytest.mark.mobile_only
@vtest
class Test_C64881016_Verify_only_segmented_configration_in_CMS_No_universal_config_for_surface_bet_and_HC(Common):
    """
    TR_ID: C64881016
    NAME: This test case verifies only segmented configration in CMS (No universal config) for surface bet and HC.
    DESCRIPTION: This test case verifies only segmented configration in CMS (No universal config) for surface bet and HC.
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > Surface bet/HC
    PRECONDITIONS: Create atleast a record in each module for segment
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    PRECONDITIONS: (Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    highlights_carousels_title = ['Autotest ' + Faker().city()]

    def test_000_preconditions(self):
        """
        creating a surface bet and HC
        :return:
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
            selection_id1 = list(event_selection.values())[1]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = event.selection_ids[event.team1]
            selection_id1 = event.selection_ids[event.team2]
            eventID = event.event_id
        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                      categoryIDs=[0, 16],
                                                      inclusionList=[self.segment], universalSegment=False,
                                                      eventIDs=[eventID])
        self.__class__.surface_bet_title = surface_bet.get('title').upper()
        self.cms_config.add_surface_bet(selection_id=selection_id1,
                                                       categoryIDs=[0, 16],
                                                       eventIDs=[eventID])
        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[0],
                                                   events=[eventID], inclusionList=[self.segment],
                                                   universalSegment=False)
        self.__class__.highlights_carousel_name = self.highlights_carousels_title[0] if self.brand == 'bma' else self.highlights_carousels_title[0].upper()

    def test_001_launch_coral_and_lads_appmobile_web(self):
        """
        DESCRIPTION: Launch coral and Lads app/mobile web
        EXPECTED: Homepage should load as per CMS config
        """
        self.navigate_to_page(name='/')
        self.site.wait_content_state(state_name='Homepage')

    def test_002_verify_universal_view_observe__surface_bet_and_HC_as_per_pre_conditions(self):
        """
        DESCRIPTION: verify universal view ,observe all modules(as per pre conditions)
        EXPECTED: No data (records) should be displayed for surface bet and HC as there is no universal configuration
        """
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertFalse(surface_bet, msg=f'"{self.surface_bet_title}" found in "{list(surface_bets.keys())}"')

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertFalse(highlight_carousel,
                         msg=f'Highlights Carousel named {self.highlights_carousel_name} is displayed')

    def test_003_login_with_user_who_mapped_to_segment_as_preconditions(self):
        """
        DESCRIPTION: Login with user who mapped to segment as preconditions
        EXPECTED: Homepage should load as per CMS segment config.
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)

    def test_004_verify_homepage(self):
        """
        DESCRIPTION: Verify homepage
        EXPECTED: Segmented records for surface bet and HC should display as per CMS configurations
        """
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')

        highlight_carousels = self.site.home.tab_content.highlight_carousels
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name}')
