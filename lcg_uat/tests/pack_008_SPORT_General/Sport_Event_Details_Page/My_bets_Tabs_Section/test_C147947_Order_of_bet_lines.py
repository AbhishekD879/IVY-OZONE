import pytest

import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod
# @pytest.mark.crl_hl
@pytest.mark.bet_placement
@pytest.mark.event_details
@pytest.mark.my_bets
@pytest.mark.cash_out
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.login
@vtest
class Test_C147947_Order_of_bet_lines(BaseCashOutTest):
    """
    TR_ID: C147947
    NAME: Order of bet lines
    DESCRIPTION: This test case verifies the order of bets on 'My bets' tab on Event Details page when the user is logged in.
    """
    keep_browser_open = True
    first_bet_name, second_bet_name, third_bet_name = None, None, None
    expected_bets_list = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create several events and place bet
        """
        self.__class__.event1 = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=6))
        self.__class__.event2 = self.ob_config.add_autotest_premier_league_football_event(
            start_time=self.get_date_time_formatted_string(hours=2))
        self.__class__.event3 = self.ob_config.add_autotest_premier_league_football_event(is_live=True)

        self.site.login()
        # Adding each selection separately to know exact order of bet legs
        for selection_name, selection_id in self.event1.selection_ids.items():
            self.open_betslip_with_selections(selection_ids=selection_id)   # BMA-43396
            self.__class__.expected_bets_list.append(f'{vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE} - [{selection_name}]')

        self.__class__.expected_bets_list = list(reversed(self.expected_bets_list))
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

        self.__class__.expected_betslip_counter_value = 0
        first_event_team1, second_event_team1, third_event_team1 = \
            self.event1.team1, self.event2.team1, self.event3.team1

        self.__class__.selection_ids[third_event_team1] = self.event3.selection_ids[third_event_team1]
        self.__class__.selection_ids[first_event_team1] = self.event1.selection_ids[first_event_team1]
        self.__class__.selection_ids[second_event_team1] = self.event2.selection_ids[second_event_team1]

        multiple_selections_order = f'{third_event_team1}, {first_event_team1}, {second_event_team1}'

        # Adding each selection separately to know exact order of bet legs
        for selection_name, selection_id in self.selection_ids.items():
            self.open_betslip_with_selections(selection_ids=selection_id)

        self.place_multiple_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.close_button.click()

        self.__class__.expected_bets_list.append(f'{vec.betslip.ROB.upper()} - [{multiple_selections_order}]')
        self.__class__.expected_bets_list.append(f'{vec.betslip.BETSLIP_SINGLE_STAKES_ABOUT.format(3)} - [{multiple_selections_order}]')
        self.__class__.expected_bets_list.append(f'{vec.betslip.PAT.upper()} - [{multiple_selections_order}]')
        self.__class__.expected_bets_list.append(f'{vec.betslip.TRX.upper()} - [{multiple_selections_order}]')
        self.__class__.expected_bets_list.append(f'{vec.betslip.TBL.upper()} - [{multiple_selections_order}]')
        self.__class__.expected_bets_list.append(f'{vec.betslip.DBL.upper()} - [{multiple_selections_order}]')

    def test_001_navigate_to_event_details_my_bets_page(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed bets from preconditions
        """
        self.navigate_to_edp(event_id=self.event1.event_id)
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

    def test_002_verify_order_of_cash_out_bet_lines(self):
        """
        DESCRIPTION: Verify order of Cash Out bet lines
        EXPECTED: Cash Out bets are ordered chronologically by bet placement time/date (the most recent - first)
        """
        bets = self.site.sport_event_details.my_bets.accordions_list.items_as_ordered_dict
        actual_bets_list = list(bets.keys())
        expected_bets_list = list(reversed(self.expected_bets_list))
        self.assertListEqual(actual_bets_list, expected_bets_list,
                             msg=f'\nActual bets order:\n{actual_bets_list},\nExpected:\n{expected_bets_list}')
