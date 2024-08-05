import pytest
import tests
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.prod -  In production we can not grant odds boost
@pytest.mark.uat
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870264_Verify_no_live_push_for_boosted_betslip__Betslip_does_not_show_updated_prices_message_and_update_price_for_boosted_bets_and_boosted_prices_returns_remains_same_Verify_system_shows_updated_price_messaging_and_prices_when_betslip_gets_refresh_only(BaseBetSlipTest):
    """
    TR_ID: C44870264
    NAME: "Verify no live push for boosted betslip - Betslip does not show updated prices message and update price for boosted bets, and boosted prices/returns remains same -Verify system shows updated price messaging and prices when betslip gets refresh only
    DESCRIPTION: "Verify no live push for boosted betslip
    DESCRIPTION:  Add the selections that has odds boost available
    """
    keep_browser_open = True
    prices = {0: '1/20'}
    new_price = '1/10'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load application and Login into the application
        """
        event_params = self.ob_config.add_tennis_event_to_autotest_trophy(lp_prices=self.prices)
        selection_ids = event_params.selection_ids
        self.__class__.selection_id = list(selection_ids.values())[0]
        username = tests.settings.odds_boost_user
        self.site.login(username=username)
        self.ob_config.grant_odds_boost_token(username=username, level='selection', id=self.selection_id)
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        selections = self.get_betslip_sections().Singles
        self.assertTrue(selections.keys(), msg=f'"{selections}" is not added to the betslip')
        stake_name, self.__class__.stake = list(selections.items())[0]
        self.enter_stake_amount(stake=(stake_name, self.stake))

    def test_001_verify_no_live_push_for_boosted_betslip(self):
        """
        DESCRIPTION: Verify no live push for boosted betslip
        EXPECTED: Betslip does not show updated prices message and update price for boosted bets, and boosted prices/returns remains same
        """
        odds_boost_header = self.get_betslip_content().odds_boost_header
        odds_boost_header.boost_button.click()
        self.assertTrue(odds_boost_header, msg='Odds boost header is not available')
        est_returns_before_push = self.get_betslip_content().total_estimate_returns
        self.ob_config.change_price(selection_id=self.selection_id, price=self.new_price)
        before_refresh_error_betslip_msg = self.get_betslip_content().error
        self.assertFalse(before_refresh_error_betslip_msg, msg=f'"{ before_refresh_error_betslip_msg}" message is displayed')
        est_returns_after_push = self.get_betslip_content().total_estimate_returns
        self.assertEqual(est_returns_before_push, est_returns_after_push,
                         msg=f'Actual Returns: "{est_returns_before_push}" is not same as '
                             f'Expected Returns:"{est_returns_after_push}"')

    def test_002_verify_system_shows_updated_price_messaging_and_prices_when_betslip_gets_refresh_only(self):
        """
        DESCRIPTION: Verify system shows updated price messaging and prices when betslip gets refresh only
        EXPECTED: updated price is shown only after refresh
        """
        old_price = self.stake.boosted_odds_container.price_value
        self.device.refresh_page()
        self.device.driver.implicitly_wait(5)
        self.site.header.bet_slip_counter.click()
        selections = self.get_betslip_sections().Singles
        stake = list(selections.values())[0]
        new_price = stake.boosted_odds_container.price_value
        self.assertNotEqual(old_price, new_price, msg=f'Actual price"{old_price}" is same as updated price "{new_price}')

    def test_003_verify_betslip_gets_grey_out_for_boosted_bets_when_getting_suspension_only_that_time_livepush_works_for_boosted_bets(self):
        """
        DESCRIPTION: Verify betslip gets grey out for boosted bets when getting suspension (only that time livepush works for boosted bets)
        EXPECTED: only that time livepush works for boosted bets
        """
        self.ob_config.change_selection_state(selection_id=self.selection_id, displayed=True, active=False)
        if self.brand == 'ladbrokes':
            self.device.refresh_page()
            self.site.open_betslip()
            result = wait_for_result(lambda: self.get_betslip_content().error == vec.betslip.SELECTION_DISABLED,
                                     name='Betslip error to change', timeout=10)
            self.assertTrue(result, msg=f'Bet Now section warning "{self.get_betslip_content().error}"'
                                        f'is not the same as expected: "{vec.betslip.SELECTION_DISABLED}"')
        else:
            result = wait_for_result(lambda: self.get_betslip_content().error == vec.betslip.SINGLE_DISABLED,
                                     name='Betslip error to change', timeout=10)
            self.assertTrue(result, msg=f'Bet Now section warning "{self.get_betslip_content().error}" '
                                        f'is not the same as expected: "{vec.betslip.SINGLE_DISABLED}"')
            bet_now_button = self.get_betslip_content().bet_now_button
            self.assertFalse(wait_for_result(lambda: bet_now_button.is_enabled(expected_result=False), timeout=15),
                             msg=f'"{vec.quickbet.BUTTONS.place_bet}" button is not disabled')
