import pytest
from time import sleep
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest


# @pytest.mark.tst2   # cannot get banach events in qa environments
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.build_your_bet
@vtest
class Test_C1990085_Banach_Markets_with_1_switcher_90min_1st_2nd_Half_Multiple_Selections(BaseBanachTest):
    """
     TR_ID: C1990085
     NAME: Banach Markets with 1 switcher (90min, 1st, 2nd Half) & Multiple Selections
     DESCRIPTION: This test case verifies the display and selection rule of markets with multiple selections and switcher (90min, 1st, 2nd Half)
     DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
     DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
     PRECONDITIONS: Build Your Bet CMS configuration:
     PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
     PRECONDITIONS: **Scope of markets with multiple selections with switcher. Select available for testing**
     PRECONDITIONS: TOTAL GOALS
     PRECONDITIONS: PARTICIPANT_1 TOTAL GOALS
     PRECONDITIONS: PARTICIPANT_2 TOTAL GOALS
     PRECONDITIONS: TOTAL CORNERS
     PRECONDITIONS: PARTICIPANT_1 TOTAL CORNERS
     PRECONDITIONS: PARTICIPANT_2 TOTAL CORNERS
     PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
     PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
     PRECONDITIONS: **'Build Your Bet (Coral)/Bet Builder (Ladbrokes)' tab on event details page is loaded and no selections are added to the dashboard.**
     """
    keep_browser_open = True
    EXPECTED_TOTAL_GOALS_BUTTONS = ['90 Minutes', '1st Half', '2nd Half']

    def get_dashboard_outcomes(self):
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(),
                        msg='BYB Dashboard panel is not shown')
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        result = wait_for_result(lambda: '' != list(dashboard_panel.outcomes_section.items_as_ordered_dict.keys())[0],
                                 timeout=2,
                                 name='No empty name on dashboard')
        self.assertTrue(result, msg='Empty name on dashboard')
        outcomes = dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        self.__class__.dashboard_selections = list(outcomes.keys())

    def test_000_preconditions(self):
        """
     PRECONDITIONS: Build Your Bet CMS configuration:
     PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
     PRECONDITIONS: **Scope of markets with multiple selections with switcher. Select available for testing**
     PRECONDITIONS: TOTAL GOALS
     PRECONDITIONS: PARTICIPANT_1 TOTAL GOALS
     PRECONDITIONS: PARTICIPANT_2 TOTAL GOALS
     PRECONDITIONS: TOTAL CORNERS
     PRECONDITIONS: PARTICIPANT_1 TOTAL CORNERS
     PRECONDITIONS: PARTICIPANT_2 TOTAL CORNERS
     PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
     PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
     PRECONDITIONS: **'Build Your Bet (Coral)/Bet Builder (Ladbrokes)' tab on event details page is loaded and no selections are added to the dashboard.**"""
        self.__class__.proxy = None
        eventID = self.get_ob_event_with_byb_market(
            market_name=self.expected_market_sections.total_goals.title())
        self.navigate_to_edp(event_id=eventID)
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.__class__.total_goals = self.get_market(
            market_name=self.expected_market_sections.total_goals)
        self.assertTrue(self.total_goals,
                        msg=f'"Total Goals" section is not found')

    def test_001_expand__collapse_market_accordion_of_market_without_switcher_provided_in_the_pre_conditions(self):
        """
         DESCRIPTION: Expand / collapse market accordion of market without switcher provided in the pre-conditions
         EXPECTED: - Switcher is displayed having 3 tabs (90min, 1st, 2nd Half)
         EXPECTED: - '90 mins' selected by default
         """
        if self.total_goals.is_expanded():
            self.total_goals.collapse()
        self.total_goals.expand()
        total_goals_switchers = list(self.total_goals.time_period_outcomes_list.items_as_ordered_dict.keys())
        self.assertEqual(total_goals_switchers, self.EXPECTED_TOTAL_GOALS_BUTTONS,
                         msg=f'Actual market headers "{total_goals_switchers}" '
                             f'are not same as expected headers: "{self.EXPECTED_TOTAL_GOALS_BUTTONS}"')
        # self.__class__.btn_90_min = self.total_goals.time_period_outcomes_list.items_as_ordered_dict.get(
        #     self.EXPECTED_TOTAL_GOALS_BUTTONS[0])
        # self.assertTrue(self.btn_90_min.is_selected(),
        #                 msg=f'"{self.EXPECTED_TOTAL_GOALS_BUTTONS[0]}" button is not selected by default')

    def test_002_switch_between_90min_1st_2nd_half_tabs(self):
        """
         DESCRIPTION: Switch between 90min, 1st, 2nd Half tabs
         EXPECTED: - Within each tab there are selections displayed in 2 columns as per **selections** request e.g.:
         EXPECTED: Over 0.5 Goals / Under 0.5 Goals
         EXPECTED: Over 1.5 Goals / Under 1.5 Goals
         EXPECTED: - A maximum of 3 rows are displayed with the 'Show More' link in the footer when # of rows>3
         """
        switchers = list(self.total_goals.time_period_outcomes_list.items_as_ordered_dict.values())
        for index in range(len(switchers)):
            switchers[index].click()
            sleep(1)
            selections_list = self.total_goals.outcomes.items_as_ordered_dict
            self.__class__.selections = []
            for selection in selections_list.keys():
                self.selections.append(selection)
                self.assertTrue(selections_list[selection].is_displayed(),
                                msg=f'selection name: "{selection}" is not displayed')

    def test_003_on_the_90_mins_tab_tap_on_show_more_link_in_the_footer_if_selections_rows3(self):
        """
         DESCRIPTION: On the #90 mins' tab tap on 'Show More' link in the footer if selections rows>3
         EXPECTED: The full list of all available selections is displayed with a 'Show Less' link at the bottom of the list
         """
        # Show More link functionality removed
        # self.btn_90_min.click()
        # sleep(1)
        # selections_list = self.total_goals.outcomes.items_as_ordered_dict
        # if len(selections_list) == 6:
        #     self.assertTrue(self.total_goals.show_all_button.is_displayed(), msg=f'Show all button is displayed')
        #     self.total_goals.show_all_button.click()
        #     self.assertTrue(self.total_goals.show_less_button.is_displayed(),
        #                     msg=f'Show less button is not displayed')
        #     selections_list = self.total_goals.outcomes.items_as_ordered_dict
        #     self.assertTrue(len(selections_list) > 6, msg=f'Only 6 selections are displaying')

    def test_004_tap_show_less_link(self):
        """
         DESCRIPTION: Tap 'Show Less' link
         EXPECTED: A maximum of 3 rows are displayed again with the 'Show More' link in the footer.
         """
        # Show less link functionality removed
        # self.total_goals.show_less_button.click()
        # sleep(1)
        # selections_list = self.total_goals.outcomes.items_as_ordered_dict
        # self.assertTrue(self.total_goals.show_all_button.is_displayed(),
        #                 msg=f'Show all button is displayed')
        # self.assertTrue(len(selections_list) == 6, msg=f'More than 6 selections are displaying')

    def test_005_tap_on_1_selection_eg_over_15_goals_from_90_mins_switcher_tab(self):
        """
         DESCRIPTION: Tap on 1 selection (e.g. 'Over 1.5 Goals') from "90 mins" switcher tab
         EXPECTED: - Selection is highlighted inside accordion
         EXPECTED: - Selection is added to the dashboard
         """
        self.total_goals.outcomes.items_as_ordered_dict[self.selections[0]].click()
        self.assertTrue(self.total_goals.outcomes.items_as_ordered_dict[self.selections[0]].is_selected(),
                        msg=f'selection name: "{self.selections[0]}" is not highlighted')
        self.total_goals.time_period_outcomes_list.items_as_ordered_dict.get(self.EXPECTED_TOTAL_GOALS_BUTTONS[0]).click()
        self.__class__.goals = self.total_goals.goals_outcomes_list.items_as_ordered_dict
        total_goals_selection_names = list(self.goals.keys())[0]
        sleep(2)
        self.goals.get('Over').click()
        self.total_goals.add_to_betslip_button.click()
        self.get_dashboard_outcomes()
        if self.brand == 'ladbrokes':
            self.__class__.expected_second_selection = f'{self.expected_market_sections.total_goals} {"90 Mins"} - {total_goals_selection_names} {"0.5 Goals"}'
        else:
            self.__class__.expected_second_selection = f'{self.expected_market_sections.total_goals.title()} {"90 Mins"} {total_goals_selection_names.upper()} {"0.5 GOALS"}'
        self.assertIn(self.expected_second_selection, self.dashboard_selections,
                      msg=f'Added selection "{self.expected_second_selection}" is not present in dashborad selecitons "{self.dashboard_selections}"')

    def test_006_tap_on_2_selection_eg_over_25_goals_from_the_same_tab(self):
        """
         DESCRIPTION: Tap on 2 selection (e.g. 'Over 2.5 Goals') from the same tab
         EXPECTED: - Fist selection is deselected and removed from the dashboard
         EXPECTED: - Second selection is selected inside accordion and is in the dashboard
         """
        # This functionality not available
        # total_goals_team_names = self.selections[1]
        # self.total_goals.outcomes.items_as_ordered_dict[self.selections[1]].click()
        # self.assertTrue(self.total_goals.outcomes.items_as_ordered_dict[self.selections[1]].is_selected(),
        #                 msg=f'selection name: "{total_goals_team_names}" is not highlighted')
        # self.total_goals.time_period_outcomes_list.items_as_ordered_dict.get(
        #     self.EXPECTED_TOTAL_GOALS_BUTTONS[0]).click()
        # sleep(2)
        # total_goals_selection_names = list(self.goals.keys())[0]
        # self.total_goals.goals_outcomes_list.items_as_ordered_dict.get('Over').click()
        # self.total_goals.add_to_betslip_button.click()
        # self.get_dashboard_outcomes()
        # if self.brand == 'ladbrokes':
        #     self.__class__.expected_second_selection = f'{total_goals_team_names} {self.expected_market_sections.total_goals} {"90 mins"} - {total_goals_selection_names} {"0.5 Goals"}'
        # else:
        #     self.__class__.expected_second_selection = f'{self.expected_market_sections.total_goals.title()} {self.EXPECTED_TOTAL_GOALS_BUTTONS[0].title()} {total_goals_selection_names.upper()}'
        # self.assertNotIn(self.expected_first_selection, self.dashboard_selections,
        #                  msg=f'Added selection "{self.expected_first_selection}" is present in dashborad selecitons "{self.dashboard_selections}"')
        # self.assertIn(self.expected_second_selection, self.dashboard_selections,
        #               msg=f'Added selection "{self.expected_second_selection}" is not present in dashborad selecitons "{self.dashboard_selections}"')

    def test_007_switch_to_1st_half_tab_and_tap_on_selection(self):
        """
         DESCRIPTION: Switch to "1st half" tab and tap on selection
         EXPECTED: 2 selections is dashboard:
         EXPECTED: - Selection form "1st half" tab is highlighted inside accordion
         EXPECTED: - Selection "1st half" tab has been added to the dashboard
         """
        total_goals_team_names = self.selections[1]
        self.total_goals.outcomes.items_as_ordered_dict[self.selections[1]].click()
        self.assertTrue(self.total_goals.outcomes.items_as_ordered_dict[self.selections[1]].is_selected(),
                        msg=f'selection name: "{total_goals_team_names}" is not highlighted')
        total_goals_selection_names = list(self.goals.keys())[0]
        self.total_goals.time_period_outcomes_list.items_as_ordered_dict.get(
            self.EXPECTED_TOTAL_GOALS_BUTTONS[1]).click()
        sleep(3)
        self.total_goals.goals_outcomes_list.items_as_ordered_dict.get('Over').click()
        self.total_goals.add_to_betslip_button.click()
        self.get_dashboard_outcomes()
        market = self.EXPECTED_TOTAL_GOALS_BUTTONS[1].title().replace('1St', '1st')
        if self.brand == 'ladbrokes':
            self.__class__.expected_first_selection = f'{total_goals_team_names.upper()} {self.expected_market_sections.total_goals} {market} - {total_goals_selection_names} {"0.5 Goals"}'
        else:
            self.__class__.expected_first_selection = f'{total_goals_team_names.upper()} {self.expected_market_sections.total_goals.title()} {market} {total_goals_selection_names.upper()} {"0.5 GOALS"}'
        self.assertEqual(self.dashboard_selections, [self.expected_second_selection, self.expected_first_selection],
                         msg=f'Actual selections: "{self.dashboard_selections}" is not same as '
                             f'Expected selections:"{[self.expected_second_selection, self.expected_first_selection]}"')
