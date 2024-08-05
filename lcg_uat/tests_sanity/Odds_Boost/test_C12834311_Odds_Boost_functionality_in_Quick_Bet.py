import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - can't grant odds boost tokens on prod
# @pytest.mark.hl - can't grant odds boost tokens on hl
@pytest.mark.high
@pytest.mark.quick_bet
@pytest.mark.bet_receipt
@pytest.mark.bet_placement
@pytest.mark.login
@pytest.mark.mobile_only
@pytest.mark.odds_boost
@pytest.mark.soc
@vtest
class Test_C12834311_Odds_Boost_functionality_in_Quick_Bet(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C12834311
    VOL_ID: C50985241
    NAME: Odds Boost functionality in Quick Bet
    DESCRIPTION: This test case verifies  Odds Boost functionality in Quick Bet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Quick Bet is enabled
    PRECONDITIONS: Generate for user Odds boost token with ANY token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add OB token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Note: Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Load application and do NOT log in
    PRECONDITIONS: Fractional odds format selected for User1
    """
    keep_browser_open = True
    bet_amount = 1
    original_potential_returns = '1.50'
    boosted_potential_returns = '1.53'

    def test_000_preconditions(self):
        """
        Create event and grant odds boost
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost', {})
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.event_id = event_params.event_id
        market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)
        selection_ids = event_params.selection_ids
        self.__class__.selection_name, self.__class__.selection_id = list(selection_ids.items())[0]
        self.__class__.username = tests.settings.odds_boost_user
        self.__class__.offer_id = self.ob_config.backend.ob.odds_boost_offer_non_adhoc.general_offer.offer_id
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id, offer_id=self.offer_id)

    def test_001_add_selection_to_the_quick_bet_and_verify_that_quick_bet_is_shown_without_boost_button(self):
        """
        DESCRIPTION: Add selection to the Quick Bet and verify that Quick Bet is shown WITHOUT 'BOOST' button
        EXPECTED: - Quick Bet is shown
        EXPECTED: - 'BOOST' button is NOT shown in Quick Bet
        """
        self.navigate_to_edp(event_id=self.event_id)
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.selection_name,
                                                           market_name=self.expected_market_name)
        self.assertFalse(self.site.quick_bet_panel.has_odds_boost_button(expected_result=False),
                         msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is shown')

    def test_002_close_quick_bet_and_login_into_application_with_a_user1_that_has_an_odds_boost_token(self):
        """
        DESCRIPTION: Close Quick Bet and Login into Application with a User1 that has an Odds Boost token
        EXPECTED: - User is logged in successfully
        EXPECTED: - The "Odds Boost" token notification is displayed
        """
        self.site.quick_bet_panel.close()
        self.site.login(username=self.username, async_close_dialogs=False,
                        ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, close_free_bets_notification=False)
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id,
                                              offer_id=self.offer_id)
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST)
        self.assertTrue(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_ODDS_BOOST}" dialog is not shown')

    def test_003_add_selection_that_is_applicable_for_odds_boost_into_the_quick_bet(self):
        """
        DESCRIPTION: Add selection that is applicable for Odds Boost into the Quick Bet
        EXPECTED: - Quick Bet is shown
        EXPECTED: - 'BOOST' button is available in Quick Bet
        EXPECTED: ![](index.php?/attachments/get/11126186)
        EXPECTED: ![](index.php?/attachments/get/11126187)
        """
        self.navigate_to_edp(event_id=self.event_id)
        bet_button = self.get_selection_bet_button(selection_name=self.selection_name,
                                                   market_name=self.expected_market_name)
        bet_button.click()
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.selection_name,
                                                           market_name=self.expected_market_name)
        self.assertTrue(self.site.quick_bet_panel.has_odds_boost_button(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not shown')

    def test_004_add_stake_to_the_selection_and_tap_boost_button(self):
        """
        DESCRIPTION: Add 'Stake' to the selection and tap 'BOOST' button
        EXPECTED: Quick Bet is displayed with the following elements:
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button
        EXPECTED: - Boosted odds are shown near original odds in a (yellow or dark blue depending on a brand) frame
        EXPECTED: - Original odds are displayed as crossed out on the left side of the boosted odds
        EXPECTED: - Updated (to reflect the boosted odds) Estimated/Potential Returns are shown
        """
        result = wait_for_result(lambda: self.site.quick_bet_panel,
                                 name='Waiting for Quick bet',
                                 timeout=10)
        self.assertTrue(result, msg='"Quick Bet" not displayed')
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.quick_bet.selection.content.amount_form.input.value = self.bet_amount
        self.quick_bet.odds_boost_button.click()

        result = wait_for_result(lambda: self.quick_bet.selection.bet_summary.total_estimate_returns ==
                                 self.boosted_potential_returns,
                                 name=f'Estimated returns to change to {self.boosted_potential_returns}',
                                 timeout=5)
        self.assertTrue(result, msg=f'Estimated Returns "{self.quick_bet.selection.bet_summary.total_estimate_returns}" '
                                    f'are not the same as expected "{self.boosted_potential_returns}"')
        self.assertEqual(self.quick_bet.odds_boost_button.name, vec.odds_boost.BOOST_BUTTON.enabled,
                         msg=f'Odds Boost button name "{self.quick_bet.odds_boost_button.name}" '
                             f'is not the same as expected "{vec.odds_boost.BOOST_BUTTON.enabled}"')
        self.assertTrue(self.quick_bet.selection.content.is_boosted_odds(), msg='Boosted odds are not displayed')
        self.assertTrue(self.quick_bet.selection.content.is_original_odds_crossed, msg='Original odds are not crossed')

    def test_005_tap_boosted_buttonverify_that_odds_boost_button_is_shown_with_animation_and_the_odds_boost_is_removed(self):
        """
        DESCRIPTION: Tap 'BOOSTED' button
        DESCRIPTION: Verify that odds boost button is shown with animation and the odds boost is removed
        EXPECTED: - 'BOOSTED' button is changed to 'BOOST' button with animation
        EXPECTED: - Original odds are shown
        EXPECTED: - Boosted odds are removed
        EXPECTED: - Estimated/Potential Returns are rolled back to match calculations for the original odds
        """
        self.quick_bet.odds_boost_button.click()
        self.assertEqual(self.quick_bet.odds_boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg=f'Odds Boost button name "{self.quick_bet.odds_boost_button.name}" '
                             f'is not the same as expected "{vec.odds_boost.BOOST_BUTTON.disabled}"')
        self.assertFalse(self.quick_bet.selection.content.is_original_odds_crossed, msg='Original odds are crossed')
        self.assertFalse(self.quick_bet.selection.content.is_boosted_odds(expected_result=False),
                         msg='Boosted odds are still displayed')
        self.assertEqual(self.original_potential_returns, self.quick_bet.selection.bet_summary.total_estimate_returns,
                         msg=f'Estimated Returns "{self.quick_bet.selection.bet_summary.total_estimate_returns}" '
                             f'are not the same as expected "{self.original_potential_returns}"')

    def test_006_tap_boost_button_one_more_time_and_then_tap_place_bet_buttonverify_that_bet_receipt_is_shown(self, decimal=False):
        """
        DESCRIPTION: Tap 'BOOST' button one more time and then tap 'Place Bet' button.
        DESCRIPTION: Verify that bet receipt is shown
        EXPECTED: Bet receipt is shown with the following elements:
        EXPECTED: - Boost icon
        EXPECTED: - Hardcoded text: "This bet has been boosted!"
        EXPECTED: - boosted odds are shown as those used for bet placement
        EXPECTED: - Estimated/Potential Returns match calculations for boosted odds
        """
        boosted_odds = '8/15' if decimal is False else '1.53'
        self.quick_bet.odds_boost_button.click()
        self.quick_bet.place_bet.click()
        bet_receipt = self.site.quick_bet_panel.bet_receipt
        self.assertTrue(bet_receipt.boosted_section.icon.is_displayed(),
                        msg='Boost icon is not displayed')
        self.assertEqual(bet_receipt.boosted_section.text, vec.betslip.BOOSTED_MSG,
                         msg=f'Boosted bet text "{bet_receipt.boosted_section.text}" '
                             f'is not the same as expected "{vec.betslip.BOOSTED_MSG}"')
        self.assertEqual(bet_receipt.odds, boosted_odds,
                         msg=f'Boosted odds "{bet_receipt.odds}" '
                             f'are not the same as expected "{boosted_odds}"')
        self.assertAlmostEqual(float(bet_receipt.estimate_returns), float(self.boosted_potential_returns), delta=0.01,
                               msg=f'Estimated returns "{bet_receipt.estimate_returns}" are not the same as expected '
                                   f'"{self.boosted_potential_returns}"')

    def test_007_provide_same_verifications_with_decimal_odds_format(self):
        """
        DESCRIPTION: Provide same verifications with decimal odds format
        """
        self.site.quick_bet_panel.close()
        self.site.logout()
        self.test_000_preconditions()
        self.test_001_add_selection_to_the_quick_bet_and_verify_that_quick_bet_is_shown_without_boost_button()
        self.test_002_close_quick_bet_and_login_into_application_with_a_user1_that_has_an_odds_boost_token()
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.test_003_add_selection_that_is_applicable_for_odds_boost_into_the_quick_bet()
        self.test_004_add_stake_to_the_selection_and_tap_boost_button()
        self.test_005_tap_boosted_buttonverify_that_odds_boost_button_is_shown_with_animation_and_the_odds_boost_is_removed()
        self.test_006_tap_boost_button_one_more_time_and_then_tap_place_bet_buttonverify_that_bet_receipt_is_shown(decimal=True)
