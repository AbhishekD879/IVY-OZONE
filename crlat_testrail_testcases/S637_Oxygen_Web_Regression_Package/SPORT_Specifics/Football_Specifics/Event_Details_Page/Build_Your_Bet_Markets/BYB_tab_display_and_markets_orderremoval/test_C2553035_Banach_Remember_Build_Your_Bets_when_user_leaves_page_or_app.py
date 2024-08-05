import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2553035_Banach_Remember_Build_Your_Bets_when_user_leaves_page_or_app(Common):
    """
    TR_ID: C2553035
    NAME: Banach. Remember Build Your Bets when user leaves page or app
    DESCRIPTION: This test case verifies remembering or resetting to default 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** page state when the user leaves the page or app
    PRECONDITIONS: **Config:**
    PRECONDITIONS: 1. 'Build Your Bet' tab is available on Event Details Page : In CMS -> System-configuration -> YOURCALLICONSANDTABS -> 'enableTab' is selected
    PRECONDITIONS: 2. Banach leagues are added and enabled in CMS -> Your Call -> YourCall Leagues
    PRECONDITIONS: 3. Event belonging to Banach league is mapped (on the Banach side) and created in OpenBet (T.I)
    PRECONDITIONS: 4. BYB markets are added in CMS -> BYB -> BYB Markets
    PRECONDITIONS: 5. 'buildyourbet leagues' response from Banach returns at least one of leagues (competitions), that are added to CMS
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/YourCall+feature+CMS+configuration
    PRECONDITIONS: 1. Oxygen application is loaded
    """
    keep_browser_open = True

    def test_001__navigate_to_football_edp_page_of_event_that_satisfies_the_following_event_is_from_league_competition_that_is_added_and_enabled_in_cms_and_is_returned_from_banach_eventsid_request_to_banach_for_this_event_contains_info_within_data_response_observe_markets_tabs(self):
        """
        DESCRIPTION: * Navigate to Football EDP page of event, that satisfies the following:
        DESCRIPTION: * event is from league (competition), that is added and enabled in CMS and is returned from Banach
        DESCRIPTION: * /events[ID] request to Banach for this event contains info within 'data' response
        DESCRIPTION: * Observe Markets tabs
        EXPECTED: * 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is present within markets tab
        EXPECTED: * Position of 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is defined by EDP-Markets response from CMS
        """
        pass

    def test_002_add_selections_to_byb_dashboard(self):
        """
        DESCRIPTION: Add selection(s) to BYB Dashboard
        EXPECTED: * Bet Dashboard is expanded by default, containing added selection(s)
        EXPECTED: * Chosen selections are recorded to Local Storage -> OX.yourCallStoredData: <event_id and names of added selections>
        """
        pass

    def test_003_go_to_other_tabspages_within_or_outside_the_app__return_to_pre_match_football_event_from_step_1(self):
        """
        DESCRIPTION: Go to other tabs/pages within or outside the app > Return to Pre-match Football event from Step 1
        EXPECTED: * Market accordions, that contain selected selections are shown expanded
        EXPECTED: * If user returns < 3 hours, 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab state is kept (corresponding selections are added and displayed within BYB Dashboard, market accordions are expanded/collapsed)
        EXPECTED: * If the price change has occurred, new price is displayed in BYB Dashboard
        EXPECTED: * If user returns 3 ≥ hours, 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab state is reset to default
        """
        pass

    def test_004_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: * User is logged in
        EXPECTED: * 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** page state is kept (selected selections are displayed within BYB Dashboard)
        """
        pass

    def test_005_edit_added_selections_remove_and_add_new_or_select_other_ones(self):
        """
        DESCRIPTION: Edit added selections (remove and add new or select other ones)
        EXPECTED: * New selections within BYB Dashboard are available
        EXPECTED: * Chosen selections are recorded to Local Storage -> OX.yourCallStoredData: <event_id and names of added selections>
        """
        pass

    def test_006_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step 3
        EXPECTED: 
        """
        pass

    def test_007_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        pass

    def test_008_navigate_to_pre_match_football_event_from_step_1___verify_build_your_bet_coral__bet_builder_ladbrokes_state(self):
        """
        DESCRIPTION: Navigate to Pre-match Football event from Step 1  > Verify 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** state
        EXPECTED: * 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab state is reset to default
        EXPECTED: *  'OX.yourCallStoredData' parameter is empty in Local Storage
        """
        pass
