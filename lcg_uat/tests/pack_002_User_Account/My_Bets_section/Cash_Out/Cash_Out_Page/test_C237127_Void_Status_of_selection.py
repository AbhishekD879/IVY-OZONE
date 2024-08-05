import pytest

import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.bet_placement
@pytest.mark.cash_out
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.login
@pytest.mark.slow
@pytest.mark.timeout(1000)
@vtest
class Test_C237127_Void_Status_of_selection(BaseCashOutTest):
    """
    TR_ID: C237127
    NAME: Void status of selection
    DESCRIPTION: This test case verifies displaying 'Void' status on the Cash Out page
    """
    keep_browser_open = True
    num_of_events = 2
    event1_name, event2_name = None, None
    expected_status = 'void'

    def get_bet_status_from_cashout(self, bet_type, event_name):
        single_bet_name, single_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            event_names=event_name, bet_type=bet_type, number_of_bets=3)
        single_betlegs = single_bet.items_as_ordered_dict
        self.assertTrue(single_betlegs, msg=f'No bet leg was found for bet "{single_bet_name}"')
        single_betleg_name, single_betleg = list(single_betlegs.items())[0]
        self.assertTrue(single_betleg, msg=f'Cannot found betleg for event "{event_name}"')
        if single_betleg.has_icon_status():
            return single_betleg.icon.status
        else:
            return False

    def test_000_preconditions(self):
        """
        DESCRIPTION: Login as Oxygen user, create test event, add selections with deep link and place multiple bet
        """
        self.__class__.events_info = self.create_several_autotest_premier_league_football_events(
            number_of_events=self.num_of_events)
        self.__class__.event1_name = f'{self.events_info[0].event_name} {self.events_info[0].local_start_time}'
        self.__class__.event2_name = f'{self.events_info[1].event_name} {self.events_info[1].local_start_time}'

        username = tests.settings.betplacement_user
        self.site.login(username=username)

        self.open_betslip_with_selections(selection_ids=self.events_info[0].selection_ids[self.events_info[0].team1])
        self.place_single_bet()
        self.site.bet_receipt.footer.click_done()

        self.__class__.expected_betslip_counter_value = 0

        self.open_betslip_with_selections(
            selection_ids=[event_info.selection_ids[event_info.team1] for event_info in self.events_info])
        self.place_multiple_bet()
        self.site.bet_receipt.footer.click_done()

    def test_001_navigate_to_cash_out_tab(self):
        """
        DESCRIPTION: Navigate to 'Cash out' tab on 'My Bets' page/'Bet Slip' widget
        EXPECTED: * 'Cash out' tab is opened
        EXPECTED: * All bets are shown **without** any status badge (previously "Open")
        """
        self.site.open_my_bets_cashout()

        status = self.get_bet_status_from_cashout(bet_type='SINGLE',
                                                  event_name=self.event1_name)
        self.assertFalse(status, msg='Bet shown with status badge')

        status = self.get_bet_status_from_cashout(bet_type='DOUBLE',
                                                  event_name=self.event1_name)
        self.assertFalse(status, msg='Bet shown with status badge')

        status = self.get_bet_status_from_cashout(bet_type='DOUBLE',
                                                  event_name=self.event2_name)
        self.assertFalse(status, msg='Bet shown with status badge')

    def test_002_in_ob_backoffice_set_void_result_for_selection_of_event_with_placed_single_bet(self):
        """
        DESCRIPTION: In OB Backoffice set **Void** result settle for selection of event
        """
        event = self.events_info[0]
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        market_id = self.ob_config.market_ids[event.event_id][market_short_name]
        self.ob_config.result_selection(selection_id=event.selection_ids[event.team1],
                                        market_id=market_id,
                                        event_id=event.event_id,
                                        result='V',
                                        wait_for_update=True)
        self.ob_config.confirm_result(selection_id=event.selection_ids[event.team1],
                                      market_id=market_id,
                                      event_id=event.event_id,
                                      result='V',
                                      wait_for_update=True)
        self.ob_config.settle_result(selection_id=event.selection_ids[event.team1],
                                     market_id=market_id,
                                     event_id=event.event_id,
                                     result='V',
                                     wait_for_update=True)

    def test_003_check_badge_for_single_bet(self):
        """
        DESCRIPTION: Check badge on Cashout page for single bet
        EXPECTED: Bet is shown with status badge of "Void" for a few seconds and after it bet disappears from the page
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        if self.device_type == 'desktop':
            self.site.wait_content_state('Homepage', timeout=30)
            self.site.open_my_bets_cashout()
        self.__class__.event1_name = f'{self.events_info[0].event_name} FT'

        # we cannot verify badge status for single bet because it disappears too fast

        _, bet = self.site.cashout.tab_content.accordions_list.get_bet(event_names=self.event1_name,
                                                                       bet_type='SINGLE',
                                                                       raise_exceptions=False,
                                                                       number_of_bets=3)
        self.assertIsNone(bet, msg=f'Event "{self.event1_name}" did not disappear, but was expected to disappear')

    def test_004_check_badge_for_multiple_bet(self):
        """
        DESCRIPTION: Check badge on Cashout page for multiple bet
        EXPECTED: Bet is shown with status badge of "Void"
        """
        actual_status = self.get_bet_status_from_cashout(bet_type='DOUBLE',
                                                         event_name=self.event1_name)
        self.assertEqual(self.expected_status, actual_status,
                         msg=f'Actual status "{actual_status}" does not equal to expected "{self.expected_status}"')

    def test_005_refresh_my_bets_page(self):
        """
        DESCRIPTION: Refresh 'My Bets' page'
        EXPECTED: All bets and legs are shown with relevant statuses, where applied
        """
        self.test_003_check_badge_for_single_bet()
        self.test_004_check_badge_for_multiple_bet()
