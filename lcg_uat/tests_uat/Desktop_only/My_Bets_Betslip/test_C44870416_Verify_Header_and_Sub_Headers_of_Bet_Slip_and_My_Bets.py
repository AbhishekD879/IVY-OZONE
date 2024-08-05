import pytest
import tests
from tests.base_test import vtest
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod -->only applicable for QA2 as it involving suspention of events
@pytest.mark.p2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C44870416_Verify_Header_and_Sub_Headers_of_Bet_Slip_and_My_Bets(BaseBetSlipTest):
    """
    TR_ID: C44870416
    NAME: Verify Header and Sub -Headers of Bet Slip and My Bets.
    DESCRIPTION: This TC is to verify contents of Bet Slip and My Bets in desktop.
    """
    keep_browser_open = True
    bir_delay = 30
    device_name = tests.desktop_default

    def test_001_check_user_sees_following_headers_and_sub_headers__betslip__my_bets_cash_out_open_bets_settled_bets(self):
        """
        DESCRIPTION: "Check user sees following headers and sub-headers
        DESCRIPTION: - Betslip
        DESCRIPTION: - My Bets
        DESCRIPTION: . Cash Out
        DESCRIPTION: . Open bets
        DESCRIPTION: . Settled Bets
        EXPECTED: User is able to see
        EXPECTED: - BETSLIP
        EXPECTED: - MY BETS
        EXPECTED: . CASH OUT
        EXPECTED: . OPEN BETS
        EXPECTED: . SETTLED BETS
        """
        actual_header_tabs = list(self.site.betslip.betslip_tabs.items_as_ordered_dict.keys())
        self.assertEqual(self.required_bet_slip_tabs, actual_header_tabs, msg=f'"{actual_header_tabs}" is not same as expected "{self.required_bet_slip_tabs}"')
        self.site.open_my_bets()
        actual_my_bet_tabs = list(self.site.betslip.tabs_menu.items_as_ordered_dict.keys())
        self.assertEqual(vec.bet_history.mybets_tab, actual_my_bet_tabs, msg=f'"{actual_my_bet_tabs}" is not same as expected "{vec.bet_history.mybets_tab}"')

    def test_002_betslip__no_selections_message___check_user_sees_your_betslip_is_empty_message_when_no_selections_in_their_betsliplogged_in_or_out(self):
        """
        DESCRIPTION: BETSLIP- NO SELECTIONS MESSAGE - Check user sees ''Your Betslip is empty'' message when no selections in their betslip((logged in or out))
        EXPECTED: User sees ''Your betslip is empty'  message when no selections in their betslip (logged in or out).
        """
        self.site.betslip.betslip_tabs.items_as_ordered_dict.get('BETSLIP').click()
        message = self.site.betslip.no_selections_title
        self.assertEqual(message, vec.betslip.NO_SELECTIONS_TITLE, msg=f'"{message}" is not same as expected "{vec.betslip.NO_SELECTIONS_TITLE}"')

    def test_003_betslip__with_selections____check__user_sees_their_betsadded_selections_when_they_view_their_betslip_logged_in_or_logged_out_and_betslip_count_with_number_of_selection(self):
        """
        DESCRIPTION: BETSLIP- WITH SELECTIONS  - Check  user sees their bets(added selections) when they view their betslip (logged in or logged out) and Betslip count with number of selection
        EXPECTED: User is able to see their bets(added selections) when they view their betslip (logged in or logged out) and Betslip count with number of selections.
        """
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(is_live=True, default_market_name='|Draw No Bet|')
        self.__class__.event2 = self.ob_config.add_autotest_premier_league_football_event(is_live=True, default_market_name='|Draw No Bet|')
        self.__class__.teams = [self.event.team1, self.event2.team2]
        self.__class__.selection_id_1 = self.event.selection_ids[self.event.team1]
        self.__class__.selection_id_2 = self.event2.selection_ids[self.event2.team2]
        self.open_betslip_with_selections(selection_ids=(self.selection_id_1, self.selection_id_2))

    def test_004_betslip__suspended_selections___check_user_is_seeing__signposting_and_messages_for_suspended_selections_as_belowheader_some_of_your_selections_have_been_suspendedgreyed_out_bet_with_suspended_labelfooter_some_of_your_selections_have_been_suspended(self):
        """
        DESCRIPTION: BETSLIP- SUSPENDED SELECTIONS - Check user is seeing  signposting and messages for suspended selections as below
        DESCRIPTION: Header: Some of your selections have been suspended
        DESCRIPTION: Greyed out bet with suspended label
        DESCRIPTION: Footer: Some of your selections have been suspended"
        EXPECTED: User should see
        EXPECTED: Header: Some of your selections have been suspended
        EXPECTED: Greyed out bet with suspended label
        EXPECTED: Footer: Some of your selections have been suspended"
        """
        self.ob_config.change_selection_state(self.selection_id_1, displayed=True, active=False)
        self.ob_config.change_selection_state(self.selection_id_2, displayed=True, active=False)
        self.device.refresh_page()
        self.site.open_betslip()
        result = wait_for_result(lambda: self.get_betslip_content().error == vec.betslip.MULTIPLE_DISABLED,
                                 name='Betslip error to change', timeout=10)
        self.assertTrue(result, msg=f'Bet Now section warning "{self.get_betslip_content().error}"'
                                    f'is not the same as expected: "{vec.betslip.MULTIPLE_DISABLED}"')
        singles_section = self.get_betslip_sections().Singles
        for i in range(2):
            self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[i]
            self.assertEqual(self.stake_name, self.teams[i],
                             msg=f'Expected Selection "{self.teams[i]}" is not matching with Actual selection '
                                 f'"{self.stake_name}" on the betslip')
            result = wait_for_result(lambda: self.stake.suspended_stake_label, name='SUSPENDED label to appear', timeout=self.bir_delay)
            self.assertEqual(result.strip('"'), vec.betslip.SUSPENDED_LABEL, msg=f'{vec.betslip.SUSPENDED_LABEL} does not appear Actual content "{result}"')
