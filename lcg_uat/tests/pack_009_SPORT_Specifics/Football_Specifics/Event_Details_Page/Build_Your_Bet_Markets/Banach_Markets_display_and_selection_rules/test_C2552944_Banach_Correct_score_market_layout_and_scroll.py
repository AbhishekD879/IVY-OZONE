import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from time import sleep


@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C2552944_Banach_Correct_score_market_layout_and_scroll(BaseBanachTest):
    """
    TR_ID: C2552944
    NAME: Banach. Correct score market layout and scroll
    DESCRIPTION: Test case verifies display of Correct score market, drop downs value selection, Show All/Less button, selected value display in selections grid
    DESCRIPTION: Test case should be run after [Trigger Selection Dashboard][1] is passed
    DESCRIPTION: [1]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    DESCRIPTION: Related to [Format of Correct score selections][2]
    DESCRIPTION: [2]:https://ladbrokescoral.testrail.com/index.php?/cases/view/2490706
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: **CORRECT SCORE market is present on Build Your Bet tab**
    PRECONDITIONS: **'Build Your Bet(Coral)/Bet Builder (Ladbrokes)' tab on event details page is loaded and no selections are added to the dashboard.**
    """
    keep_browser_open = True
    EXPECTED_CORRECT_SCORE_BUTTONS = ['90 mins', '1st Half', '2nd Half']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find event with Build Your Bet markets, open its EDP
        """
        self.__class__.proxy = None
        self.__class__.eventID = self.get_ob_event_with_byb_market()
        self.navigate_to_edp(event_id=self.eventID)
        self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(self.site.sport_event_details.markets_tabs_list.current,
                        msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')

    def test_001_tap_on_market_header_correct_score(self):
        """
        DESCRIPTION: Tap on market header 'CORRECT SCORE'
        EXPECTED: - Market accordion is expanded
        EXPECTED: - Three switcher tabs are displayed:
        EXPECTED: * '90 MIN' (selected by default)
        EXPECTED: * '1ST HALF'
        EXPECTED: * '2ND HALF'
        """
        self.__class__.correct_score_market = self.get_market(market_name=self.expected_market_sections.correct_score)
        self.assertTrue(self.correct_score_market.is_expanded(),
                        msg=f'"{self.expected_market_sections.correct_score}" section is not expanded')
        correct_score_switchers = self.correct_score_market.grouping_buttons.items_names

        self.assertEqual(correct_score_switchers, self.EXPECTED_CORRECT_SCORE_BUTTONS,
                         msg=f'Actual market headers "{correct_score_switchers}" '
                             f'are not same as expected headers: "{self.EXPECTED_CORRECT_SCORE_BUTTONS}"')
        btn_90_min = self.correct_score_market.grouping_buttons.current
        self.assertEquals(btn_90_min, vec.sb.HANDICAP_SWITCHERS.ninety_mins.lower(),
                          msg='90 mins tab is not selected by default')

    def test_002_tap_on_each_tab_of_the_switchers_90_min__1st_half__2nd_half(self):
        """
        DESCRIPTION: Tap on each tab of the switchers '90 MIN' / '1ST HALF' / '2ND HALF'.
        EXPECTED: - Two drop down menus under the [Home/away] team names are displayed
        EXPECTED: - ADD TO BET button as per the GD.
        EXPECTED: - "Show All" button is displayed underneath the score drop-downs
        """
        switchers = self.correct_score_market.grouping_buttons.items
        for index in range(len(switchers)):
            switchers[index].click()
            sleep(2)
            self.assertTrue(self.correct_score_market.team_away_scores.is_displayed, msg='away team is not displayed')
            self.assertTrue(self.correct_score_market.team_home_scores.is_displayed, msg='home team is not diaplayed ')
            self.assertTrue(self.correct_score_market.add_to_betslip_button.is_displayed,
                            msg='add to Bet is not displayed')
            # self.assertTrue(self.correct_score_market.has_show_all_button, msg='"SHOW ALL" button is not present')

    def test_003_in_90_mins_switcher_tab_select_the_following_score_43_and_tap_add_to_bet_button(self):
        """
        DESCRIPTION: In "90 mins" switcher tab select the following score: 4:3 and tap ADD TO BET button
        EXPECTED: "4:3" selection is added to dashboard
        """
        self.correct_score_market.grouping_buttons.click_button(vec.sb.HANDICAP_SWITCHERS.ninety_mins.lower(), timeout=3)
        team_a_scores = self.correct_score_market.team_away_scores
        team_h_scores = self.correct_score_market.team_home_scores
        team_h_scores.select_score_by_text(text='4')
        team_a_scores.select_score_by_text(text='3')
        self.correct_score_market.add_to_betslip_button.click()
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        outcomes = dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        dashboard_selections = list(outcomes.keys())
        self.assertTrue(dashboard_selections[0].find("4-3"),
                        msg=f'{dashboard_selections} selection is not added to dashboard ')

    def test_004_expand_grid_of_selections_by_tapping_show_all_buttonscroll_until_value_43(self):
        """
        DESCRIPTION: Expand grid of selections by tapping "Show All" button
        DESCRIPTION: Scroll until value "4:3"
        EXPECTED: - Selections grid is expanded and scrollable
        EXPECTED: - Selection "4:3" is highlighted in the first (Home) part of the grid
        """
        # Note: From OX-136.0.0 BYB template is changed. Hence Show all button is removed
        pass
        # self.correct_score_market.show_all_button.click()
        # self.correct_score_market.scroll_to_we()
        # outcomes = self.correct_score_market.outcome_table.home_outcomes.items
        # for index in range(len(outcomes)):
        #     if outcomes[index].bet_button.name == "4 - 3":
        #         self.assertTrue(outcomes[index].bet_button.is_selected,
        #                         msg=f'{outcomes[index].bet_button.name} is not selected')
        #         break
        # if outcomes[index].bet_button.name != "4 - 3":
        #     raise VoltronException('"4-3" button is not there/highlighted')

    def test_005_switch_to_1st_half_tab(self):
        """
        DESCRIPTION: Switch to "1st half" tab
        EXPECTED: - Tab is switched
        EXPECTED: - Selections grid is expanded
        EXPECTED: - "Show less" button is displayed
        """
        self.correct_score_market.grouping_buttons.click_button(self.EXPECTED_CORRECT_SCORE_BUTTONS[1], timeout=3)
        self.assertEquals(self.correct_score_market.grouping_buttons.current, self.EXPECTED_CORRECT_SCORE_BUTTONS[1],
                          msg='tab is not switched to 1st half')
        # self.assertTrue(self.correct_score_market.has_show_less_button, msg='"SHOW LESS" button is not present')

    def test_006_tap_on_show_less_button(self):
        """
        DESCRIPTION: Tap on "Show Less" button
        EXPECTED: - Selections grid is collapsed
        EXPECTED: - "Show All" button is shown
        """
        # From OX-136.0.0 BYB template is changed. Hence Show all button is removed
        pass
        # self.correct_score_market.show_less_button.click()
        # self.assertTrue(self.correct_score_market.has_show_all_button, msg='"SHOW ALL" button is not present')
