import pytest
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


# @pytest.mark.prod # Can't be executed, can't create OB event on prod, can't trigger Overask appearance on prod
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.open_bets
@pytest.mark.overask
@pytest.mark.betslip
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C44870282__Double_Horse_Racing_Bet_Countered_from_EW_to_Win_Only(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C44870282
    NAME: - Double Horse Racing Bet Countered from EW to Win Only
    """
    keep_browser_open = True
    max_bet = 0.2
    suggested_max_bet = 0.25
    prices = [{0: '1/12'}, {0: '1/11'}]
    selection_ids = []

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create an event
        EXPECTED: Event is created
        """
        for i in range(2):
            event_params = self.ob_config.add_UK_racing_event(ew_terms=self.ew_terms, number_of_runners=1, lp_prices=self.prices[i], max_bet=self.max_bet)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self.selection_ids.append(list(selection_ids.values())[0])
        self.__class__.username = tests.settings.betplacement_user
        self.site.login(self.username)

    def test_001_place_an_oa_double_ew_bet(self):
        """
        DESCRIPTION: Place an OA double EW bet
        EXPECTED: The bet should have gone through to the OA flow
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.__class__.bet_amount = self.max_bet + 0.1
        self.place_multiple_bet(number_of_stakes=1, each_way=True)
        overask = self.get_betslip_content().wait_for_overask_panel(timeout=10)
        self.assertTrue(overask, msg='Overask is not triggered for the User')

    def test_002_in_the_ti_change_the_bet_from_ew_to_win_only_and_click_submit(self):
        """
        DESCRIPTION: In the TI, change the bet from EW to Win Only and click Submit
        EXPECTED: On the Front End, you should see a counter offer which is half of the original stake and you should see the text Win Only under the text
        """
        account_id, bet_id, betslip_id = \
            self.bet_intercept.find_bet_for_review(username=self.username, event_id=self.eventID)
        self.bet_intercept.change_bet_to_each_way_or_win(account_id=account_id, bet_id=bet_id, betslip_id=betslip_id,
                                                         bet_amount=self.suggested_max_bet, leg_type='W')
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

    def test_003_check_that_the_potential_returns_are_correct(self):
        """
        DESCRIPTION: Check that the Potential Returns are correct
        EXPECTED: The Potential Returns should be correct
        """
        combined_odd = self.calculate_combined_odd(self.prices)
        self.__class__.expected_return = self.get_betslip_content().total_estimate_returns
        self.verify_estimated_returns(est_returns=self.expected_return, bet_amount=self.suggested_max_bet, odds=combined_odd)

    def test_004_place_the_bet(self):
        """
        DESCRIPTION: Place the bet
        EXPECTED: The bet should have been placed and the bet receipt should be seen
        """
        self.get_betslip_content().confirm_overask_offer_button.click()
        self.check_bet_receipt_is_displayed()

    def test_005_check_that_the_bet_receipt_shows_the_correct_potential_returns(self):
        """
        DESCRIPTION: Check that the bet receipt shows the correct Potential Returns
        EXPECTED: The bet receipt should show the correct Potential Returns
        """
        actual_est_returns = self.site.bet_receipt.footer.total_estimate_returns
        self.assertEqual(actual_est_returns, self.expected_return,
                         msg=f'Actual Returns: "{actual_est_returns}" is not same as '
                             f'Expected Returns:"{self.expected_return}"')
