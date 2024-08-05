import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.waiters import wait_for_haul


# @pytest.mark.tst2   # cannot get banach events in qa environments
# @pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.reg156_fix
@pytest.mark.build_your_bet
@vtest
class Test_C1696995_Banach_Markets_with_1_switcher_90min_1st_2nd_Half_3_x_Selections_positive_cases(BaseBanachTest):
    """
    TR_ID: C1696995
    NAME: Banach. Markets with 1 switcher (90min, 1st, 2nd Half) & 3 x Selections
    DESCRIPTION: This test case verifies positive cases in functionality of switcher (90min, 1st, 2nd Half) on 'Build Your Bet' **Coral** / 'Bet Builder' **Ladbrokes** tab on EDP of event
    DESCRIPTION: Test case should be run after [Trigger selections dashboard and price][1] is passed
    DESCRIPTION: [1]: https://ladbrokescoral.testrail.com/index.php?/cases/view/2490965
    PRECONDITIONS: **Build Your Bet CMS configuration:**
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **Scope of markets with 1 switcher (90min, 1st, 2nd Half) & 3 x Selections. Select available for testing**
    PRECONDITIONS: MATCH BETTING,
    PRECONDITIONS: CORNERS MATCH BET,
    PRECONDITIONS: BOOKINGS MATCH BET,
    PRECONDITIONS: DOUBLE CHANCE
    PRECONDITIONS: To check response with markets from Banach: Open Dev Tools > XHR > **markets-grouped** request
    PRECONDITIONS: Response of selections for specific markets is to be taken from **selections** request when the market is expanded
    PRECONDITIONS: **'Build Your Bet/Bet Builder' tab on event details page is loaded and no selections are added to the dashboard**
    """
    keep_browser_open = True
    EXPECTED_MATCH_BETTIG_BUTTONS = ["90 Minutes", "1st Half", "2nd Half"]
    expected_added_selections = []
    switchers = []
    selection_to_be_removed = None

    def verify_selections_on_dashboard(self, switcher=''):
        self.assertTrue(self.site.sport_event_details.tab_content.wait_for_dashboard_panel(), msg='BYB Dashboard panel is not shown')
        dashboard_panel = self.site.sport_event_details.tab_content.dashboard_panel
        result = wait_for_result(lambda: '' != list(dashboard_panel.outcomes_section.items_as_ordered_dict.keys())[0],
                                 timeout=2,
                                 name='No empty name on dashboard')
        self.assertTrue(result, msg='Empty name on dashboard')
        outcomes = dashboard_panel.outcomes_section.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'List of outcomes is empty: "{outcomes}"')
        dashboard_selections = [i.upper() for i in list(outcomes.keys())]
        switcher = switcher.replace('2Nd', '2nd').replace('1St', '1st')
        if self.brand == 'ladbrokes':
            match_betting_market_and_selection_name = f'{self.expected_market_sections.match_betting} ' \
                                                      f'{switcher} - {self.team1}'
        else:
            match_betting_market_and_selection_name = f'{self.expected_market_sections.match_betting.title()} ' \
                f'{switcher} {self.team1.upper()}'
        if switcher not in self.switchers:
            self.switchers.append(switcher)
            self.expected_added_selections.append(match_betting_market_and_selection_name.upper())
        else:
            self.expected_added_selections.remove(self.selection_to_be_removed.upper())
            self.expected_added_selections.append(match_betting_market_and_selection_name.upper())
        self.assertEqual(sorted(list(dashboard_selections)), sorted(self.expected_added_selections),
                         msg=f'Lists with outcomes "{sorted(list(dashboard_selections))}" are not equal \n'
                             f'to list of added selections "{sorted(self.expected_added_selections)}"')

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find event with player bets markets, open its EDP
        """
        self.__class__.proxy = None
        eventID = self.get_ob_event_with_byb_market(
            market_name=self.expected_market_sections.match_betting.title())
        self.navigate_to_edp(event_id=eventID)

    def test_001_click_on_market_headers_match_betting(self):
        """
        DESCRIPTION: Click on market headers 'MATCH BETTING'
        EXPECTED: Switcher with three tabs is displayed:
        EXPECTED: * '90 MIN' (selected by default)
        EXPECTED: * '1ST HALF'
        EXPECTED: * '2ND HALF'
        """
        self.assertTrue(
            self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet),
            msg=f'"{self.expected_market_tabs.build_your_bet}" tab is not active')
        self.__class__.match_betting = self.get_market(market_name=self.expected_market_sections.match_betting.upper())
        self.assertTrue(self.match_betting, msg=f'Can not get market "{self.expected_market_sections.match_result}"')
        match_betting_switchers = list(self.match_betting.time_period_outcomes_list.items_as_ordered_dict.keys())
        self.assertEqual(match_betting_switchers, self.EXPECTED_MATCH_BETTIG_BUTTONS,
                         msg=f'Actual market headers "{match_betting_switchers}" '
                             f'are not same as expected headers: "{self.EXPECTED_MATCH_BETTIG_BUTTONS}"')
        # self.match_betting.set_market_selection(selection_index=1, time=True)
        # btn_90_min = self.match_betting.time_period_outcomes_list.items_as_ordered_dict.get(self.EXPECTED_MATCH_BETTIG_BUTTONS[0])
        # self.assertTrue(btn_90_min.is_selected(),
        #                 msg=f'"{self.EXPECTED_MATCH_BETTIG_BUTTONS[0]}" button is not selected by default')

    def test_002_tap_on_each_tab_of_the_switchers_90_min__1st_half__2nd_half(self):
        """
        DESCRIPTION: Tap on each tab of the switchers '90 MIN' / '1ST HALF' / '2ND HALF'.
        EXPECTED: Three selections (e.g. 'Burnley', 'Draw', 'Stoke') is offered as the buttons below each switcher (as per **selections request** mentioned in preconditions).
        """
        switchers = self.match_betting.time_period_outcomes_list.items_as_ordered_dict
        for name, switcher in switchers.items():
            switcher.click()
            wait_for_haul(5)
            current_tab_name = self.match_betting.time_period_outcomes_list.current
            self.assertEqual(name, current_tab_name,
                             msg=f'Actual tab: "{name}" is not same as '
                                 f'Expected tab: "{current_tab_name}" ')
            selections_list = self.match_betting.outcomes.items_as_ordered_dict
            self.assertEqual(len(selections_list.keys()), 3,
                             msg=f'Actual outcomes length: "{len(selections_list)}" is not same as '
                                 f'Expected length: "3"')
            self.__class__.selections = []
            for selection in selections_list.keys():
                self.selections.append(selections_list[selection].name)
                self.assertTrue(selections_list[selection].bet_button.is_displayed(), msg=f'selection name: "{selection}" is not displayed')

    def test_003_tap_on_the_selection_eg_burnley_from_one_of_the_switcher_tabs_eg_1st_half(self):
        """
        DESCRIPTION: Tap on the selection (e.g. 'Burnley') from one of the switcher tabs (e.g. '1ST HALF')
        EXPECTED: * Selection is highlighted inside accordion.
        EXPECTED: * Selection is added to the dashboard.
        """
        selections_list = self.match_betting.outcomes.items_as_ordered_dict[self.selections[0]]
        match_betting_selection_names = selections_list.name
        self.match_betting.outcomes.items_as_ordered_dict[self.selections[0]].bet_button.click()
        self.assertTrue(self.match_betting.outcomes.items_as_ordered_dict[self.selections[0]].is_selected(),
                        msg=f'selection name: "{match_betting_selection_names}" is not highlighted')
        self.match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            initial_counter=self.initial_counter, timeout=15)
        self.initial_counter += 1

        self.__class__.team1 = ''.join(match_betting_selection_names)
        self.verify_selections_on_dashboard(switcher=self.EXPECTED_MATCH_BETTIG_BUTTONS[2].title())

    def test_004_tap_on_the_selection_eg_draw_from_different_tab_eg_2nd_half(self):
        """
        DESCRIPTION: Tap on the selection (e.g. 'Draw') from different tab (e.g. '2ND HALF')
        EXPECTED: * Selection is highlighted inside accordion.
        EXPECTED: * Selection is added to the dashboard (2 selections are present in the dashboard).
        """
        self.match_betting.time_period_outcomes_list.items_as_ordered_dict.get(self.EXPECTED_MATCH_BETTIG_BUTTONS[1]).click()
        sleep(1)
        selections_list = self.match_betting.outcomes.items_as_ordered_dict[self.selections[0]]
        match_betting_selection_names = selections_list.name
        self.match_betting.outcomes.items_as_ordered_dict[self.selections[0]].bet_button.click()
        self.assertTrue(self.match_betting.outcomes.items_as_ordered_dict[self.selections[0]].is_selected(),
                        msg=f'selection name: "{match_betting_selection_names}" is not highlighted')
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        self.match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            initial_counter=self.initial_counter, timeout=15)
        self.initial_counter += 1
        self.__class__.team1 = ''.join(match_betting_selection_names)
        market = self.EXPECTED_MATCH_BETTIG_BUTTONS[1].title().replace('1St', '1st')
        if self.brand == 'bma':
            self.__class__.selection_to_be_removed = f'{self.expected_market_sections.match_betting.title()} ' \
                                                     f'{market} {self.team1.upper()}'
        else:
            self.__class__.selection_to_be_removed = f'{self.expected_market_sections.match_betting} ' \
                                                     f'{market} - {self.team1}'
        self.verify_selections_on_dashboard(switcher=self.EXPECTED_MATCH_BETTIG_BUTTONS[1].title())

    def test_005_tap_on_different_selection_eg_stoke_from_the_same_switcher_tab_eg_2nd_half(self):
        """
        DESCRIPTION: Tap on different selection (e.g. 'Stoke') from the same switcher tab (e.g. '2ND HALF')
        EXPECTED: * Selection is highlighted inside accordion.
        EXPECTED: * Previous selection from the same tab has been substituted with the new selection in the dashboard (2 selections are present in the dashboard )
        """
        selections_list = self.match_betting.outcomes.items_as_ordered_dict[self.selections[1]]
        match_betting_selection_names = selections_list.name
        self.match_betting.outcomes.items_as_ordered_dict[self.selections[1]].bet_button.click()
        self.assertTrue(self.match_betting.outcomes.items_as_ordered_dict[self.selections[1]].is_selected(),
                        msg=f'selection name: "{match_betting_selection_names}" is not highlighted')
        self.assertTrue(match_betting_selection_names, msg='No one selection added to Dashboard')
        self.match_betting.time_period_outcomes_list.items_as_ordered_dict.get(
            self.EXPECTED_MATCH_BETTIG_BUTTONS[1]).click()
        sleep(1)
        self.match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            initial_counter=self.initial_counter, timeout=15)
        self.initial_counter += 1
        self.__class__.team1 = ''.join(match_betting_selection_names)
        self.verify_selections_on_dashboard(switcher=self.EXPECTED_MATCH_BETTIG_BUTTONS[1].title())
