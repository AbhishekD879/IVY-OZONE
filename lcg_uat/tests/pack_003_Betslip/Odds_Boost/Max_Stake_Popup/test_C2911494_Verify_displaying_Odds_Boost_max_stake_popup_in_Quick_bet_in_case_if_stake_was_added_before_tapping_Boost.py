import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Cannot grant odds boost and free bets.
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.betslip
@vtest
class Test_C2911494_Verify_displaying_Odds_Boost_max_stake_popup_in_Quick_bet_in_case_if_stake_was_added_before_tapping_Boost(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C2911494
    NAME: Verify displaying Odds Boost max stake popup in Quick bet in case if stake was added before tapping Boost
    DESCRIPTION: This test case verifies that Odds Boost max stake popup is displaying when stake is added and then BOOST button is tapped
    PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
    PRECONDITIONS: Create and Add Odds Boost token to the user, where max redemption value = 50 (50 is set by default)
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load application and Login into the application with user that has Odds Boost tokens available
    PRECONDITIONS: Add selection with appropriate odds boost available to Quickbet
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: User should have odds boost and add sp selection to bet slip
        EXPECTED: - Odds boost and selections are added.
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        username = tests.settings.default_username
        self.ob_config.grant_odds_boost_token(username=username, token_value=50)

        event_params = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '4/1'}, sp=True)
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.selection_name = list(event_params.selection_ids.keys())[0]
        self.__class__.eventID = event_params.event_id
        self.site.login(username)

    def test_001_enter_a_stake_above_the_max_redemption_value_stake_51_or_more(self):
        """
        DESCRIPTION: Enter a stake above the max redemption value (Stake =51 or more)
        EXPECTED: Stake is placed
        EXPECTED: Boost button is available
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.add_selection_to_quick_bet(outcome_name=self.selection_name)

        self.__class__.quick_bet_panel = self.site.quick_bet_panel
        wait_for_result(lambda: self.quick_bet_panel.selection.content,
                        timeout=5,
                        name='Betslip sections to load',
                        bypass_exceptions=(NoSuchElementException, StaleElementReferenceException, VoltronException),
                        )
        self.__class__.quick_bet = self.site.quick_bet_panel.selection.content
        self.quick_bet.amount_form.input.value = 51
        self.assertTrue(self.quick_bet_panel.odds_boost_button.is_displayed(), msg="odds boost button is not dispalyed")

    def test_002_tap_boost_button_and_verify_that_max_stake_popup_message_is_displayed(self):
        """
        DESCRIPTION: Tap 'Boost' button and verify that Max stake popup message is displayed
        EXPECTED: Popup is shown with appropriate elements:
        EXPECTED: - the hardcoded text:'The current total stake exceeds the Odds Boost max stake. Please adjust your total stake.' You can boost up to 50 of your total stake
        EXPECTED: - OK button
        """
        self.quick_bet_panel.odds_boost_button.click()

        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_MAX_STAKE_EXCEEDED,
            timeout=20)
        self.assertTrue(self.dialog, msg="Odss boost max stake dialog not appeared")
        message = self.dialog.description.replace('\n', " ")
        self.assertEqual(message, vec.odds_boost.MAX_STAKE_EXCEEDED.text,
                         msg=f'Actual message:"{message}" is not same as'
                             f'Expected message: "{vec.odds_boost.MAX_STAKE_EXCEEDED.text}".')
        self.assertTrue(self.dialog.has_ok_button(), msg='"Ok" button is not displayed.')

    def test_003_verify_that_popup_is_closable_by_ok_or_tapping_anywhere(self):
        """
        DESCRIPTION: Verify that popup is closable by 'OK' or tapping anywhere
        EXPECTED: Popup is closed
        """
        self.dialog.ok_button.click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
                                           timeout=20)
        self.assertFalse(dialog, msg="Odss boost max stake dialog  appeared")

    def test_004_verify_that_the_boost_is_deselected_after_popup_was_closed(self):
        """
        DESCRIPTION: Verify that the boost is deselected after popup was closed
        EXPECTED: The boost is deselected
        """
        self.assertTrue(self.quick_bet_panel.odds_boost_button.is_displayed, msg="odds boost button is not dispalyed")
        result = wait_for_result(lambda: self.quick_bet_panel.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
                                 name=' "BOOST" button is shown',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button is not shown.')
        self.assertFalse(self.quick_bet.is_original_odds_crossed, msg="original odds are boosted")

    def test_005_reduce_the_stake_amount_to_appropriate_value_50_or_less__tap_boost_button(self):
        """
        DESCRIPTION: Reduce the stake amount to appropriate value (50 or less) & tap 'Boost' button
        EXPECTED: Stake is successfully boosted
        """
        self.quick_bet.amount_form.input.value = 50
        result = wait_for_result(
            lambda: self.quick_bet_panel.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
            name=' "BOOST" button is shown',
            timeout=2)
        self.assertTrue(result, msg='"BOOST" button is not shown.')
        self.quick_bet_panel.odds_boost_button.click()
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_MAX_STAKE_EXCEEDED,
                                           timeout=20)
        self.assertFalse(dialog, msg="Odss boost max stake dialog not appeared")

        self.assertTrue(self.quick_bet.is_boosted_odds, msg="original odds not crossed out")
        result = wait_for_result(
            lambda: self.quick_bet_panel.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
            name=' "BOOSTED" button is shown',
            timeout=2)
        self.assertTrue(result, msg='"BOOST" button is not shown.')
