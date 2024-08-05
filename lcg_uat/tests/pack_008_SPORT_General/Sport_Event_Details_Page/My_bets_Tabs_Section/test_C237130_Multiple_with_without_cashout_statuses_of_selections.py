import pytest
from tests.base_test import vtest
from tests.pack_002_User_Account.My_Bets_section.Cash_Out.BaseCashOutTest import BaseCashOutTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.crl_tst2  # Coral only
@pytest.mark.crl_stg2
# @pytest.mark.crl_prod # can't set won, lost status on prod
# @pytest.mark.crl_hl
@pytest.mark.event_details
@pytest.mark.bet_placement
@pytest.mark.my_bets
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.cash_out
@pytest.mark.slow
@pytest.mark.timeout(700)
@pytest.mark.login
@vtest
class Test_C237130_Multiple_with_and_without_cashout_statuses_of_selections(BaseCashOutTest, BaseSportTest):
    """
    TR_ID: C237130
    NAME: Multiple with and without statuses of selections
    DESCRIPTION: This test case verifies displaying status of each selection on 'My Bets' tab on the Event Details page
    PRECONDITIONS: * User is logged in;
    PRECONDITIONS: * User has placed multiple bet on events with and without Cash Out offer available
    PRECONDITIONS: * All events with placed bets are active (not suspended or resulted)
    PRECONDITIONS: Use the next link in order to get information about event:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: where
    PRECONDITIONS: X.XX - current OpenBet version;
    PRECONDITIONS: XXX - event ID
    """
    keep_browser_open = True
    bet_type = 'DOUBLE'

    def update_all_selections_result(self, result='W'):
        market_short_name = self.ob_config.football_config. \
            autotest_class.autotest_premier_league.market_name.replace('|', '').replace(' ', '_').lower()
        for event in self.sub_events:
            event_id = event.event_id
            selection_id = event.selection_ids[event.team1]
            market_id = self.ob_config.market_ids[event_id][market_short_name]
            self.result_event(selection_ids=selection_id,
                              market_id=market_id,
                              event_id=event_id,
                              result=result)

    def wait_for_bet_status(self, status, timeout=10):
        self.assertTrue(self.bet.items_as_ordered_dict, msg='No one bet leg was found in bet section')
        wait_for_result(lambda: all(status == bet_leg.icon.status for _, bet_leg in self.bet.items_as_ordered_dict.items()),
                        name=f'Bet items "{self.bet.items_as_ordered_dict.keys()}" status became: "{status}"',
                        timeout=timeout)

    def verify_selection_info(self, status, timeout=30):
        self.wait_for_bet_status(status, timeout=timeout)
        bet_legs = self.bet.items_as_ordered_dict
        self.assertTrue(bet_legs, msg='No one bet leg was found in bet section')
        for bet_leg_name, bet_leg in bet_legs.items():
            actual_status = bet_leg.icon.status
            self.assertEqual(actual_status, status,
                             msg=f'Selection: "{bet_leg_name}" current status is: '
                             f'"{actual_status}", expected: "{status}"')

    def get_bet_from_my_bets_tab(self, bet_type: str, event_name: str):
        self.assertTrue(self.site.sport_event_details.my_bets.accordions_list,
                        msg='Bet list is empty')
        _, bet = self.site.sport_event_details.my_bets.accordions_list.get_bet(bet_type=bet_type,
                                                                               event_names=event_name)
        self.assertTrue(bet, msg=f'Cannot find bet for "{event_name}"')
        return bet

    def get_betleg_status(self, bet, betleg_name):
        betlegs = bet.items_as_ordered_dict
        self.assertTrue(betlegs, msg=f'There is no events inside of "{bet.name}"')
        betleg = betlegs.get(betleg_name)
        self.assertTrue(betleg, msg=f'There is no "{betleg_name}" inside of "{bet.name}"')

        return betleg.icon.status if betleg.has_icon_status(timeout=0) else 'open'

    def navigate_my_bets_tab_and_verify(self, events):
        self.__class__.sub_events = events
        self.navigate_to_edp(self.sub_events[0].event_id)
        self.site.sport_event_details.event_user_tabs_list.open_tab(tab_name=self.my_bets_tab_name)

        self.__class__.bet = self.get_bet_from_my_bets_tab(self.bet_type, self.sub_events[0].team1)

        for event in self.sub_events:
            betleg_status = self.get_betleg_status(self.bet, event.team1)
            expected_status = 'open'
            self.assertEqual(betleg_status, expected_status,
                             msg=f'Betleg status "{betleg_status}" does not equal to "{expected_status}"')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: * User is logged in;
        PRECONDITIONS: * User has placed multiple bet on events with and without Cash Out offer available
        PRECONDITIONS: * All events with placed bets are active (not suspended or resulted)
        PRECONDITIONS: Use the next link in order to get information about event:
        PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
        PRECONDITIONS: where
        PRECONDITIONS: X.XX - current OpenBet version;
        PRECONDITIONS: XXX - event ID
        """
        self.__class__.events_with_cashout = self.create_several_autotest_premier_league_football_events(
            number_of_events=3, cashout=True)
        self.__class__.events_without_cashout = self.create_several_autotest_premier_league_football_events(
            number_of_events=3, cashout=False)
        self.__class__.selections_with_cashout = [event.selection_ids[event.team1] for event in self.events_with_cashout]
        self.__class__.selections_without_cashout = [event.selection_ids[event.team1] for event in self.events_without_cashout]

        self.__class__.events = [[self.events_with_cashout[0], self.events_without_cashout[0]],
                                 [self.events_with_cashout[1], self.events_without_cashout[1]],
                                 [self.events_with_cashout[2], self.events_without_cashout[2]]]

        self.__class__.selections = [[self.events_with_cashout[0].selection_ids[self.events_with_cashout[0].team1], self.events_without_cashout[0].selection_ids[self.events_without_cashout[0].team1]],
                                     [self.events_with_cashout[1].selection_ids[self.events_with_cashout[1].team1], self.events_without_cashout[1].selection_ids[self.events_without_cashout[1].team1]],
                                     [self.events_with_cashout[2].selection_ids[self.events_with_cashout[2].team1], self.events_without_cashout[2].selection_ids[self.events_without_cashout[2].team1]]]

        self.site.login()

        for selection in self.selections:
            self.open_betslip_with_selections(selection_ids=selection)
            self.place_multiple_bet()
            self.site.bet_receipt.footer.click_done()
            self.__class__.expected_betslip_counter_value = 0

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_multiple_bet_with_without_available_cash_out(
            self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Multiple** bet with/without available cash out
        EXPECTED: * 'My bets' tab is opened
        EXPECTED: * Multiple bet is shown **without** any status badge
        """
        self.navigate_my_bets_tab_and_verify(self.events[0])

    def test_002_in_ob_backoffice_set_win_result_for_selection_of_event_with_placed_multiple_bet(self):
        """
        DESCRIPTION: In OB Backoffice set **Win** result for selection of event with placed **Multiple** bet
        EXPECTED: * Bet is shown with status badge of "Won" (in green color)
        """
        self.update_all_selections_result(result='W')
        self.verify_selection_info(status='won')

    def test_003_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_multiple_bet_with_without_available_cash_out(
            self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Multiple** bet with/without available cash out
        EXPECTED: * 'My bets' tab is opened
        EXPECTED: * Bet is shown without any status badge
        """
        self.navigate_my_bets_tab_and_verify(self.events[1])

    def test_004_in_ob_backoffice_set_lose_result_for_selection_of_event_with_placed_multiple_bet(self):
        """
        DESCRIPTION: In OB Backoffice set **Lose** result for selection of event with placed **Multiple** bet
        EXPECTED: * Bet is shown with status badge of "Lost" (in grey color)
        """
        self.update_all_selections_result(result='L')
        self.verify_selection_info(status='lost')

    def test_005_navigate_to_my_bets_tab_on_event_details_page_of_event_with_placed_multiple_bet_with_without_available_cash_out(
            self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of event with placed **Multiple** bet with/without available cash out
        EXPECTED: * 'My bets' tab is opened
        EXPECTED: * Bet is shown without any status badge
        """
        self.navigate_my_bets_tab_and_verify(self.events[2])

    def test_006_in_ob_backoffice_set_void_result_for_selection_of_event_with_placed_multiple_bet(self):
        """
        DESCRIPTION: In OB Backoffice set **Void** result for selection of event with placed **Multiple** bet
        EXPECTED: * Bet is shown with status badge of "Void" (in yellow color)
        """
        self.update_all_selections_result(result='V')
        self.verify_selection_info(status='void')

    def test_007_refresh_my_bets_page(self):
        """
        DESCRIPTION: Refresh 'My Bets' page'
        EXPECTED: * All bets and legs are shown with relevant statuses
        EXPECTED: Note: Some bets can be removed from frontend as already settled
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        for event in self.events:
            self.verify_my_bets_disappeared(event[0])
