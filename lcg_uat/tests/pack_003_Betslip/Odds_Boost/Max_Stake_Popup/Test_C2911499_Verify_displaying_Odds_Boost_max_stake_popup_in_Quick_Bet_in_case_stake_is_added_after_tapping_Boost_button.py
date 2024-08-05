import pytest
import voltron.environments.constants as vec
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod can't create OB event on prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.mobile_only
@vtest
class Test_C2911499_Verify_displaying_Odds_Boost_max_stake_popup_in_Quick_Bet_in_case_stake_is_added_after_tapping_Boost_button(BaseBetSlipTest,
                                                                                                                                BaseSportTest):
    """
    TR_ID: C2911499
    NAME: Verify displaying Odds Boost max stake popup in Quick Bet in case stake is added after tapping Boost button
    DESCRIPTION: This test case verifies displaying Odds Boost max stake popup in Quick Bet in case stake above the token max stake is added after tapping Boost button
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Create and Add Odds Boost token to the user, where max redemption value = 50 (50 is set by default, we cannot change it)
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    PRECONDITIONS: Add selection with appropriate odds boost available to Quickbet
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: User should have odds boost and added selection to quick bet
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        username = tests.settings.default_username
        self.ob_config.grant_odds_boost_token(username=username, token_value=50)
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = event_params.event_id
        self.__class__.expected_market = event_params.ss_response['event']['children'][0]['market']['name']

        self.site.login(username)

        self.navigate_to_edp(event_id=self.eventID, timeout=40)
        self.site.wait_content_state(state_name='EventDetails', timeout=60)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market)

    def test_001_tap_boost_button(self):
        """
        DESCRIPTION: Tap 'Boost' button
        EXPECTED: - 'Boost' button is enabled
        EXPECTED: - Boosted odds is shown
        """
        self.__class__.quick_bet = self.site.quick_bet_panel
        result = wait_for_result(lambda: self.quick_bet.has_odds_boost_button(timeout=5),
                                 expected_result=False,
                                 timeout=5)
        self.quick_bet.odds_boost_button.click()
        result = wait_for_result(lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        self.assertTrue(self.quick_bet.selection.content.is_boosted_odds(), msg='Boosted odds are not displayed')

        self.__class__.initial_total_est_returns = self.quick_bet.selection.bet_summary.total_estimate_returns
        self.__class__.initial_total_stake = self.site.quick_bet_panel.selection.bet_summary.total_stake

    def test_002_add_stake_stake__50_or_lessverify_that_max_stake_popup_is_not_shown(self):
        """
        DESCRIPTION: Add Stake (Stake = 50 or less)
        DESCRIPTION: Verify that max stake popup is NOT shown
        EXPECTED: - Popup is NOT shown
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Total Stake and Potential returns are updated
        """
        self.__class__.quick_bet_selection = self.site.quick_bet_panel.selection
        self.__class__.stake_amount = 49
        self.quick_bet_selection.content.amount_form.input.value = self.stake_amount

        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
                                           timeout=5)
        self.assertFalse(dialog, msg="Odds boost max stake dialog is appeared")
        self.assertTrue(self.quick_bet.selection.content.is_boosted_odds(), msg='Boosted odds are not displayed')

        self.__class__.boosted_total_est_returns = self.quick_bet.selection.bet_summary.total_estimate_returns
        self.assertNotEqual(self.boosted_total_est_returns, self.initial_total_est_returns,
                            msg=f'Boosted Total Est. Returns value "{self.boosted_total_est_returns}" '
                                f'is the same as initial value "{self.initial_total_est_returns}"')

        self.__class__.total_stake = self.site.quick_bet_panel.selection.bet_summary.total_stake
        self.assertEqual(self.total_stake, f'{self.stake_amount:.2f}',
                         msg=f'Actual "Total Stake" value "{self.total_stake}" != Expected "{self.stake_amount:.2f}"')

    def test_003_edit_stake_stake51_or_moreverify_that_max_stake_popup_is_shown(self):
        """
        DESCRIPTION: Edit Stake (Stake=51 or more)
        DESCRIPTION: Verify that Max stake popup is shown
        EXPECTED: Popup is shown with appropriate elements:
        EXPECTED: - the hardcoded text:'The current total stake exceeds the Odds Boost max stake. Please adjust your total stake.' You can boost up to 50 of your total stake
        EXPECTED: - OK button
        """
        self.quick_bet_selection.content.amount_form.input.value = 51

        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_MAX_STAKE_EXCEEDED,
            timeout=10)
        self.assertTrue(self.dialog, msg="Odds boost max stake dialog not appeared")

        message = self.dialog.description.replace('\n', " ")
        self.assertEqual(message, vec.odds_boost.MAX_STAKE_EXCEEDED.text,
                         msg=f'Actual message:"{message}" is not same as'
                             f'Expected message: "{vec.odds_boost.MAX_STAKE_EXCEEDED.text}".')
        self.assertTrue(self.dialog.has_ok_button(), msg='"Ok" button is not displayed.')

    def test_004_verify_that_popup_is_closable_by_ok_or_tapping_anywhere(self):
        """
        DESCRIPTION: Verify that popup is closable by 'OK' or tapping anywhere
        EXPECTED: Popup is closed
        """
        self.dialog.ok_button.click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
                                           timeout=5)
        self.assertFalse(dialog, msg="Odds boost max stake dialog  appeared")

    def test_005_verify_that_odds_boost_is_deselected(self):
        """
        DESCRIPTION: Verify that odds boost is deselected
        EXPECTED: The Boost is deselected
        """
        result = wait_for_result(lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOSTED" button did not change to "BOOST" button')

    def test_006_reduce_the_stake_amount_to_appropriate_value_50_or_less__tap_boost_button(self):
        """
        DESCRIPTION: Reduce the stake amount to appropriate value (50 or less) & tap 'Boost' button
        EXPECTED: - Stake is successfully boosted
        EXPECTED: - Popup is NOT shown
        EXPECTED: - Total Stake and Potential returns are updated
        """
        self.quick_bet_selection.content.amount_form.input.value = 49

        self.quick_bet.odds_boost_button.click()
        self.assertTrue(self.quick_bet.selection.content.is_boosted_odds(), msg='Boosted odds are not displayed')

        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
                                           timeout=5)
        self.assertFalse(dialog, msg="Odds boost max stake dialog is appeared")

        total_est_returns = self.quick_bet.selection.bet_summary.total_estimate_returns
        self.assertEqual(total_est_returns, self.boosted_total_est_returns,
                         msg=f'Boosted Total Est. Returns value "{total_est_returns}" '
                             f'is the same as initial value "{self.boosted_total_est_returns}"')

        actual_stake = self.site.quick_bet_panel.selection.bet_summary.total_stake
        self.assertEqual(actual_stake, self.total_stake,
                         msg=f'Actual "Total Stake" value "{actual_stake}" != Expected "{self.total_stake}"')
