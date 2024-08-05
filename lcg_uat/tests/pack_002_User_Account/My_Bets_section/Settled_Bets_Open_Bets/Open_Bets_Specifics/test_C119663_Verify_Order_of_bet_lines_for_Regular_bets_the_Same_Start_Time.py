import random

import pytest

import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_placement
@pytest.mark.open_bets
@pytest.mark.bet_history_open_bets
@pytest.mark.login
@vtest
class Test_C119663_Verify_Order_of_bet_lines_for_Regular_bets_the_Same_Start_Time(BaseBetSlipTest):
    """
    TR_ID: C119663
    VOL_ID: C9698264
    NAME: Verify Order of bet lines for Regular bets with the same start time
    DESCRIPTION: This test case verifies order of 'Regular' bet lines on 'Open Bets' tab when the user is logged in
    """
    keep_browser_open = True
    num_of_events = 4

    def test_001_login_create_event_and_place_bets(self):
        """
        DESCRIPTION: Login as Oxygen user, create test event, add selections with deep link and place single bets
        """
        selection_ids = []
        start_time = self.get_date_time_formatted_string(hours=1)
        for i in range(0, self.num_of_events):
            event_params = self.ob_config.add_autotest_premier_league_football_event(start_time=start_time)
            selection_ids.append(event_params.selection_ids[event_params.team1])
        self.site.login(username=tests.settings.betplacement_user)
        random.shuffle(selection_ids)
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.__class__.bet_place_info = self.place_and_validate_single_bet(number_of_stakes=self.num_of_events)
        del self.bet_place_info['total_stake']
        del self.bet_place_info['total_estimate_returns']
        self.site.bet_receipt.footer.click_done()
        self.site.wait_content_state('HomePage')

    def test_002_go_to_my_bets(self):
        """
        DESCRIPTION: Tap on 'My Bets' item on Top Menu
        EXPECTED: 'My Bets' page / 'Bet Slip' widget is opened
        EXPECTED: 'Open Bets' tab is shown next to 'Cash Out' tab
        """
        self.site.open_my_bets_cashout()
        page_title = self.site.cashout.header_line.page_title.title
        self.assertEqual(page_title, self.expected_my_bets_page_title,
                         msg='Page title "%s" doesn\'t match expected text "%s"'
                         % (page_title, self.expected_my_bets_page_title))

        expected_tabs = self.get_expected_my_bets_tabs()

        tabs = self.site.cashout.tabs_menu.items_as_ordered_dict
        self.assertListEqual(list(tabs.keys()), expected_tabs, msg=f'Actual tabs order: "{list(tabs.keys())}" '
                                                                   f'is not as expected: "{expected_tabs}"')

    def test_003_tap_open_bets_tab(self):
        """
        DESCRIPTION: Tap 'Open Bets' tab
        EXPECTED: 'Regular' sort filter is selected by default
        """
        self.site.cashout.tabs_menu.open_tab(tab_name='OPEN BETS')
        result = wait_for_result(
            lambda: self.site.open_bets.tab_content.grouping_buttons.current == self.expected_active_btn_open_bets,
            name='"%s" to became active' % self.expected_active_btn_open_bets,
            timeout=2)
        self.assertTrue(result, msg='%s sorting type is not selected by default' % self.expected_active_btn_open_bets)

    def test_004_verify_order_of_bets_within_the_same_date_panel(self):
        """
        DESCRIPTION: Verify order of bets within the same date panel
        EXPECTED: All bets are ordered chronologically by bet placement time (the most recent first)
        """
        # This validation is covered in Test_C29212_Verify_Open_Bets_Regular_Filter_For_Single_Bet step 4 validation

    def test_005_verify_oder_of_bets_with_the_same_bet_placement_time(self):
        """
        DESCRIPTION: Verify order of bets with the same bet placement time
        EXPECTED: In case of the same Event Start Time - in the order they come back from betplacement API
        """
        sections = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        actual_selection_names = []
        for section_name, selection in list(sections.items())[:self.num_of_events]:
            bet_legs = selection.items_as_ordered_dict
            bet_leg_name, bet_leg = list(bet_legs.items())[0]
            actual_selection_names.append(bet_leg.outcome_name)
        # In case of the same Event Start Time - in the order they come back from betplacement API
        self.assertListEqual(actual_selection_names, list(self.bet_place_info.keys()))
