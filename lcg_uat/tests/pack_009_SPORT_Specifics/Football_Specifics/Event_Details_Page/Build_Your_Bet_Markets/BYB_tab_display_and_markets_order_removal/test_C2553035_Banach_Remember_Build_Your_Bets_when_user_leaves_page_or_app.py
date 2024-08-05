import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


# @pytest.mark.tst2
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.build_your_bet
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C2553035_Banach_Remember_Build_Your_Bets_when_user_leaves_page_or_app(BaseBanachTest):
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
    proxy = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Get OB event with Banach markets or create one to use in mock service
        """
        self.__class__.eventID = self.get_ob_event_with_byb_market()

    def test_001__navigate_to_football_edp_page_of_event_that_satisfies_the_following_event_is_from_league_competition_that_is_added_and_enabled_in_cms_and_is_returned_from_banach_eventsid_request_to_banach_for_this_event_contains_info_within_data_response_observe_markets_tabs(self):
        """
        DESCRIPTION: * Navigate to Football EDP page of event, that satisfies the following:
        DESCRIPTION: * event is from league (competition), that is added and enabled in CMS and is returned from Banach
        DESCRIPTION: * /events[ID] request to Banach for this event contains info within 'data' response
        DESCRIPTION: * Observe Markets tabs
        EXPECTED: * 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is present within markets tab
        EXPECTED: * Position of 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab is defined by EDP-Markets response from CMS
        """
        self.navigate_to_edp(self.eventID)
        self.site.wait_content_state(state_name='EventDetails')
        byb_tab = self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(byb_tab, msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_002_add_selections_to_byb_dashboard(self):
        """
        DESCRIPTION: Add selection(s) to BYB Dashboard
        EXPECTED: * Bet Dashboard is expanded by default, containing added selection(s)
        EXPECTED: * Chosen selections are recorded to Local Storage -> OX.yourCallStoredData: <event_id and names of added selections>
        """
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting.is_expanded(),
                        msg=f'Market "{self.expected_market_sections.match_betting}" is not expanded')
        match_betting_selection_name = match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_name, msg='No selections added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')

    def test_003_go_to_other_tabspages_within_or_outside_the_app__return_to_pre_match_football_event_from_step_1(self):
        """
        DESCRIPTION: Go to other tabs/pages within or outside the app > Return to Pre-match Football event from Step 1
        EXPECTED: * Market accordions, that contain selected selections are shown expanded
        EXPECTED: * If user returns < 3 hours, 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab state is kept (corresponding selections are added and displayed within BYB Dashboard, market accordions are expanded/collapsed)
        EXPECTED: * If the price change has occurred, new price is displayed in BYB Dashboard
        EXPECTED: * If user returns 3 ≥ hours, 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab state is reset to default
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state(state_name='HomePage')
        self.navigate_to_edp(self.eventID)
        self.site.wait_content_state(state_name='EventDetails')
        sleep(3)
        byb_tab = self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(byb_tab, msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        match_betting_market = self.get_market(market_name=self.expected_market_sections.match_betting)
        self.assertTrue(match_betting_market.is_expanded(),
                        msg=f'Market "{self.expected_market_sections.match_betting}" is not expanded')
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')

    def test_004_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: * User is logged in
        EXPECTED: * 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** page state is kept (selected selections are displayed within BYB Dashboard)
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state(state_name='HomePage')
        self.site.header.sign_in.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg='No login dialog present on page')
        self.dialog.username = tests.settings.betplacement_user
        self.dialog.password = tests.settings.default_password
        self.dialog.click_login()
        self.dialog.wait_dialog_closed()
        self.site.close_all_dialogs(async_close=False)
        self.navigate_to_edp(self.eventID)
        self.site.wait_content_state(state_name='EventDetails')
        sleep(3)
        byb_tab = self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(byb_tab, msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')

    def test_005_edit_added_selections_remove_and_add_new_or_select_other_ones(self):
        """
        DESCRIPTION: Edit added selections (remove and add new or select other ones)
        EXPECTED: * New selections within BYB Dashboard are available
        EXPECTED: * Chosen selections are recorded to Local Storage -> OX.yourCallStoredData: <event_id and names of added selections>
        """
        self.add_byb_selection_to_dashboard(market_name=self.expected_market_sections.match_betting,
                                            selection_index=2)

    def test_006_repeat_step_3(self):
        """
        DESCRIPTION: Repeat step 3
        """
        self.test_003_go_to_other_tabspages_within_or_outside_the_app__return_to_pre_match_football_event_from_step_1()

    def test_007_logout(self):
        """
        DESCRIPTION: Logout
        EXPECTED: User is logged out
        """
        self.site.logout()

    def test_008_navigate_to_pre_match_football_event_from_step_1___verify_build_your_bet_coral__bet_builder_ladbrokes_state(self):
        """
        DESCRIPTION: Navigate to Pre-match Football event from Step 1  > Verify 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** state
        EXPECTED: * 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab state is reset to default
        EXPECTED: *  'OX.yourCallStoredData' parameter is empty in Local Storage
        """
        self.navigate_to_edp(self.eventID)
        self.site.wait_content_state(state_name='EventDetails')
        sleep(3)
        byb_tab = self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(byb_tab, msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.assertFalse(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(), msg='BYB Dashboard panel is shown')
