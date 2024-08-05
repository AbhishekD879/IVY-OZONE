import pytest
import tests
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from voltron.utils.helpers import normalize_name
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
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
class Test_C2693980_Verify_Odds_Boost_unavailable_pop_up_for_SP_in_Quickbet(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C2693980
    NAME: Verify Odds Boost unavailable pop up for SP in Quickbet
    DESCRIPTION: This test case verifies Odds Boost unavailable pop up for SP in Quickbet
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office
    PRECONDITIONS: How to add Odds boost token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: Load application and Login into the application
    """
    keep_browser_open = True
    expected_sp_odds = 'SP'

    def test_000_preconditions(self):
        """
        DESCRIPTION: User should have odds boost and add sp selection to Quickbet
        EXPECTED: - Odds boost and selections are added.
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')

        username = tests.settings.default_username
        self.ob_config.grant_odds_boost_token(username=username)

        event = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '5/2'})
        self.__class__.selection_names = list(event.selection_ids.keys())
        eventID = event.event_id
        self.__class__.market_name = self.ob_config.backend.ti.horse_racing.\
            horse_racing_live.autotest_uk.market_name.replace('|', '')

        username = tests.settings.default_username
        self.site.login(username=username)
        self.navigate_to_edp(event_id=eventID, sport_name='horse-racing')

    def test_001_add_a_selection_to_the_quickbet_with_lp_and_sp_available(self):
        """
        DESCRIPTION: Add a selection to the Quickbet with LP and SP available
        EXPECTED: Selection is added to the Quickbet
        EXPECTED: Odds Boost section is available
        """
        self.add_selection_to_quick_bet(outcome_name=self.selection_names[0])
        self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet was not shown')
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.assertTrue(self.quick_bet.has_odds_boost_button(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not shown')

    def test_002_tap_boost_buttonverify_that_odds_is_boosted(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds is boosted
        EXPECTED: - 'BOOST' button changed to 'BOOSTED'
        EXPECTED: - Original odds is shown in dropdown
        EXPECTED: - New boosted adds is shown
        """
        self.quick_bet.odds_boost_button.click()
        result = wait_for_result(lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        self.assertTrue(self.quick_bet.selection.content.boosted_odds_container.is_displayed(timeout=3),
                        msg='Boosted odds are not shown')
        self.assertTrue(self.quick_bet.selection.content.is_original_odds_crossed_for_lp_sp_dropdown,
                        msg='Original odds are not crossed out')

    def test_003_change_lp_to_spverify_that_odds_boost_unavailable_popup_is_shown(self):
        """
        DESCRIPTION: Change LP to SP
        DESCRIPTION: Verify that Odds Boost unavailable popup is shown
        EXPECTED: The popup message is shown with the following elements:
        EXPECTED: - 'Odds Boost is unavailable for SP selections.' - hardcoded text is displayed
        EXPECTED: - 'Odds Boost unavailable' - the hardcoded header text is displayed
        EXPECTED: - 'OK' button is displayed
        """
        self.quick_bet.selection.content.odds_dropdown.select_value('SP')
        self.__class__.dialog = \
            self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
                                      timeout=20)
        self.assertTrue(self.dialog, msg="Odss boost unavailable dialog not appeared")
        message = self.dialog.description
        self.assertEqual(message, vec.odds_boost.BETSLIP_DIALOG.unavailable_message,
                         msg=f'Actual message:"{message}" is not same as'
                             f'Expected message: "{vec.odds_boost.BETSLIP_DIALOG.unavailable_message}".')
        self.assertTrue(self.dialog.has_ok_button(), msg='"Ok" button is not displayed.')

    def test_004_verify_that_popup_is_closable_by_tapping_ok_or_anywhere(self):
        """
        DESCRIPTION: Verify that popup is closable by tapping 'OK' or anywhere
        EXPECTED: - Pop up is closed
        EXPECTED: - SP price is shown for selection
        EXPECTED: - The Odds boost button is de-selected back to an unboosted state
        EXPECTED: - Boosted price is rolled back to an unboosted state
        EXPECTED: - Odds boost button is tappable
        """
        self.dialog.ok_button.click()
        dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
            timeout=20)
        self.assertFalse(dialog, msg="Odss boost unavailable dialog is not closed")
        self.assertTrue(self.quick_bet.has_odds_boost_button(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not shown')
        result = wait_for_result(lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
                                 name='"BOOSTED" button to become "BOOST" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOSTED" button did not change to "BOOST" button')

        stake = self.quick_bet.selection.content.odds_value
        self.assertEqual(stake, self.expected_sp_odds,
                         msg=f'Actual odds: "{stake}" is not same as Expected odds: "{self.expected_sp_odds}"')

    def test_005_tap_boost_button(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        EXPECTED: The same Odds boost unavailable popup is displayed with the following elements:
        EXPECTED: - 'Odds Boost is unavailable for SP selections.' - hardcoded text is displayed
        EXPECTED: - 'Odds Boost unavailable' - the hardcoded header text is displayed
        EXPECTED: - 'OK' button is displayed
        """
        self.quick_bet.odds_boost_button.click()
        dialog = \
            self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
                                      timeout=20)
        self.assertTrue(dialog, msg="Odss boost unavailable dialog not appeared")

        self.assertEqual(dialog.description, vec.odds_boost.BETSLIP_DIALOG.unavailable_message,
                         msg=f'Actual message:"{dialog.description}" is not same as'
                             f'Expected message: "{vec.odds_boost.BETSLIP_DIALOG.unavailable_message}".')
        self.assertTrue(dialog.has_ok_button(), msg='"Ok" button is not displayed.')
