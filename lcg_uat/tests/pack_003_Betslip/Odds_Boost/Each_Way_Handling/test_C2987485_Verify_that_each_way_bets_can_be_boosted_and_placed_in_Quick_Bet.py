import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod Can't grant odds boost tokens on prod
# @pytest.mark.hl   Can't grant odds boost tokens on prod
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@vtest
class Test_C2987485_Verify_that_each_way_bets_can_be_boosted_and_placed_in_Quick_Bet(BaseUserAccountTest,
                                                                                     BaseBetSlipTest):
    """
    TR_ID: C2987485
    NAME: Verify that each way bets can be boosted and placed in Quick Bet
    DESCRIPTION: This test case verifies that each way bet can be boosted and placed in Quick Bet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: For creating Odds Boost tokens use instruction: https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: CREATE Odds Boost token with ANY Bet Type
    PRECONDITIONS: Add 2(two) just created odds boost tokens to USER1
    PRECONDITIONS: Login with USER1.
    """
    keep_browser_open = True
    prices = {0: '1/2', 1: '2/3'}
    username = tests.settings.betplacement_user
    bet_amount = 0.11

    def placebet_verify_receipt(self, eachway):
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Bet receipt sections not found')
        single_sections = sections.get(vec.betslip.SINGLE)
        self.assertIsNotNone(single_sections, msg='Single sections not found')
        single_section = single_sections.items_as_ordered_dict
        bet = single_section.get(self.stake_name)
        self.assertIsNotNone(bet, msg=f'Bet "{bet.name}" not found in single section')
        self.assertTrue(bet.boosted_section.icon.is_displayed(),
                        msg='Boost icon is not displayed')

        self.assertEqual(bet.boosted_section.text, vec.betslip.BOOSTED_MSG,
                         msg=f'Boosted bet text "{bet.boosted_section.text}" '
                             f'is not the same as expected "{vec.betslip.BOOSTED_MSG}"')
        self.assertEqual(bet.odds, self.boosted_odds,
                         msg=f'Boosted odds "{bet.odds}" '
                             f'are not the same as expected "{self.boosted_odds}"')
        if eachway:
            self.assertTrue(bet.ew_terms, msg="eachway msg is not displayed")
        self.assertTrue(bet.stake_currency,
                        msg=f'stake value "{bet.total_stake}" is not displayed '
                        )
        self.assertTrue(bet.estimate_returns_currency,
                        msg=f'estimate returns "{self.estimate_returns}" is not displayed'
                        )

    def tap_and_verify_odd_boosts(self):
        self.odds_boost_header.boost_button.click()
        result = wait_for_result(
            lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
            name='"BOOST" button to become "BOOSTED" button with animation',
            timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        if self.brand == 'bma':
            self.assertTrue(self.odds_boost_header.boost_button.has_boost_indicator,
                            msg='Boost button does not have boost indicator')
        else:
            self.assertIn('enabled', self.odds_boost_header.boost_button.boost_indicator,
                          msg='Boost-meter did not animate during odds boosting')
        self.__class__.boosted_odds = self.stake.boosted_odds_container.price_value
        self.assertTrue(self.stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')

    def add_stake_verify_boost(self):
        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.stake.amount_form.input.value = self.bet_amount
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header, msg='Odds boost header is not available')
        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        self.assertEqual(self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg=f'Button text "{self.odds_boost_header.boost_button.name}" '
                             f'is not the same as expected "{vec.odds_boost.BOOST_BUTTON.disabled}"')

    def test_000_precondition(self):
        """
        DESCRIPTION: Create odd boosts to user
        DESCRIPTION: Create selection from Horse Racing/Greyhounds (E/W market with LP available)
        Log in as a user from preconditions
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')
        event_params1 = self.ob_config.add_UK_racing_event(number_of_runners=2, time_to_start=1, lp_prices=self.prices)
        self.__class__.selection_id = list(event_params1.selection_ids.values())[0]
        self.__class__.expected_odds_boost_amount = 0
        self.ob_config.grant_odds_boost_token(username=self.username)
        self.expected_odds_boost_amount += 1
        self.site.login(username=self.username)

    def test_001_add_selection_from_horse_racinggreyhounds_ew_market_with_lp_available_to_quick_betadd_a_stake_to_selectionverify_that_odds_boost_button_is_available(
            self):
        """
        DESCRIPTION: Add selection from Horse Racing/Greyhounds (E/W market with LP available) to Quick Bet
        DESCRIPTION: Add a Stake to selection
        DESCRIPTION: Verify that odds boost button is available
        EXPECTED: 'BOOST' button is shown
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.add_stake_verify_boost()
        self.__class__.stake_value = self.get_betslip_content().total_stake
        self.__class__.estimate_returns = self.get_betslip_content().total_estimate_returns

    def test_002_check_each_way_checkboxverify_that_total_stake_and_total_est_return_are_updated_appropriately(self):
        """
        DESCRIPTION: Check 'Each Way' checkbox
        DESCRIPTION: Verify that Total Stake and Total Est. Return are updated appropriately
        EXPECTED: - 'Each Way' checkbox is checked
        EXPECTED: - Updated Total Stake is shown
        EXPECTED: - Updated Total Est. Returns is shown
       """
        self.stake.each_way_checkbox.click()
        self.assertTrue(self.stake.each_way_checkbox.is_selected(), msg='Each Way checkbox is not selected')
        each_way_stake = self.get_betslip_content().total_stake
        self.__class__.each_way_estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertGreater(each_way_stake, self.stake_value,
                           msg=f'Actual "Total Stake" value "{each_way_stake}" < Expected "{self.stake_value}"')
        self.assertGreater(self.each_way_estimate_returns, self.estimate_returns,
                           msg=f'Actual "Total Estimate" value "{self.estimate_returns}" < Expected "{self.each_way_estimate_returns}"')

    def test_003_tap_boost_buttonverify_that_odds_are_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted
        EXPECTED: Quick Bet is shown with appropriate elements:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds are shown
        EXPECTED: - Updated Total Est. Returns is shown
        """
        self.tap_and_verify_odd_boosts()
        self.__class__.stake_value = self.get_betslip_content().total_stake
        self.__class__.estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertTrue(self.estimate_returns == self.each_way_estimate_returns,
                        msg=f'New Potential Returns value "{self.estimate_returns}" is not updated')

    def test_004_tap_place_bet_buttonverify_that_bet_is_placed_with_each_way_stake_and_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed with each way stake and boosted odds
        EXPECTED: Bet receipt is shown with appropriate elements:
        EXPECTED: - Odds boost title
        EXPECTED: - Boosted odds
        EXPECTED: - E/W bet (2 Lines at £1.00 per line)
        EXPECTED: - Stake for this bet: currency(amount)
        EXPECTED: - Potential Returns: currency(amount)
        """
        self.placebet_verify_receipt(eachway=True)

    def test_005_tap_reuse_selection_buttonand_add_stakeverify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Tap 'Reuse selection' button
        DESCRIPTION: And add Stake
        DESCRIPTION: Verify that odds boost button is shown
        EXPECTED: 'BOOST' button is shown
        """
        self.ob_config.grant_odds_boost_token(username=self.username)
        self.expected_odds_boost_amount += 1
        self.assertTrue(self.site.bet_receipt.footer.has_reuse_selections_button(),
                        msg='Can not find "Reuse selection" button')
        self.site.bet_receipt.footer.reuse_selection_button.click()
        self.add_stake_verify_boost()

    def test_006_tap_boost_buttondo_not_check__each_way_checkbox(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Do not check 'Each Way' checkbox
        EXPECTED: Quick Bet is shown with appropriate elements:
        EXPECTED: - 'BOOSTED' button is shown
        EXPECTED: - Boosted odds are shown
        EXPECTED: - Updated TotalEst. Returns is shown
        """
        self.tap_and_verify_odd_boosts()
        self.assertFalse(self.stake.each_way_checkbox.is_selected(), msg='Each Way checkbox is selected')
        actual_estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertLess(actual_estimate_returns, self.estimate_returns,
                        msg=f'New Potential Returns value "{actual_estimate_returns}" is not updated')

    def test_007_tap_place_bet_buttonverify_that_bet_is_placed_and_boosted_odds(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that bet is placed and boosted odds
        EXPECTED: Bet receipt is shown with appropriate elements:
        EXPECTED: - Odds boost title
        EXPECTED: - Boosted odds
        EXPECTED: - Stake for this bet: currency(amount)
        EXPECTED: - Potential Returns: currency(amount)
        """
        self.placebet_verify_receipt(eachway=False)
