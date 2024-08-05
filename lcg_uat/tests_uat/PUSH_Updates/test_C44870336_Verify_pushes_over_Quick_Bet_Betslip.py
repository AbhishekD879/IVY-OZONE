from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
import voltron.environments.constants as vec
import pytest


# @pytest.mark.prod - This test case is limited to QA2 only can't change price in prod
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.uat
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870336_Verify_pushes_over_Quick_Bet_Betslip(BaseBetSlipTest):
    """
    TR_ID: C44870336
    NAME: Verify pushes over Quick Bet/ Betslip
    DESCRIPTION: Verify pushes over Quick Bet/ Betslip
    PRECONDITIONS: User loads the https://beta-sports.coral.co.uk/ and logs in.
    PRECONDITIONS: User make one or more selections
    """
    keep_browser_open = True
    prices = {0: '1/20'}
    new_price = '1/10'
    bet_amount = 5

    def test_000_preconditions(self):
        """
        DESCRIPTION:Create an event
        EXPECTED: Event is created
        """
        event_params = self.ob_config.add_tennis_event_to_autotest_trophy(lp_prices=self.prices)
        selection_ids = event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        self.site.login()

    def test_001_user_make_a_selection_and_verify_that_the_selection_is_added_to_quick_bet_betslip(self):
        """
        DESCRIPTION: User make a selection and verify that the selection is added to Quick Bet/ Betslip
        EXPECTED: The selection is added to Quick Bet/ Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" is not added to the betslip')
        stake_name, self.__class__.stake = list(selections.items())[0]
        self.enter_stake_amount(stake=(stake_name, self.stake))

    def test_002_verify_that_when_a_push_happens_due_to_odds_changes_this_is_reflected_in_quick_bet_betslip__user_is_displayed_the_right_message__the_odds_are_changed_to_the_new_value__the_potential_returns_are_reflecting_the_new_value(self):
        """
        DESCRIPTION: Verify that when a push happens due to odds changes, this is reflected in Quick Bet/ Betslip:
        DESCRIPTION: - user is displayed the right message
        DESCRIPTION: - the odds are changed to the new value
        DESCRIPTION: - the potential returns are reflecting the new value
        EXPECTED: When a push ( odds values changes) happens, this is reflected in Quick Bet/ Betslip
        """
        est_returns_before_push = self.get_betslip_content().total_estimate_returns
        old_price = self.stake.odds
        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price)
        actual_error_betslip_msg = self.get_betslip_content().wait_for_warning_message()
        self.assertEqual(actual_error_betslip_msg, vec.Betslip.PRICE_CHANGE_BANNER_MSG,
                         msg=f'Actual BetSlip error message "{actual_error_betslip_msg}" != 'f'Expected "{vec.Betslip.PRICE_CHANGE_BANNER_MSG}" ')
        new_price = self.stake.odds
        self.assertNotEqual(old_price, new_price, msg=f'Actual price"{old_price}" is same as updated price "{new_price}')
        est_returns_after_push = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(est_returns_before_push, est_returns_after_push,
                            msg=f'Actual est_returns"{est_returns_before_push}" is same as updated est_returns "{est_returns_after_push}"')

    def test_003_verify_that_when_a_push_due_to_suspended_selectionsmarketsevents_or_na_markets_happens_this_is_reflected_in_quick_bet_betslip__user_is_displayed_the_right_message__the_odds_are_grayed_out__the_place_a_bet_button_is_grayed_out_and_not_clickableverify_that_if_selectionsmarketsevents_are_becoming_available_this_is_reflected_in_quick_betbetslip(self):
        """
        DESCRIPTION: Verify that when a push due to suspended selections/markets/events or NA markets happens, this is reflected in Quick Bet/ Betslip:
        DESCRIPTION: - user is displayed the right message
        DESCRIPTION: - the 'place a bet' button is grayed out and not clickable
        DESCRIPTION: Verify that if selections/markets/events are becoming available, this is reflected in Quick Bet/Betslip
        EXPECTED: When a push (suspended, NA) happens, this is reflected in Quick Bet/ Betslip
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)
        actual_error_betslip_msg = self.get_betslip_content().error
        self.assertEqual(actual_error_betslip_msg, vec.Betslip.SINGLE_DISABLED,
                         msg=f'Actual error "{actual_error_betslip_msg}" != Expected ' f'error "{vec.Betslip.SINGLE_DISABLED}"')
        self.assertFalse(self.get_betslip_content().bet_now_button.is_enabled(),
                         msg='"place a bet"button is not grayed out')
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=True)
        self.assertTrue(self.get_betslip_content().bet_now_button.is_displayed(),
                        msg='"place a bet"button is grayed out')
