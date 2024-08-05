import pytest
import tests
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Cannot grant odds boost and free bets.
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.betslip
@vtest
class Test_C2600888_Verify_showing_information_popup_when_Odds_Boost_is_selected_and_then_Free_Bet_is_selected_in_Betslip(BaseBetSlipTest):
    """
    TR_ID: C2600888
    NAME: Verify showing information popup when Odds Boost is selected and then Free Bet is selected in Betslip
    DESCRIPTION: This Test case verifies that information notification with two buttons is shown when odds are boosted
                 and than Free Bet is selected
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Generate for user FreeBet token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add Selection with Odds Boost available to the Betslip
    """
    keep_browser_open = True
    free_bet_value = 1.03

    def test_000_pre_conditions(self):
        """
        DESCRIPTION: Login with user and place bet with boosting odds
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        username = tests.settings.default_username
        self.ob_config.grant_odds_boost_token(username=username)
        self.ob_config.grant_freebet(username=username, freebet_value=self.free_bet_value)
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_ids = self.event.selection_ids[self.event.team1]
        self.site.login(username)
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        self.site.wait_content_state_changed()

    def test_001_navigate_to_betslip_and_tap_boost_button(self):
        """
        DESCRIPTION: Navigate to Betslip and Tap 'BOOST' button
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' with animation
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is shown as crossed out
        EXPECTED: - Before OX99: Free Bet dropdown is shown
        EXPECTED: After OX99: 'Use Free Bet' button is shown
        """
        odds_boost_header = self.get_betslip_content().odds_boost_header
        odds_boost_header.boost_button.click()
        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section[self.event.team1]
        self.assertTrue(self.stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.assertTrue(self.stake.is_original_odds_crossed, msg='Original odds are not crossed out')
        self.stake.has_use_free_bet_link()
        free_bet_text = self.stake.get_free_bet_text
        self.assertEqual(free_bet_text, vec.betslip.USE_FREE_BET,
                         msg=f'Actual text: "{free_bet_text}" is not same as'
                             f'Expected text: " {vec.betslip.USE_FREE_BET}".')

    def test_002_choose_one_of_the_available_free_betsverify_that_information_popup_is_displayed(self):
        """
        DESCRIPTION: Choose one of the available free bets
        DESCRIPTION: Verify that information popup is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?"
        EXPECTED: - 'NO, THANKS' button
        EXPECTED: - 'YES, PLEASE' button
        """
        self.stake.use_free_bet_link.click()
        self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.free_bet_value))

        self.__class__.continue_free_bet_dialog_box = \
            self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_CONTINUE_WITH_FREE_BET,
                                      timeout=5)
        self.assertTrue(self.continue_free_bet_dialog_box.yes_please_button.is_displayed(),
                        msg=f'"YES PLEASE" button not displayed on"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE} pop up')
        self.assertTrue(self.continue_free_bet_dialog_box.no_thanks_button.is_displayed(),
                        msg=f'"NO THANKS" button not displayed on "{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE} pop up')

    def test_003_tap_no_thanks_buttonverify_that_popup_is_closed_and_odds_boost_remains_selected(self):
        """
        DESCRIPTION: Tap 'NO, THANKS' button
        DESCRIPTION: Verify that popup is closed and odds boost remains selected
        EXPECTED: - Popup is closed
        EXPECTED: - Odds Boost button remains selected (show as BOOSTED)
        EXPECTED: - Odds is shown in boosted state
        EXPECTED: - Original odds remains cross out
        EXPECTED: - The free bet is deselected (removed)
        """
        self.continue_free_bet_dialog_box.no_thanks_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5, verify_name=False)
        self.assertFalse(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is shown')
        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake = singles_section[self.event.team1]
        self.assertTrue(self.stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.assertTrue(self.stake.is_original_odds_crossed, msg='Original odds are not crossed out')

    def test_004_choose_one_of_the_available_free_bets_one_more_timeverify_that_information_popup_is_displayed(self):
        """
        DESCRIPTION: Choose one of the available free bets one more time
        DESCRIPTION: Verify that information popup is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?"
        EXPECTED: - 'NO, THANKS' button
        EXPECTED: - 'YES, PLEASE' button
        """
        self.test_002_choose_one_of_the_available_free_betsverify_that_information_popup_is_displayed()

    def test_005_tap_yes_please_buttonverify_that_popup_is_closed_and_freebet_remains_selected(self):
        """
        DESCRIPTION: Tap 'YES, PLEASE' button
        DESCRIPTION: Verify that popup is closed and Freebet remains selected
        EXPECTED: - Popup is closed
        EXPECTED: - The selected free bet remains selected
        EXPECTED: - The odds boost button is rolled back to an unboosted state (show as BOOST)
        EXPECTED: - Odds of is rolled back to an unboosted state
        """
        self.continue_free_bet_dialog_box.yes_please_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5, verify_name=False)
        self.assertFalse(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is shown')
        self.assertTrue(self.stake.remove_free_bet_link, msg=f'"{vec.betslip.REMOVE_FREE_BET}" link was not found')
        self.assertEqual(self.stake.free_bet_stake, str(self.free_bet_value),
                         msg='The selected free bet not remains selected')
        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
                                 name='"BOOSTED" button to become "BOOST" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOSTED" button did not change to "BOOST" button')
