import voltron.environments.constants as vec
import tests
import pytest
from copy import copy
from time import sleep
from faker import Faker
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C65581932_Verify_reorder_the_records_for_segmented_view_in_CMS_and_Verify_in_FE_for_surface_bet_and_highlight_carousel(Common):
    """
    TR_ID: C65581932
    NAME: Verify reorder the records for segmented view in CMS and Verify in FE for Surface bet and HC
    DESCRIPTION: This test case verifies for Segmented view records reordering.
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > super button/Footermenu/QL/MRT/Surface bet/Featured Module/HC/Inplay Module/Sports Ribbon
    PRECONDITIONS: Create atleast a record in each module for universal and segment
    PRECONDITIONS: Create a record for Universal by selecting Universal Radio button.
    PRECONDITIONS: Create a record for specific segment by selecting radio button 'Segment(s) inclusion' select segment in segment inclusion text box in Homepage in CMS
    PRECONDITIONS: (Segmented view = Segment specific configurations + Universal configurations (if the segment is not in excluded list))
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL
    """
    keep_browser_open = True
    highlights_carousels_title = ['Autotest ' + Faker().city(), 'Autotest ' + Faker().city()]
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            event1 = self.get_active_events_for_category(category_id=self.ob_config.tennis_config.category_id)[0]
            eventID = event['event']['id']
            eventID1 = event1['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
            selection_id2 = list(event_selection.values())[1]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = event.selection_ids[event.team1]
            selection_id2 = event.selection_ids[event.team2]
            eventID = event.event_id
            event1 = self.ob_config.add_autotest_premier_league_football_event()
            eventID1 = event1.event_id
        # surface_bet
        self.cms_config.add_surface_bet(selection_id=selection_id,
                                        categoryIDs=[0, 16], highlightsTabOn=True)

        surface_bet1 = self.cms_config.add_surface_bet(selection_id=selection_id2,
                                                       categoryIDs=[0, 16],
                                                       inclusionList=[self.segment], universalSegment=False, highlightsTabOn=True)

        self.__class__.surface_bet_title = surface_bet1.get('title').upper()
        sleep(3)
        surface_bets = self.cms_config.get_surface_bets_for_page(reference_id=0, related_to='sport',
                                                                 segment=self.segment)

        initial_markets_id_order = [surface_bet['id'] for surface_bet in surface_bets]
        drag_panel_id = next(
            (panel['id'] for panel in surface_bets if panel['title'] == self.surface_bet_title.title()), '')

        new_order = copy(initial_markets_id_order)
        new_order.remove(drag_panel_id)
        new_order.insert(0, drag_panel_id)
        self.cms_config.set_surfacebet_ordering(new_order=new_order, moving_item=drag_panel_id,
                                                segmentName=self.segment)

        # Highlight_courousel
        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[0],
                                                   events=[eventID])

        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[1],
                                                   events=[eventID1], inclusionList=[self.segment],
                                                   universalSegment=False)
        self.__class__.highlights_carousel_name = self.highlights_carousels_title[1] if not self.brand == 'ladbrokes' \
            else self.highlights_carousels_title[1].upper()
        sleep(10)
        highlights_carousels = self.cms_config.get_all_highlights_carousels(segment=self.segment)

        initial_markets_id_order = [highlights_carousel['id'] for highlights_carousel in highlights_carousels]
        drag_panel_id = next((panel['id'] for panel in highlights_carousels if panel['title'] == self.highlights_carousel_name.title()), '')

        new_order = copy(initial_markets_id_order)
        new_order.remove(drag_panel_id)
        new_order.insert(0, drag_panel_id)
        self.cms_config.set_highlight_courousel_ordering(new_order=new_order, moving_item=drag_panel_id,
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
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        self.assertEquals(list(surface_bets.keys())[0], self.surface_bet_title,
                          msg=f'{list(surface_bets.keys())[0]} section is not same as {self.surface_bet_title}')
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertTrue(highlight_carousels, msg='No highlight carousels')
        self.assertEquals(list(highlight_carousels.keys())[0], self.highlights_carousel_name,
                          msg=f'{list(highlight_carousels.keys())[0]} section is not same as {self.highlights_carousel_name}')
