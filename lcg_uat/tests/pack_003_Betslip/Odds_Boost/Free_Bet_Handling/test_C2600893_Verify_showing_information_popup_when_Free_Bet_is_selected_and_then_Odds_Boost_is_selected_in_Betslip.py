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
class Test_C2600893_Verify_showing_information_popup_when_Free_Bet_is_selected_and_then_Odds_Boost_is_selected_in_Betslip(BaseBetSlipTest):
    """
    TR_ID: C2600893
    NAME: Verify showing information popup when Free Bet is selected and then Odds Boost is selected in Betslip
    DESCRIPTION: This Test case verifies that information notification with one button is shown when Free Bet is selected and then the odds are boosted
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1 using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Generate for user FreeBet token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application
    PRECONDITIONS: Login with User1
    PRECONDITIONS: Add Selection with Odds Boost available to the Betslip
    """
    keep_browser_open = True
    free_bet_value = 1.04

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
        selection_ids = self.event.selection_ids[self.event.team1]
        self.site.login(username)
        self.open_betslip_with_selections(selection_ids=selection_ids)
        self.site.wait_content_state_changed()

    def test_001_navigate_to_betslip_and_add_one_of_the_available_free_bets_to_the_selection(self):
        """
        DESCRIPTION: Navigate to Betslip and add one of the available free bets to the selection
        EXPECTED: - The Free Bet is added
        EXPECTED: - The Odds boost section with 'BOOST' button is shown
        """
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section[self.event.team1]
        stake.has_use_free_bet_link()
        stake.use_free_bet_link.click()
        self.select_free_bet(free_bet_name=self.get_freebet_name(value=self.free_bet_value))
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
                                 name=' "BOOST" button is shown',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button is not shown.')

    def test_002_tap_boost_buttonverify_that_information_popup_with_one_button_is_displayed(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that information popup (with one button) is displayed
        EXPECTED: Information popup is displayed with the following items:
        EXPECTED: - Hardcoded text: "Continue with Free Bet? Unfortunately you can't boost your odds while using a Free Bet. Please de-select your Free Bet to boost your odds."
        EXPECTED: - 'OK, THANKS' button
        """
        if self.brand == 'bama':
            self.__class__.free_bet_name = vec.dialogs.DIALOG_MANAGER_FREE_BETS_CONTINUE_WITH_FREE_BET.upper()
        else:
            self.__class__.free_bet_name = vec.dialogs.DIALOG_MANAGER_FREE_BETS_CONTINUE_WITH_FREE_BET
        self.odds_boost_header.boost_button.click()
        continue_free_bet_dialog_box = \
            self.site.wait_for_dialog(self.free_bet_name, verify_name=False,
                                      timeout=15)
        self.assertTrue(continue_free_bet_dialog_box)
        self.__class__.ok_thanks = continue_free_bet_dialog_box.ok_thanks_button
        self.assertEqual(self.ok_thanks.name, vec.odds_boost.BETSLIP_DIALOG.ok_thanks.upper())
        self.assertTrue(continue_free_bet_dialog_box.ok_thanks_button.is_displayed(),
                        msg=f'"OK THANKS" button not displayed on "{vec.dialogs.DIALOG_MANAGER_FREE_BETS_AVAILABLE} pop up')

    def test_003_tap_ok_thanks_buttonverify_that_popup_is_closed_and_free_bet_remains_selected(self):
        """
        DESCRIPTION: Tap 'OK, THANKS' button
        DESCRIPTION: Verify that popup is closed and free bet remains selected
        EXPECTED: - Popup is closed
        EXPECTED: - The selected free bet remains selected
        EXPECTED: - The odds boost button remains in an unboosted state (show as BOOST)
        EXPECTED: - Odds of all selections on the betslip are rolled back to an unboosted state
        """
        self.ok_thanks.click()
        continue_free_bet_dialog_box = \
            self.site.wait_for_dialog(self.free_bet_name, verify_name=False,
                                      timeout=5)
        self.assertFalse(continue_free_bet_dialog_box, msg='"Free bet" dialog box is opened')
        singles_section = self.get_betslip_sections().Singles
        stake = singles_section[self.event.team1]
        self.assertTrue(stake.remove_free_bet_link, msg=f'"{vec.betslip.REMOVE_FREE_BET}" link was not found')
        self.assertEqual(stake.free_bet_stake, str(self.free_bet_value),
                         msg='The selected free bet not remains selected')
        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
                                 name='"BOOSTED" button to become "BOOST" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOSTED" button did not change to "BOOST" button')

    def test_004_tap_place_bet_buttonverify_that_bet_is_placed_with_free_bet(self):
        """
        DESCRIPTION: Tap 'Place bet' button
        DESCRIPTION: Verify that Bet is placed with Free Bet
        EXPECTED: The receipt with Free Bet Stake is shown
        """
        self.get_betslip_content().bet_now_button.click()
        self.check_bet_receipt_is_displayed()
        actual_free_bet_stake = self.site.bet_receipt.footer.total_stake
        self.assertEqual(actual_free_bet_stake, str(self.free_bet_value),
                         msg=f'Actual Stake:"{actual_free_bet_stake}" is not same as'
                             f'Expected Stake: "{str(self.free_bet_value)}".')
