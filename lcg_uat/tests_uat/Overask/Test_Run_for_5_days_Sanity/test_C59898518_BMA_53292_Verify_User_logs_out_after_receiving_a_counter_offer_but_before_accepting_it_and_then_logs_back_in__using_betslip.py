import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.overask
@pytest.mark.desktop
@pytest.mark.uat
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C59898518_BMA_53292_Verify_User_logs_out_after_receiving_a_counter_offer_but_before_accepting_it_and_then_logs_back_in__using_betslip(BaseBetSlipTest):
    """
    TR_ID: C59898518
    NAME: BMA-53292: Verify User logs out after receiving a counter offer but before accepting it and then logs back in - using betslip
    """
    keep_browser_open = True
    max_bet = 1.2
    suggested_max_bet = 0.94
    prices = {'odds_home': '1/12', 'odds_draw': '1/13', 'odds_away': '1/14'}

    def test_000_precoditions(self):
        """
        DESCRIPTION: Create Event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event(lp=self.prices, max_bet=self.max_bet)
        self.__class__.eventID = event_params.event_id
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]

    def test_001_1_log_in(self):
        """
        DESCRIPTION: 1. Log in
        EXPECTED: User should be logged in
        """
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(username=self.username)

    def test_002_place_an_oa_bet_using_betslip(self):
        """
        DESCRIPTION: Place an OA bet using betslip
        EXPECTED: Bet should have gone through to OA and trader should see it in TI.
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_single_bet(number_of_stakes=1)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_003_when_the_counter_offer_is_received_log_out_of_the_application(self):
        """
        DESCRIPTION: When the counter offer is received, log out of the application
        EXPECTED: The user should be logged out
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.offer_stake(account_id=account_id, bet_id=bet_id,
                                       betslip_id=betslip_id, max_bet=self.suggested_max_bet)
        overask = self.get_betslip_content().wait_for_overask_panel(expected_result=False, timeout=10)
        self.assertFalse(overask, msg='Overask is not closed')
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        cms_overask_trader_message = self.get_overask_trader_offer()
        self.assertEqual(overask_trader_message, cms_overask_trader_message,
                         msg=f'Actual overask message: "{overask_trader_message}" is not '
                             f'equal: "{cms_overask_trader_message}" from CMS')
        overask_expires_message = self.get_betslip_content().overask_trader_section.expires_message
        cms_overask_expires_message = self.get_overask_expires_message()
        self.assertIn(cms_overask_expires_message, overask_expires_message,
                      msg=f'Overask message "{overask_expires_message}" not contain '
                          f'"{cms_overask_expires_message}" from CMS')
        if self.device_type == 'mobile':
            self.site.bet_receipt.close_button.click()
        self.site.logout()
        self.site.wait_logged_out()

    def test_004_verify_that_the_betslip_has_been_cleared(self):
        """
        DESCRIPTION: Verify that the betslip has been cleared
        EXPECTED: The betslip should have been cleared
        """
        if self.device_type == 'mobile':
            self.site.header.bet_slip_counter.click()
        betslip = self.get_betslip_content()
        no_selections_title = betslip.no_selections_title
        self.assertEqual(no_selections_title, vec.betslip.NO_SELECTIONS_TITLE,
                         msg=f'Actual message: "{no_selections_title}" '
                             f'does not match expected: "{vec.betslip.NO_SELECTIONS_TITLE}", Betslip is not empty as expected')

    def test_005_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: The user should be logged in
        """
        if self.device_type == 'mobile':
            self.site.bet_receipt.close_button.click()
        self.site.login(username=self.username)

    def test_006_verify_that_betslip_is_empty_ie_you_should_not_see_the_counter_offer_and_you_should_not_see_any_selections(self):
        """
        DESCRIPTION: Verify that betslip is empty i.e. you should not see the counter offer and you should not see any selections
        EXPECTED: No counter offer or selection should be seen in the betslip
        """
        self.test_004_verify_that_the_betslip_has_been_cleared()
