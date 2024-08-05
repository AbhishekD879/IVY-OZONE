import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.Featured_tab.Highlights_Carousel.base_highlights_carousel_test import generate_highlights_carousel_name


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.other
@pytest.mark.mobile_only
@pytest.mark.csp
@vtest
class Test_C65581906_Verify_universal_view_for_SB_and_HC_before_user_login(Common):
    """
    TR_ID: C65581906
    NAME: Verify universal view for SB and HC before user login.
    DESCRIPTION: This testcases verifies Universal view before user login
    PRECONDITIONS: User should have admin access to CMS.
    PRECONDITIONS: CMS configuration>
    PRECONDITIONS: CMS > sports pages > Surface bet/HC
    PRECONDITIONS: Create atleast a record in each module
    PRECONDITIONS: Select Universal Radio button while creating record.
    PRECONDITIONS: For Universal,There is atleast one record for each module added to the Homepage in CMS
    """
    keep_browser_open = True
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
                                                      universalSegment=True,
                                                      eventIDs=[eventID], edpOn=True, displayOnDesktop=True)
        self.__class__.surface_bet_title = surface_bet.get('title').upper()
        self.cms_config.create_highlights_carousel(title=self.highlights_carousels_title[0],
                                                   events=[eventID],
                                                   universalSegment=True)
        self.__class__.highlights_carousel_name = self.highlights_carousels_title[0] if not self.brand == 'ladbrokes' else self.highlights_carousels_title[0].upper()

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
        surface_bets = self.site.home.tab_content.surface_bets.items_as_ordered_dict
        self.assertTrue(surface_bets, msg='No Surface Bets found')
        surface_bet = surface_bets.get(self.surface_bet_title)
        self.assertTrue(surface_bet, msg=f'"{self.surface_bet_title}" not found in "{list(surface_bets.keys())}"')
        highlight_carousel = self.site.home.tab_content.highlight_carousels.get(self.highlights_carousel_name)
        self.assertTrue(highlight_carousel,
                        msg=f'Failed to display Highlights Carousel named {self.highlights_carousel_name}')
