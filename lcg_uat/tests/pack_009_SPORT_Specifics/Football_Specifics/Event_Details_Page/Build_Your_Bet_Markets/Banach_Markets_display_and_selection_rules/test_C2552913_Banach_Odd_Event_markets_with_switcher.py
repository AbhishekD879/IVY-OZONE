import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from time import sleep


@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@pytest.mark.build_your_bet
@vtest
class Test_C2552913_Banach_Odd_Event_markets_with_switcher(BaseBanachTest):
    """
    TR_ID: C2552913
    NAME: Banach. Odd/Event markets with switcher
    DESCRIPTION: Test case verifies display and selection rule of markets Odd/Even markets having 2 alternative selections and switcher
    DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
    DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: Check such markets availability in Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: **Example of market**
    PRECONDITIONS: TOTAL GOALS ODD/EVEN
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: **'Build Your Bet(Coral)/Bet Builder (Ladbrokes)' tab on event details page is loaded and no selections are added to the dashboard.**
    """
    keep_browser_open = True
    team_odd = "Odd"
    team_even = "Even"
    EXPECTED_TOTAL_GOALS_BUTTONS = ["90 min", "1st Half", "2nd Half"]

    def test_000_preconditions(self):
        self.__class__.proxy = None

        eventID = self.get_ob_event_with_byb_market()
        self.navigate_to_edp(event_id=eventID)
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.__class__.total_goals_odd_even_market = self.get_market(
            market_name=self.expected_market_sections.total_goals_odd_even)
        self.assertTrue(self.total_goals_odd_even_market,
                        msg=f'"{self.expected_market_sections.total_goals_odd_even}" section is not found')

    def test_001_expand__collapse_market_accordion_of_market_with_a_switcher_provided_in_the_pre_conditions(self):
        """
        DESCRIPTION: Expand / collapse market accordion of market with a switcher provided in the pre-conditions
        EXPECTED: - Accordion is expandable/collapsable
        EXPECTED: - Switchers "90 mins", "1st half", "2nd half" are present
        """
        self.total_goals_odd_even_market.collapse()
        self.assertFalse(self.total_goals_odd_even_market.is_expanded(expected_result=False),
                         msg=f'"{self.expected_market_sections.total_goals_odd_even}" section is not collapsed')

        self.total_goals_odd_even_market.expand()
        self.assertTrue(self.total_goals_odd_even_market.is_expanded(),
                        msg=f'"{self.expected_market_sections.total_goals_odd_even}" section is not expanded')

        market_grouping_buttons = self.total_goals_odd_even_market.grouping_buttons.items_as_ordered_dict
        self.assertTrue(market_grouping_buttons, msg=f'Grouping button not found for '
                                                     f'"{self.expected_market_sections.double_chance}" market')
        self.__class__.btn_90_min = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.ninety_mins)
        self.assertTrue(self.btn_90_min, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.ninety_mins}" not found')

        btn_1st_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.first_half)
        self.assertTrue(btn_1st_half, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.first_half}" not found')
        self.assertTrue(btn_1st_half.is_displayed(),
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.first_half}" is not displayed')

        btn_2nd_half = market_grouping_buttons.get(vec.sb.HANDICAP_SWITCHERS.second_half)
        self.assertTrue(btn_2nd_half, msg=f'Grouping button "{vec.sb.HANDICAP_SWITCHERS.second_half}" not found')
        self.assertTrue(btn_2nd_half.is_displayed(),
                        msg=f'"{vec.sb.HANDICAP_SWITCHERS.second_half}" is not displayed')

    def test_002_switch_between_90_mins_1st_half_2nd_half_tabs(self):
        """
        DESCRIPTION: Switch between "90 mins", "1st half", "2nd half" tabs
        EXPECTED: - Each switcher tab contains selections "Odd", "Even" as per **selections** request
        """
        switchers = self.total_goals_odd_even_market.grouping_buttons.items
        for index in range(len(switchers)):
            switchers[index].click()
            sleep(2)
            selections = self.total_goals_odd_even_market.outcomes.items_as_ordered_dict
            self.assertEquals(list(selections.keys())[0], self.team_odd,
                              msg=f'{list(selections.keys())[0]} selection is not displayed')
            self.assertEquals(list(selections.keys())[1], self.team_even,
                              msg=f'{list(selections.keys())[1]} selection is not displayed')

    def test_003_tap_on_the_first_selection_inside_90_mins_switcher(self):
        """
        DESCRIPTION: Tap on the first selection inside 90 mins switcher
        EXPECTED: - Selection is highlighted inside accordion
        EXPECTED: - Selection has been added to the dashboard
        """
        self.total_goals_odd_even_market.grouping_buttons.click_button(vec.sb.HANDICAP_SWITCHERS.ninety_mins, timeout=3)
        self.__class__.selections = self.total_goals_odd_even_market.outcomes.items_as_ordered_dict

        self.selections[self.team_odd].bet_button.click()
        self.assertTrue(self.selections[self.team_odd].bet_button.is_selected(),
                        msg="odd selection is not selected")
        self.__class__.dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        self.__class__.summary_block = self.dashboard_panel.byb_summary
        outcomes = self.dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        self.__class__.dashboard_selections = list(outcomes.keys())
        if self.brand == "ladbrokes":
            self.__class__.total_goals_odds_event_market_and_selection_name = f'{self.expected_market_sections.total_goals_odd_even} ' \
                                                                              f'{self.btn_90_min.name.lower()} - {self.team_odd}'
        else:
            self.__class__.total_goals_odds_event_market_and_selection_name = f'{self.expected_market_sections.total_goals_odd_even.title()} ' \
                                                                              f'{self.btn_90_min.name.lower()} {self.team_odd.upper()}'

        self.assertIn(self.total_goals_odds_event_market_and_selection_name,
                      self.dashboard_selections, msg=f'{self.total_goals_odds_event_market_and_selection_name} selection is not added to dashboard')

    def test_004_tap_on_the_second_selection_inside_90_mins_switcher(self):
        """
        DESCRIPTION: Tap on the second selection inside 90 mins switcher
        EXPECTED: 1 selection is dashboard:
        EXPECTED: - First selection is deselected inside accordion and removed from the dashboard
        EXPECTED: - Second selection is selected inside accordion and is in the dashboard
        """
        self.selections[self.team_even].bet_button.click()
        self.assertTrue(self.selections[self.team_even].bet_button.is_selected(),
                        msg="odd selection is not selected")
        self.assertFalse(self.selections[self.team_odd].bet_button.is_selected(),
                         msg="odd selection is selected")
        outcomes = self.dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        self.__class__.dashboard_selections = list(outcomes.keys())

        self.assertNotIn(self.total_goals_odds_event_market_and_selection_name,
                         self.dashboard_selections,
                         msg=f'"{self.total_goals_odds_event_market_and_selection_name}" selection is there in'
                             f'"{self.dashboard_selections}" dashboard')
        self.assertEquals(len(self.dashboard_selections), 1,
                          msg=f'{self.dashboard_selections} selections is not there in dashboard')
        if self.brand == "ladbrokes":
            self.__class__.total_goals_even_event_market_and_selection_name = f'{self.expected_market_sections.total_goals_odd_even} ' \
                                                                              f'{self.btn_90_min.name.lower()} - {self.team_even}'
        else:
            self.__class__.total_goals_even_event_market_and_selection_name = f'{self.expected_market_sections.total_goals_odd_even.title()} ' \
                                                                              f'{self.btn_90_min.name.lower()} {self.team_even.upper()}'

        self.assertIn(self.total_goals_even_event_market_and_selection_name, self.dashboard_selections,
                      msg=f'selection {self.total_goals_even_event_market_and_selection_name} is not added to '
                          f'{self.dashboard_selections} dashboard')

    def test_005_switch_to_1st_half_tab_and_tap_on_the_first_selection(self):
        """
        DESCRIPTION: Switch to "1st half" tab and tap on the first selection
        EXPECTED: 2 selections in dashboard:
        EXPECTED: - Selection is highlighted inside accordion
        EXPECTED: - Selection has been added to the dashboard
        """
        self.total_goals_odd_even_market.grouping_buttons.click_button(
            vec.sb.HANDICAP_SWITCHERS.first_half, timeout=3)
        self.__class__.selections = self.total_goals_odd_even_market.outcomes.items_as_ordered_dict
        self.selections[self.team_odd].bet_button.click()
        self.assertTrue(self.selections[self.team_odd].bet_button.is_selected(),
                        msg="odd selection is not selected")
        outcomes = self.dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        self.__class__.dashboard_selections = list(outcomes.keys())
        if self.brand == "ladbrokes":
            total_goals_1st_half_odd__market_and_selection_name = self.total_goals_even_event_market_and_selection_name + ","f'{self.expected_market_sections.total_goals_odd_even} ' \
                                                                                                                             f'{self.EXPECTED_TOTAL_GOALS_BUTTONS[1]} - {self.team_odd}'
        else:
            total_goals_1st_half_odd__market_and_selection_name = self.total_goals_even_event_market_and_selection_name + ","f'{self.expected_market_sections.total_goals_odd_even.title()} ' \
                                                                                                                             f'{self.EXPECTED_TOTAL_GOALS_BUTTONS[1]} {self.team_odd.upper()}'

        self.__class__.actual_list_1sthalf_odd = total_goals_1st_half_odd__market_and_selection_name.split(",")
        self.assertListEqual(sorted(self.actual_list_1sthalf_odd), sorted(self.dashboard_selections),
                             msg=f'{sorted(self.actual_list_1sthalf_odd)}selection not added in'
                                 f'{sorted(self.dashboard_selections)} dashboard')
        self.assertEquals(len(self.dashboard_selections), 2,
                          msg=f'{self.dashboard_selections} selections are not there in dashboard')

    def test_006_tap_on_the_second_selection_inside_1st_half_tab(self):
        """
        DESCRIPTION: Tap on the second selection inside "1st half" tab
        EXPECTED: 2 selections in dashboard:
        EXPECTED: - First selection of "1st half" tab is deselected inside accordion and removed from the dashboard
        EXPECTED: - Second selection of "1st half" tab is selected inside accordion and is in the dashboard
        """
        self.selections[self.team_even].bet_button.click()
        self.assertTrue(self.selections[self.team_even].bet_button.is_selected(),
                        msg="odd selection is not selected")
        outcomes = self.dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        self.__class__.dashboard_selections = list(outcomes.keys())
        self.assertNotIn(self.actual_list_1sthalf_odd[1],
                         self.dashboard_selections,
                         msg=f'{self.actual_list_1sthalf_odd[1]} selection is there in {self.dashboard_selections} dashboard')
        if self.brand == "ladbrokes":
            total_goals_1st_half_even_event_market_and_selection_name = self.total_goals_even_event_market_and_selection_name + ","f'{self.expected_market_sections.total_goals_odd_even} ' \
                                                                                                                                f'{self.EXPECTED_TOTAL_GOALS_BUTTONS[1]} - {self.team_even}'
        else:
            total_goals_1st_half_even_event_market_and_selection_name = self.total_goals_even_event_market_and_selection_name + ","f'{self.expected_market_sections.total_goals_odd_even.title()} ' \
                                                                                                                                   f'{self.EXPECTED_TOTAL_GOALS_BUTTONS[1]} {self.team_even.upper()}'
        actual_list = total_goals_1st_half_even_event_market_and_selection_name.split(",")
        self.assertListEqual(sorted(actual_list), sorted(self.dashboard_selections),
                             msg=f'{sorted(actual_list)} selections not added in {sorted(self.dashboard_selections)} dashboard')
        self.assertEquals(len(self.dashboard_selections), 2,
                          msg=f'{self.dashboard_selections} selections are not there in dashboard')
