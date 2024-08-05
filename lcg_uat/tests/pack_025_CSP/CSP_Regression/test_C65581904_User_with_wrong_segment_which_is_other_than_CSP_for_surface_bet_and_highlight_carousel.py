import pytest
import voltron.environments.constants as vec
import tests
from tests.Common import Common
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import generate_highlights_carousel_name


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C65581904_User_with_wrong_segment_which_is_other_than_CSP_for_Surface_bet_and_highlight_carousel(Common):
    """
    TR_ID: C65581904
    NAME: User with wrong segment which is other than CSP_ for surface bet and highlight carousel
    DESCRIPTION: This test case verifies segment name
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > Surface bet/Highlight carousel
    PRECONDITIONS: User should mapped to Segment in Optimove Ex SegName = CSP_CORAL_SPORTS_FOOTBALL_20210923_ALL.
    """
    keep_browser_open = True
    cookie_name = vec.bma.CSP_COOKIE_SEGMENT
    segment = vec.bma.CSP_CMS_SEGEMENT
    Wrong_segment = vec.bma.UNIVERSAL_SEGMENT
    highlights_carousels_title = [generate_highlights_carousel_name()]

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: CMS configuration>
        PRECONDITIONS: CMS > sports pages > Surface bet/Highlight carousel
        """
        if tests.settings.backend_env == 'prod':
            event = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)[0]
            eventID = event['event']['id']
            outcomes = next(((market['market']['children']) for market in event['event']['children'] if
                             market['market'].get('children')), None)
            event_selection = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            selection_id = list(event_selection.values())[0]
        else:
            event = self.ob_config.add_autotest_premier_league_football_event()
            selection_id = event.selection_ids[event.team1]
            eventID = event.event_id

        surface_bet = self.cms_config.add_surface_bet(selection_id=selection_id,
                                                      categoryIDs=[0, 16],
                                                      inclusionList=[self.segment], universalSegment=False,
                                                      eventIDs=[eventID], edpOn=True, displayOnDesktop=True)
        self.__class__.surface_bet_title = surface_bet.get('title').upper()
        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[0],
                                                   events=[eventID], inclusionList=[self.segment],
                                                   universalSegment=False)
        self.__class__.highlights_carousel_name = self.highlights_carousels_title[0] if not self.brand == 'ladbrokes' \
            else self.highlights_carousels_title[0].upper()

    def test_001_login_to_cms_as_admin_user(self):
        """
        DESCRIPTION: Login to CMS as admin user.
        EXPECTED: User should be logged in successfully.
        """
        # Covered in preconditions

    def test_002_navigate_to_module_from_preconditions(self):
        """
        DESCRIPTION: Navigate to module from preconditions.
        EXPECTED: User should be navigated successfully.
        """
        # Covered in preconditions

    def test_003_click_on_Surface_bet_HC_link(self):
        """
        DESCRIPTION: Click on Surface bet/HC link.
        EXPECTED: User should be able to view existing Surface bet/HC.
        """
        # Covered in preconditions

    def test_004_create_a_segmented_Surface_bet_HC_with_csp__excsp_1_segment_name_and_login_with_segmented_user_verify_in_fe(self):
        """
        DESCRIPTION: Create a segmented Surface bet/HC with CSP_ (Ex:CSP_1) segment name and Login with Segmented user Verify in FE
        EXPECTED: User should able to view segmented Surface bet/HC.
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
        highlight_carousels = self.site.home.tab_content.highlight_carousels
        self.assertTrue(highlight_carousels, msg='No highlight carousels')
        highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name}')
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(),
                        msg='User has not logged out!')

    def test_005_create_a_segmented_Surface_bet_HC_otherthan_csp__exsegment_segment_name_and_login_with_segmented_user_verify_in_fe(self):
        """
        DESCRIPTION: Create a segmented Surface bet/HC otherthan CSP_ (ex:Segment )segment name and Login with Segmented user Verify in FE
        EXPECTED: If user should belongs to wrong segment (without CSP_) Universal view should be displayed.
        """
        self.site.login()
        self.set_local_storage_cookies_csp(self.cookie_name, self.Wrong_segment)
        self.device.refresh_page()
        self.site.wait_content_state(state_name='Homepage', timeout=20)
        surface_bet_presence = self.site.home.tab_content.has_surface_bets()
        if surface_bet_presence:
            surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
            surface_bet = surface_bets.get(self.surface_bet_title)
            self.assertFalse(surface_bet, msg=f'"{self.surface_bet_title}" found in "{list(surface_bets.keys())}"')
        else:
            self._logger.info(msg='Surface Bets not present')
        highlight_carousel_presence = self.site.home.tab_content.has_highlight_carousels()
        if highlight_carousel_presence:
            highlight_carousels = self.site.home.tab_content.highlight_carousels
            highlight_carousel = highlight_carousels.get(self.highlights_carousel_name)
            self.assertFalse(highlight_carousel,
                             msg=f'Displayed Highlights Carousel named {self.highlights_carousel_name}')
        else:
            self._logger.info(msg='High light Carousel not present')

    def test_006_repeat_same_steps_for_all_the_modules(self):
        """
        DESCRIPTION: Repeat same steps for all the modules
        EXPECTED: Universal view should displayed for wrong segmented name
        """
        # Covered in above steps
