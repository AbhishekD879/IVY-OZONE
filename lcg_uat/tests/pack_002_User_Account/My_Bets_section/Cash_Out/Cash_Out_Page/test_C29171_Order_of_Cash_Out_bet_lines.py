import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.hl
# @pytest.mark.prod
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C29171_Order_of_Cash_Out_bet_lines(BaseCashOutTest):
    """
    TR_ID: C29171
    NAME: Order of Cash Out bet lines
    DESCRIPTION: This test case verifies the order of Cash Out bets on 'Cash Out' tab when the user is logged in.
    PRECONDITIONS: User is logged in
    PRECONDITIONS: Place simultaneous a few bets (in order to get the same Bet Placement Time)
    PRECONDITIONS: Place a few bets at different time (in order to get bet lines with different Bet Placement Time)
    """
    keep_browser_open = True
    first_bet_name, second_bet_name, third_bet_name = None, None, None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create several events and place bet
        """
        event1 = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=4))
        event2 = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=2))
        event3 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)
        start_time1 = event1.event_date_time
        start_time1_local = self.convert_time_to_local(date_time_str=start_time1,
                                                       future_datetime_format=self.event_card_future_time_format_pattern)
        self.__class__.first_bet_name = f'{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE} - [{event1.team1} v {event1.team2} {start_time1_local}]'
        start_time2 = event2.event_date_time
        start_time2_local = self.convert_time_to_local(date_time_str=start_time2,
                                                       future_datetime_format=self.event_card_future_time_format_pattern)
        self.__class__.second_bet_name = f'{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE} - [{event2.team1} v {event2.team2} {start_time2_local}]'
        self.__class__.third_bet_name = f'{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE} - [{event3.team1} v {event3.team2}]'
        self.site.login(username=tests.settings.betplacement_user)

        self.open_betslip_with_selections(selection_ids=(event1.selection_ids[event1.team1],
                                                         event2.selection_ids[event2.team1]))

        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=event3.selection_ids[event3.team1])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

    def test_001_open_my_bets_page(self):
        """
        DESCRIPTION: Open 'My Bets' page
        EXPECTED: 'My Bets' page is opened
        """
        self.site.open_my_bets_cashout()

    def test_002_verify_order_of_cash_out_bet_lines(self):
        """
        DESCRIPTION: Verify order of Cash Out bet lines
        EXPECTED: Cash Out bets are ordered chronologically by bet placement time/date (the most recent - first)
        """
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets found on Cashout page')
        self.assertIn(self.first_bet_name, bets)
        self.assertIn(self.third_bet_name, bets)

        first_bet_index = tuple(bets).index(self.first_bet_name)
        third_bet_index = tuple(bets).index(self.third_bet_name)
        self.assertTrue(third_bet_index < first_bet_index,
                        msg=f'Bets are not ordered chronologically. Bet "{self.first_bet_name}" '
                            f'is shown after "{self.third_bet_name}"')

    def test_003_verify_order_of_cash_out_bet_lines_with_the_same_bet_placement_time(self):
        """
        DESCRIPTION: Verify order of Cash Out bet lines with the same bet placement time
        EXPECTED: Bet lines are ordered by Event Start Time (with the earliest start time first)
        EXPECTED: In case of the same Event Start Time - in the order they come back from betplacement API (getbetDetails response)
        """
        bets = self.site.cashout.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(bets, msg='No bets found on Cashout page')
        self.assertIn(self.second_bet_name, bets)

        first_bet_index = tuple(bets).index(self.first_bet_name)
        second_bet_index = tuple(bets).index(self.second_bet_name)
        self.assertTrue(second_bet_index < first_bet_index,
                        msg=f'Bets are not ordered chronologically. Bet "{self.first_bet_name}" '
                            f'is shown after "{self.second_bet_name}"')
