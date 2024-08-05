import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.overask
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898515_Verify_selection_s_is_removed_from_betslip_if_user_logs_out_after_triggering_OA(BaseBetSlipTest):
    """
    TR_ID: C59898515
    NAME: Verify selection/s is removed from betslip if user logs out after triggering OA.
    """
    keep_browser_open = True
    device_name = tests.desktop_default
    max_bet = 0.2
    prices = {'odds_home': '1/2', 'odds_away': '1/10', 'odds_draw': '1/9'}
    new_price = '1/7'

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet)
        self.__class__.eventID = event_params.event_id
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.username = tests.settings.betplacement_user

    def test_001_login_add_selection_and_trigger_oa(self):
        """
        DESCRIPTION: Login, Add selection and trigger OA
        EXPECTED: OA should be triggered.
        """
        self.site.login(self.username, async_close_dialogs=True)
        self.__class__.user_balance = self.site.header.user_balance
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections, msg=f'"{selections}" is not added to the betslip')
        self.__class__.bet_amount = self.max_bet + 0.5
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_log_off(self):
        """
        DESCRIPTION: Log off
        EXPECTED: User should be logged off and betslip should be empty.
        """
        self.site.logout()
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='User is not logged off')
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(betslip_counter, '0',
                         msg="Betslip is not empty")

    def test_003_log_back_in(self):
        """
        DESCRIPTION: Log back in
        EXPECTED: User should be logged in and betslip should be empty
        """
        self.site.login(self.username, async_close_dialogs=True)
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(betslip_counter, '0',
                         msg="Betslip is not empty")

    def test_004_add_selection_and_trigger_oa(self):
        """
        DESCRIPTION: Add selection and trigger OA
        EXPECTED: OA triggered
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.5
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_005_log_off(self):
        """
        DESCRIPTION: Log off
        EXPECTED: user is logged off
        """
        self.site.logout()
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='User is not logged off')

    def test_006_in_ti_accept_the_bet(self):
        """
        DESCRIPTION: In TI, accept the bet.
        EXPECTED: Bet should get placed succesfully.
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.eventID)
        self.bet_intercept.accept_bet(event_id=self.eventID, bet_id=bet_id, betslip_id=betslip_id)

    def test_007_log_back_in(self):
        """
        DESCRIPTION: Log back in
        EXPECTED: Betslip should be empty, balance should be deducted for the bet accepted by trader and it should appear in My Bets.
        """
        self.site.login(self.username, async_close_dialogs=True)
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(betslip_counter, '0',
                         msg="Betslip is not empty")
        self.site.open_betslip()
        expected_user_balance = self.user_balance - float(self.bet_amount)
        self.verify_user_balance(expected_user_balance=expected_user_balance)

        self.site.open_my_bets_open_bets()
        open_bets = self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(open_bets,
                        msg='No bets found in open bet')
        bet = list(open_bets.values())[0]
        actual_stake = bet.stake.stake_value
        self.assertEqual(actual_stake, "{:.2f}".format(self.bet_amount),
                         msg=f'Actual stake "{actual_stake}" is not same as '
                             f'Expected stake "{"{:.2f}".format(self.bet_amount)}"')

    def test_008_add_selection_and_trigger_oa(self):
        """
        DESCRIPTION: Add selection and trigger OA
        EXPECTED: OA is triggered
        """
        self.test_004_add_selection_and_trigger_oa()

    def test_009_log_off(self):
        """
        DESCRIPTION: Log off
        EXPECTED: User is logged out
        """
        self.site.logout()
        self.assertTrue(self.site.header.sign_in.is_displayed(), msg='User is not logged off')

    def test_010_in_ti_make_price_offer(self):
        """
        DESCRIPTION: In TI, make price offer
        EXPECTED: Price offer should be made
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_multiple_prices(account_id=account_id, bet_id=bet_id,
                                                 betslip_id=betslip_id,
                                                 price_1=self.new_price, max_bet=self.bet_amount)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask is not closed')

    def test_011_user_add_same_selection_and_clicks_on_login_and_place_bet(self):
        """
        DESCRIPTION: User add same selection and clicks on login and place bet.
        EXPECTED: User should be logged in
        EXPECTED: User will not see price offer made by the trader
        EXPECTED: Also, another OA bet will be triggered.
        """
        self.site.login(self.username, async_close_dialogs=True)
        betslip_counter = self.site.header.bet_slip_counter.counter_value
        self.assertEqual(betslip_counter, '0',
                         msg="Betslip is not empty")
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')
