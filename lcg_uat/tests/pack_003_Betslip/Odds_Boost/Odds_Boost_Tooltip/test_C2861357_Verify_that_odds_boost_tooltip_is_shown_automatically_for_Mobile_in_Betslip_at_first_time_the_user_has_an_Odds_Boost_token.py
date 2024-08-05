import pytest
import tests
from time import sleep
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # cannot grant odds boost
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.mobile_only
@vtest
class Test_C2861357_Verify_that_odds_boost_tooltip_is_shown_automatically_for_Mobile_in_Betslip_at_first_time_the_user_has_an_Odds_Boost_token(BaseBetSlipTest, BaseSportTest):
    """
    TR_ID: C2861357
    NAME: Verify that odds boost tooltip is shown automatically for Mobile in Betslip at first time the user has an Odds Boost token
    DESCRIPTION: This test case verifies that odds boost tooltip is shown in Betslip for Mobile
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Add Odds Boost tokens for USER1 using instruction - https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
    PRECONDITIONS: **Note:** Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    PRECONDITIONS: Load application
    PRECONDITIONS: Clear Local Storage and Login with User1
    PRECONDITIONS: **Note:** Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create events
        """
        event_params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_id = list(event_params.selection_ids.values())[0]
        self.__class__.eventID = event_params.event_id
        self.__class__.team1 = event_params.team1
        user = tests.settings.odds_boost_user
        self.device.driver.delete_all_cookies()
        self.device.driver.execute_script('localStorage.clear();')
        self.device.navigate_to(url=tests.HOSTNAME)
        self.device.driver.implicitly_wait(5)
        self.site.login(username=user)

    def test_001_add_selection_to_quick_betverify_that_odds_boost_tooltip_popup_is_not_shown(self):
        """
        DESCRIPTION: Add selection to Quick Bet
        DESCRIPTION: Verify that odds boost tooltip popup is not shown
        EXPECTED: - Odds Boost popup is not shown
        EXPECTED: - BOOST button is shown in Quick Bet
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(selection_name=self.team1)
        info_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_INFORMATION, timeout=5, verify_name=False)
        self.assertFalse(info_popup, msg='Information pop-up is shown in quick bet')
        self.assertTrue(self.site.quick_bet_panel.has_odds_boost_button, msg='odds boost button is not present in quickbet')
        self.site.quick_bet_panel.add_to_betslip_button.click()
        sleep(5)
        self.site.open_betslip()

    def test_002_tap_add_to_betslip_button_and_navigate_to_betslipverify_that_odds_boost_tooltip_popup_is_shown_automatically_in_betslip(self):
        """
        DESCRIPTION: Tap 'Add to Betslip' button and Navigate to Betslip
        DESCRIPTION: Verify that odds boost tooltip popup is shown automatically in Betslip
        EXPECTED: Tooltip popup with hardcoded text is shown: 'Hit Boost to increase the odds of the bets in your betslip! You can boost up to (currency)XXX.XX total stake.'
        EXPECTED: ![](index.php?/attachments/get/7216632)
        EXPECTED: ![](index.php?/attachments/get/7216633)
        """
        self.__class__.info_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_INFORMATION, timeout=5, verify_name=False)
        self.assertTrue(self.info_popup, msg='Information pop-up is not shown')
        info_popup_name = vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP.replace("lad", "")
        self.assertEqual(self.info_popup.name, info_popup_name,
                         msg=f'"{self.info_popup.name}" is not the same as expected "{info_popup_name}"')
        info_popup_description = self.info_popup.description
        self.assertEqual(info_popup_description, vec.odds_boost.INFO_DIALOG.text,
                         msg=f'Hint text "{info_popup_description}" is not the same as expected "{vec.odds_boost.INFO_DIALOG.text}"')

    def test_003_navigate_to_local_storageverify_that_oxoddsboostseen_is_added(self):
        """
        DESCRIPTION: Navigate to Local Storage
        DESCRIPTION: Verify that 'OX.oddsBoostSeen' is added
        EXPECTED: The key is shown in Local Storage: OX.oddsBoostSeen = true
        """
        cookie_value = self.get_local_storage_cookie_value('OX.oddsBoostSeen')
        self.assertEqual(cookie_value, 'true',
                         msg=f'cookie: "{cookie_value}", is not present')

    def test_004_tap_ok_buttonverify_that_tooltip_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that tooltip popup is closed
        EXPECTED: Tooltip popup is closed
        """
        self.info_popup.click_ok()
        self.assertTrue(self.info_popup.wait_dialog_closed(timeout=5), msg='Information pop-up is not closed')

    def test_005_remove_selection_from_betslip_and_add_new_selection_to_betslipverify_that_odds_boost_tooltip_popup_is_not_shown_automatically_in_betslip(self):
        """
        DESCRIPTION: Remove selection from Betslip and add new selection to Betslip
        DESCRIPTION: Verify that odds boost tooltip popup is NOT shown automatically in Betslip
        EXPECTED: - Odds Boost popup is not shown
        EXPECTED: - 'i' icon is shown
        """
        betslip_content = self.get_betslip_content()
        betslip_content.remove_all_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_REMOVE_ALL)
        dialog.continue_button.click()
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        info_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_INFORMATION, timeout=5, verify_name=False)
        self.assertFalse(info_popup, msg='Information pop-up is shown in betslip when opened second time')
        self.__class__.info_button = self.get_betslip_content().odds_boost_header.info_button
        self.assertTrue(self.info_button.is_displayed(),
                        msg='Info button is not displayed')

    def test_006_tap_i_iconverify_that_tooltip_popup_is_shown(self):
        """
        DESCRIPTION: Tap 'i' icon
        DESCRIPTION: Verify that tooltip popup is shown
        EXPECTED: Tooltip popup with hardcoded text is shown: 'Hit Boost to increase the odds of the bets in your betslip! You can boost up to (currency)XXX.XX total stake.'
        """
        self.info_button.click()
        self.test_002_tap_add_to_betslip_button_and_navigate_to_betslipverify_that_odds_boost_tooltip_popup_is_shown_automatically_in_betslip()

    def test_007_tap_ok_buttonverify_that_tooltip_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK button
        DESCRIPTION: Verify that tooltip popup is closed
        EXPECTED: Tooltip popup is closed
        """
        self.test_004_tap_ok_buttonverify_that_tooltip_popup_is_closed()
