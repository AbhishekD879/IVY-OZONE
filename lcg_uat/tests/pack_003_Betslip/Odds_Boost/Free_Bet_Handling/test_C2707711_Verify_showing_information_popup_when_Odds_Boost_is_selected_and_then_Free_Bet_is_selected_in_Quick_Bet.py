import pytest
import tests
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.helpers import normalize_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod #Cannot grant odds boost and free bets.
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.mobile_only
@pytest.mark.betslip
@vtest
class Test_C2707711_Verify_showing_information_popup_when_Odds_Boost_is_selected_and_then_Free_Bet_is_selected_in_Quick_Bet(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C2707711
    NAME: Verify showing information popup when Odds Boost is selected and then Free Bet is selected in Quick Bet
    DESCRIPTION: This Test case verifies that information notification with two buttons is shown when odds are boosted and then Free Bet is selected in Quick Bet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1 using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Generate for user FreeBet token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    """
    keep_browser_open = True
    free_bet_value = 1.01

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

        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.team1 = event_params.team1
        expected_market = normalize_name(self.ob_config.football_config.autotest_class.autotest_premier_league.market_name)
        self.__class__.expected_market = self.get_accordion_name_for_market_from_ss(ss_market_name=expected_market)
        self.site.login(username)
        self.navigate_to_edp(event_id=event_params.event_id, sport_name='football')

    def test_001_add_selection_with_odds_boost_available_to_quick_betverify_that_quick_bet_is_shown_with_free_bets_available_and_boost_button(self):
        """
        DESCRIPTION: Add selection (with odds boost available) to Quick Bet
        DESCRIPTION: Verify that Quick bet is shown with Free Bets available and 'Boost' button
        EXPECTED: Quick Bet is opened with following elements:
        EXPECTED: - BOOST' button
        EXPECTED: - 'Free Bets' drop down (Before OX99)
        EXPECTED: 'Use Free Bet 'button (After OX99)
        """
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.team1, market_name=self.expected_market)
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.assertTrue(self.quick_bet.selection.content.use_free_bet_link,
                        msg='"Use Free Bet" is not available')
        self.assertTrue(self.quick_bet.has_odds_boost_button(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not shown')

    def test_002_tap_boost_buttonverify_that_odds_is_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds is boosted
        EXPECTED: - Button state is changed to 'Boosted'
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is shown as crossed out
        """
        self.quick_bet.odds_boost_button.click()
        result = wait_for_result(lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        self.assertTrue(self.quick_bet.selection.content.boosted_odds_container.is_displayed(timeout=3),
                        msg='Boosted odds are not shown')
        self.assertTrue(self.quick_bet.selection.content.is_original_odds_crossed,
                        msg='Original odds are not crossed out')

    def test_003_add_one_of_the_available_free_betsverify_that_information_popup_is_displayed(self):
        """
        DESCRIPTION: Add one of the available free bets
        DESCRIPTION: Verify that information popup is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?"
        EXPECTED: - 'NO, THANKS' button
        EXPECTED: - 'YES, PLEASE' button
        """
        self.quick_bet.selection.content.use_free_bet_link.click()
        self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.free_bet_value))
        self.__class__.continue_free_bet_dialog_box = \
            self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_CONTINUE_WITH_FREE_BET, verify_name=False,
                                      timeout=5)
        self.assertTrue(self.continue_free_bet_dialog_box.yes_please_button.is_displayed(),
                        msg=f'"YES PLEASE" button not displayed on"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE} pop up')
        self.assertTrue(self.continue_free_bet_dialog_box.no_thanks_button.is_displayed(),
                        msg=f'"NO THANKS" button not displayed on "{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE} pop up')

    def test_004_tap_no_thanks_buttonverify_that_popup_is_closed_and_odds_boost_remains_selected(self):
        """
        DESCRIPTION: Tap 'NO, THANKS' button
        DESCRIPTION: Verify that popup is closed and odds boost remains selected
        EXPECTED: - Popup is closed
        EXPECTED: - Odds Boost button remains selected (show as BOOSTED)
        EXPECTED: - Odds is shown in boosted state
        EXPECTED: - Original odd remains cross out
        EXPECTED: - The free bet is deselected (removed)
        """
        self.continue_free_bet_dialog_box.no_thanks_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5, verify_name=False)
        self.assertFalse(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is shown')
        result = wait_for_result(lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        self.assertTrue(self.quick_bet.selection.content.boosted_odds_container.is_displayed(timeout=3),
                        msg='Boosted odds are not shown')
        self.assertTrue(self.quick_bet.selection.content.is_original_odds_crossed,
                        msg='Original odds are not crossed out')

    def test_005_add_one_of_the_available_free_bets_one_more_timeverify_that_information_popup_with_two_buttons_is_displayed(self):
        """
        DESCRIPTION: Add one of the available free bets one more time
        DESCRIPTION: Verify that information popup (with two buttons) is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Selecting a Free Bet will cancel your boosted price. Are you sure you want to continue?"
        EXPECTED: - 'NO, THANKS' button
        EXPECTED: - 'YES, PLEASE' button
        """
        self.test_003_add_one_of_the_available_free_betsverify_that_information_popup_is_displayed()

    def test_006_tap_yes_please_buttonverify_that_popup_is_closed_and_freebet_remains(self):
        """
        DESCRIPTION: Tap 'YES, PLEASE' button
        DESCRIPTION: Verify that popup is closed and Freebet remains
        EXPECTED: - Popup is closed
        EXPECTED: - The selected free bet remains selected
        EXPECTED: - The odds boost button is rolled back to an unboosted state (show as BOOST)
        EXPECTED: - Odds of is rolled back to an unboosted state
        """
        self.continue_free_bet_dialog_box.yes_please_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE, timeout=5, verify_name=False)
        self.assertFalse(dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE}" dialog is shown')
        self.assertTrue(self.quick_bet.selection.content.remove_free_bet_link, msg=f'"{vec.betslip.REMOVE_FREE_BET}" link was not found')
        self.assertEqual(self.quick_bet.selection.content.free_bet_stake, str(self.free_bet_value),
                         msg='The selected free bet not remains selected')
        result = wait_for_result(lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
                                 name='"BOOSTED" button to become "BOOST" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOSTED" button did not change to "BOOST" button')
