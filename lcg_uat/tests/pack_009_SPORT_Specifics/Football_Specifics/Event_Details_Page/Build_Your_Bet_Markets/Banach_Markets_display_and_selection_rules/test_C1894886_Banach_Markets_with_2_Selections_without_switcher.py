import pytest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


# @pytest.mark.tst2 # No banach data available in qa2 env
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.sports
@pytest.mark.build_your_bet
@vtest
class Test_C1894886_Banach_Markets_with_2_Selections_without_switcher(BaseBanachTest):
    """
    TR_ID: C1894886
    NAME: Banach. Markets with 2 Selections without switcher
    DESCRIPTION: Test case verifies display and selection rule of markets with 2 selections without switcher.
    DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
    DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Scope of markets with 2 selections without switcher. Select available for testing**
    PRECONDITIONS: RED CARD IN MATCH
    PRECONDITIONS: PARTICIPANT_1 (Home Team) RED CARD
    PRECONDITIONS: PARTICIPANT_2 (Away Team) RED CARD
    PRECONDITIONS: BOTH TEAMS TO SCORE
    PRECONDITIONS: TO WIN TO NIL
    PRECONDITIONS: TOTAL GOALS ODD/EVEN
    PRECONDITIONS: BOTH TEAMS TO SCORE IN BOTH HALVES
    PRECONDITIONS: BOTH TEAMS TO SCORE IN 1ST HALF
    PRECONDITIONS: BOTH TEAMS TO SCORE IN 2ND HALF
    PRECONDITIONS: TEAM TO SCORE IN BOTH HALVES
    PRECONDITIONS: WIN BOTH HALVES
    PRECONDITIONS: WIN EITHER HALF
    PRECONDITIONS: CLEAN SHEET
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: **'Build Your Bet(Coral)/Bet Builder (Ladbrokes) tab on event details page is loaded and no selections are added to the dashboard.**
    """
    keep_browser_open = True

    def get_dashboard_outcomes(self):
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        wait_for_result(lambda: '' != list(dashboard_panel.outcomes_section.items_as_ordered_dict.keys())[0],
                                 timeout=2,
                                 name='No empty name on dashboard')
        outcomes = dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        self.__class__.dashboard_selections = list(outcomes.keys())

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find event with player bets markets, open its EDP
        """
        self.__class__.proxy = None
        self.__class__.eventID = self.get_ob_event_with_byb_market(
            market_name=self.expected_market_sections.match_betting.title())
        self.navigate_to_edp(event_id=self.eventID)
        self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.current,
                        msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_001_expand__collapse_market_accordion_of_market_without_switcher_provided_in_the_pre_conditions(self):
        """
        DESCRIPTION: Expand / collapse market accordion of market without switcher provided in the pre-conditions
        EXPECTED: - Two selections are displayed as per request **selections** without switcher inside the market accordion
        EXPECTED: - Accordion is expandable
        """
        self.site.wait_content_state_changed(timeout=30)
        self.__class__.to_win_to_nil = self.get_market(market_name=self.expected_market_sections.to_win_to_nil)
        self.assertTrue(self.to_win_to_nil, msg=f'Can not get market "{self.expected_market_sections.to_win_to_nil}"')
        outcomes = self.to_win_to_nil.outcomes.items_as_ordered_dict
        self.assertEqual(len(outcomes), 2,
                         msg=f'Length of actual outcomes "{len(outcomes)}" is not same as expected length: "2"')
        if self.to_win_to_nil.is_expanded():
            self.to_win_to_nil.collapse()
        self.to_win_to_nil.expand()

    def test_002_tap_on_the_first_selection_inside_a_market(self):
        """
        DESCRIPTION: Tap on the first selection inside a market
        EXPECTED: - Selection is highlighted inside accordion
        EXPECTED: - Selection has been added to the dashboard
        """
        self.__class__.first_selection = self.to_win_to_nil.outcomes.items[0]
        self.first_selection.bet_button.click()
        self.assertTrue(self.first_selection.bet_button.is_selected(), msg=f'Second selection "{self.first_selection.outcome_name}" is not selected')
        self.get_dashboard_outcomes()
        if self.brand == 'ladbrokes':
            self.__class__.expected_first_selection = f'{self.expected_market_sections.to_win_to_nil} - {self.first_selection.outcome_name}'
        else:
            self.__class__.expected_first_selection = f'{self.expected_market_sections.to_win_to_nil.title()} {self.first_selection.outcome_name.upper()}'
        self.assertIn(self.expected_first_selection, self.dashboard_selections,
                      msg=f'Added selection "{self.expected_first_selection}" is not present in dashborad selecitons "{self.dashboard_selections}"')

    def test_003_tap_on_the_second_selection_inside_a_market(self):
        """
        DESCRIPTION: Tap on the second selection inside a market
        EXPECTED: - Fist selection is deselected and removed from the dashboard
        EXPECTED: - Second selection is selected inside accordion and is in the dashboard
        """
        second_selection = self.to_win_to_nil.outcomes.items[1]
        second_selection.bet_button.click()
        self.assertFalse(self.first_selection.bet_button.is_selected(expected_result=False),
                        msg=f'first selection "{self.first_selection.outcome_name}" is not deselected')
        self.assertTrue(second_selection.bet_button.is_selected(), msg=f'Second selection "{second_selection.outcome_name}" is not selected')
        self.get_dashboard_outcomes()
        if self.brand == 'ladbrokes':
            expected_second_selection = f'{self.expected_market_sections.to_win_to_nil} - {second_selection.outcome_name}'
        else:
            expected_second_selection = f'{self.expected_market_sections.to_win_to_nil.title()} {second_selection.outcome_name.upper()}'
        self.assertNotIn(self.expected_first_selection, self.dashboard_selections,
                         msg=f'First selection "{self.expected_first_selection}" is still present in dashborad selecitons "{self.dashboard_selections}"')
        self.assertIn(expected_second_selection, self.dashboard_selections,
                      msg=f'Added selection "{expected_second_selection}" is not present in dashborad selecitons "{self.dashboard_selections}"')
