import pytest
import tests
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
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
class Test_C2600787_Verify_displaying_odds_boost_unavailable_popup_for_SP_in_Betslip_Multiple_Selection(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C2600787
    NAME: Verify displaying odds boost unavailable popup for SP in Betslip (Multiple Selection)
    DESCRIPTION: This test case verifies that a clear message that Odds Boost is not available for SP Bets is showing in Betslip
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application and Login into the application
    PRECONDITIONS: Add selection with SP only available (Selection_1)
    PRECONDITIONS: Add selection with LP and SP available (Selection_2) and LP price is selected
    PRECONDITIONS: Add selection with LP and SP available (Selection_3) and LP price is selected
    """
    keep_browser_open = True
    free_bet_value = 1.03
    expected_sp_odds = 'SP'

    def odds_boost_unavailable_dialog_verification(self):
        self.__class__.dialog = \
            self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
                                      timeout=20)
        self.assertTrue(self.dialog, msg="Odss boost unavailable dialog not appeared")
        message = self.dialog.description
        self.assertEqual(message, vec.odds_boost.BETSLIP_DIALOG.unavailable_message,
                         msg=f'Actual message:"{message}" is not same as'
                             f'Expected message: "{vec.odds_boost.BETSLIP_DIALOG.unavailable_message}".')
        self.assertTrue(self.dialog.has_ok_button(), msg='"Ok" button is not displayed.')

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
        self.ob_config.grant_odds_boost_token(username=username)
        self.ob_config.grant_freebet(username=username, freebet_value=self.free_bet_value)

        event_params_1 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp=False, sp=True)
        event_params_2 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '5/2'})
        event_params_3 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '4/1'})
        self.__class__.selection_id_1 = list(event_params_1.selection_ids.values())[0]
        self.__class__.selection_id_2 = list(event_params_2.selection_ids.values())[0]
        self.__class__.selection_id_3 = list(event_params_3.selection_ids.values())[0]
        self.site.login(username)

    def test_001_navigate_to_betslipverify_that_the_odds_boost_section_is_shown_in_the_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip
        DESCRIPTION: Verify that the Odds Boost section is shown in the Betslip
        EXPECTED: Odds Boost section is shown on the top of Betslip with the following elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - 'Tap to boost your betslip' text
        EXPECTED: - 'i' icon (tooltip)
        """
        self.open_betslip_with_selections(selection_ids=[self.selection_id_1, self.selection_id_2, self.selection_id_3])
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        self.assertTrue(self.odds_boost_header.boost_button.is_displayed(),
                        msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is not displayed')
        self.assertEqual(self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled,
                         msg='Button text label "%s" is not the same as expected "%s"' %
                             (self.odds_boost_header.boost_button.name, vec.odds_boost.BOOST_BUTTON.disabled))
        actual_text = self.odds_boost_header.tap_to_boost_your_betslip_label.text
        self.assertEqual(actual_text, vec.odds_boost.BETSLIP_HEADER.subtitle,
                         msg=f'Actual Text: "{actual_text}" is not same as Expected text: "{vec.odds_boost.BETSLIP_HEADER.subtitle}"')
        self.assertTrue(self.odds_boost_header.info_button.is_displayed(), msg='"i" button is not displayed')

    def test_002_add_stake_and_tap_a_boost_button(self):
        """
        DESCRIPTION: Add Stake and tap a 'BOOST' button
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED'
        EXPECTED: - 'i' icon is shown for Selection_1
        EXPECTED: - Boosted odds is NOT shown for Selection_1
        EXPECTED: - Boosted odds is shown for Section_2 and Selection_3
        EXPECTED: - Original odds is displayed for Selection_2 and Selection_3 in dropdown
        EXPECTED: - N/A is shown Returns
        """
        sections = self.get_betslip_sections().Singles
        for stake in list(sections.values()):
            stake.amount_form.input.value = 1
        self.odds_boost_header.boost_button.click()
        result = wait_for_result(lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        events_list = list(sections.ordered_collection.values())
        self.__class__.event_1 = events_list[0]
        self.__class__.event_2 = events_list[1]
        event_3 = events_list[2]
        self.assertTrue(self.event_1.has_odds_boost_info_icon(expected_result=True),
                        msg='Odds boost info icon not shown')
        self.assertFalse(self.event_1.has_boosted_odds, msg='Boosted odds are shown')
        self.assertTrue(self.event_2.has_boosted_odds, msg='Boosted odds are  not shown')
        self.assertTrue(event_3.has_boosted_odds, msg='Boosted odds are  not shown')
        self.assertTrue(self.event_2.is_original_odds_crossed_for_lp_sp_dropdown,
                        msg='Original odds are not crossed out')
        self.assertTrue(event_3.is_original_odds_crossed_for_lp_sp_dropdown,
                        msg='Original odds are not crossed out')

        total_estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertEqual(total_estimate_returns, 'N/A',
                         msg=f'Total Est returns is "{total_estimate_returns}" not "N/A"')

    def test_003_tap_i_icon_for_selection_1verify_that_notification_is_shown(self):
        """
        DESCRIPTION: Tap 'i' icon for Selection_1
        DESCRIPTION: Verify that notification is shown
        EXPECTED: Notification is displayed with the hardcoded text: 'Odds Boost is unavailable for this selection'
        """
        self.event_1.odds_boost_info_icon.click()
        self.assertTrue(self.event_1.has_odds_boost_tooltip(),
                        msg='Odds Boost is unavailable for this selection')
        actual_text = self.event_1.odds_boost_tooltip()
        self.assertEqual(actual_text.text, vec.odds_boost.INFO_DIALOG.odds_boost_unavailable,
                         msg=f'Actual text: "{actual_text.text}" is not same as'
                             f'Expected text: "{vec.odds_boost.INFO_DIALOG.odds_boost_unavailable}"')

    def test_004_change_lp_to_sp_for_selection_2verify_that_odds_boost_popup_is_shown(self):
        """
        DESCRIPTION: Change LP to SP for Selection_2
        DESCRIPTION: Verify that Odds Boost popup is shown
        EXPECTED: The popup message is shown with the following elements:
        EXPECTED: - hardcoded 'Odds Boost Unavailable' title
        EXPECTED: - hardcoded 'Odds Boost is unavailable for SP selection' message text
        EXPECTED: - 'OK' button
        """
        self.event_2.odds_dropdown.select_value('SP')
        self.site.betslip._load_complete()
        sections = self.get_betslip_sections().Singles
        events_list = list(sections.ordered_collection.values())
        event_2 = events_list[1]
        selected_option = event_2.odds
        self.assertEqual(selected_option, 'SP', msg=f'"SP" is not selected have "{selected_option}" instead')
        self.odds_boost_unavailable_dialog_verification()

    def test_005_tap_ok_buttonverify_that_odds_boost_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that Odds boost popup is closed
        EXPECTED: - The popup is closed
        EXPECTED: - Odds boost button is de-selected ('BOOST' button is shown)
        EXPECTED: - 'i' icon is NOT shown for Selection_1
        EXPECTED: - SP price is shown for Selection_1 and Selection_2
        EXPECTED: - Selection_3 is rolled back to an UNboosted state
        EXPECTED: - N/A is shown for returns
        """
        self.dialog.ok_button.click()
        dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
            timeout=20)
        self.assertFalse(dialog, msg="Odss boost unavailable dialog is not closed")
        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(
            lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
            name=' "BOOST" button is shown',
            timeout=2)
        self.assertTrue(result, msg='"BOOST" button is not shown.')

        sections = self.get_betslip_sections().Singles
        events_list = list(sections.ordered_collection.values())
        event_1 = events_list[0]
        event_2 = events_list[1]
        event_3 = events_list[2]
        self.assertFalse(event_1.has_odds_boost_info_icon(expected_result=False), msg='Odds boost info icon shown')
        self.assertEqual(self.event_1.odds, self.expected_sp_odds,
                         msg=f'Actual odds: "{event_1.odds}" is not same as Expected odds: "{self.expected_sp_odds}"')
        self.assertEqual(event_2.odds, self.expected_sp_odds,
                         msg=f'Actual odds: "{event_2.odds}" is not same as Expected odds: "{self.expected_sp_odds}"')
        self.assertFalse(event_3.has_boosted_odds, msg='Boosted odds are shown')
        total_estimate_returns = self.get_betslip_content().total_estimate_returns
        self.assertEqual(total_estimate_returns, 'N/A',
                         msg=f'Total Est returns is "{total_estimate_returns}" not "N/A"')

    def test_006_tap_boost_button_one_more_timeverify_that_odds_boost_popup_is_shown(self):
        """
        DESCRIPTION: Tap 'BOOST' button one more time
        DESCRIPTION: Verify that Odds boost popup is shown
        EXPECTED: The popup message is shown with the following elements:
        EXPECTED: - hardcoded 'Odds Boost Unavailable' title
        EXPECTED: - hardcoded 'Odds Boost is unavailable for SP selection' message text
        EXPECTED: - 'OK' button
        """
        self.odds_boost_header.boost_button.click()
        self.odds_boost_unavailable_dialog_verification()

    def test_007_tap_ok_buttonverify_that_odds_boost_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that Odds boost popup is closed
        EXPECTED: - The popup is closed
        EXPECTED: - Odds boost button is NOT selected to the boosted state
        EXPECTED: - 'i' icon is NOT shown for Section_1
        EXPECTED: - SP price is shown for Selection_1 and Selection_2
        EXPECTED: - Selection_3 is shown in an UNboosted state
        EXPECTED: - N/A is shown for returns
        """
        self.test_005_tap_ok_buttonverify_that_odds_boost_popup_is_closed()
