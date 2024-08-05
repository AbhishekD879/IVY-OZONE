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
class Test_C2610656_Verify_displaying_odds_boost_unavailable_popup_for_SP_in_Betslip_Single_Selection(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C2610656
    NAME: Verify displaying odds boost unavailable popup for SP in Betslip (Single Selection)
    DESCRIPTION: This test case verifies that odds boost button is not shown for SP in Betslip
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Load application and Login into the application
    PRECONDITIONS: Add selection with SP only available
    """
    keep_browser_open = True
    free_bet_value = 1.03
    expected_sp_odds = 'SP'

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

        event_params_1 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp_prices={0: '4/1'})
        self.__class__.selection_id = list(event_params_1.selection_ids.values())[0]
        self.__class__.eventID = event_params_1.event_id

        event_params_2 = self.ob_config.add_UK_racing_event(number_of_runners=1, lp=False, sp=True)
        self.__class__.selection_id_2 = list(event_params_2.selection_ids.values())[0]
        self.__class__.eventID_2 = event_params_2.event_id

        self.site.login(username)

    def test_001_navigate_to_betslip_and_add_a_stakeverify_that_the_odds_boost_section_is_not_shown_in_the_betslip(self):
        """
        DESCRIPTION: Navigate to Betslip and add a stake
        DESCRIPTION: Verify that the Odds Boost section is NOT shown in the Betslip
        EXPECTED: - 'BOOST' button is NOT shown
        EXPECTED: - SP odds is shown
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id_2)
        self.assertFalse(self.get_betslip_content().has_odds_boost_header,
                         msg='"Odds Boost section and its contents" is shown in the Betslip')
        singles_section = self.get_betslip_sections().Singles
        self.assertTrue(singles_section.items(), msg='No stakes found')
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = 0.5
        self.assertEqual(stake.odds, self.expected_sp_odds,
                         msg=f'Actual odds: "{stake.odds}" is not same as Expected odds: "{self.expected_sp_odds}"')

    def test_002_tap_place_bet_buttonverify_that_bet_receipt_is_shown(self):
        """
        DESCRIPTION: Tap 'Place Bet' button
        DESCRIPTION: Verify that Bet Receipt is shown
        EXPECTED: Bet Receipt is shown with SP odds
        """
        betnow_btn = self.get_betslip_content().bet_now_button
        betnow_btn.click()
        self.check_bet_receipt_is_displayed()
        receipt_sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(receipt_sections, msg='No receipt sections found in BetReceipt')
        receipt_bet_type_section = receipt_sections.get(vec.betslip.SINGLE)
        section_items = receipt_bet_type_section.items_as_ordered_dict
        self.assertTrue(section_items, msg='No bets found in BetReceipt')
        bet_info = list(section_items.values())[0]
        self.assertEqual(bet_info.odds, self.expected_sp_odds,
                         msg=f'Actual odds: "{bet_info.odds}" is not same as Expected odds: "{self.expected_sp_odds}"')
        self.site.bet_receipt.close_button.click()

    def test_003_add_selection_with_lp_and_sp_available_lp_is_selectednavigate_to_betslip_and_add_a_stake_to_the_selectionverify_that_the_odds_boost_section_is_shown_in_the_betslip(self):
        """
        DESCRIPTION: Add selection with LP and SP available (LP is selected)
        DESCRIPTION: Navigate to Betslip and add a Stake to the selection
        DESCRIPTION: Verify that the Odds Boost section is shown in the Betslip
        EXPECTED: Odds Boost section is shown on the top of Betslip with the following elements:
        EXPECTED: - 'BOOST' button
        EXPECTED: - 'Tap to boost your betslip' text
        EXPECTED: - 'i' icon
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_id)
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

    def test_004_tap_a_boost_button(self):
        """
        DESCRIPTION: Tap a 'BOOST' button
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed in dropdown
        EXPECTED: - Updated (to reflect the boosted odds) potential returns are shown
        """
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        stake.amount_form.input.value = 1
        original_est_returns = stake.est_returns
        self.odds_boost_header.boost_button.click()

        result = wait_for_result(
            lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
            name='"BOOST" button to become "BOOSTED" button with animation',
            timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        self.assertTrue(stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.assertTrue(stake.is_original_odds_crossed_for_lp_sp_dropdown, msg='Original odds are not crossed out')
        boosted_est_returns = stake.est_returns
        self.assertNotEqual(original_est_returns, boosted_est_returns,
                            msg=f'Boosted estimated returns "{boosted_est_returns}" are the same as '
                                f'original estimated returns "{original_est_returns}"')

    def test_005_change_lp_to_spverify_that_odds_boost_popup_is_shown(self):
        """
        DESCRIPTION: Change LP to SP
        DESCRIPTION: Verify that Odds Boost popup is shown
        EXPECTED: The popup message is shown with the following elements:
        EXPECTED: - hardcoded 'Odds Boost Unavailable' title
        EXPECTED: - hardcoded 'Odds Boost is unavailable for SP selection' message text
        EXPECTED: - 'OK' button
        """
        self.select_sp_price()
        self.__class__.dialog = \
            self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
                                      timeout=20)
        self.assertTrue(self.dialog, msg="Odss boost unavailable dialog not appeared")
        message = self.dialog.description
        self.assertEqual(message, vec.odds_boost.BETSLIP_DIALOG.unavailable_message,
                         msg=f'Actual message:"{message}" is not same as'
                             f'Expected message: "{vec.odds_boost.BETSLIP_DIALOG.unavailable_message}".')
        self.assertTrue(self.dialog.has_ok_button(), msg='"Ok" button is not displayed.')

    def test_006_tap_ok_buttonverify_that_odds_boost_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that Odds boost popup is closed
        EXPECTED: - The popup is closed
        EXPECTED: - Odds boost button is de-selected ('BOOST' button is shown)
        EXPECTED: - SP price is shown
        EXPECTED: - N/A is shown Est. Returns
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

        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.values())[0]
        self.assertEqual(stake.odds, self.expected_sp_odds,
                         msg=f'Actual odds: "{stake.odds}" is not same as Expected odds: "{self.expected_sp_odds}"')

        est_returns = stake.est_returns
        self.assertEqual(est_returns, 'N/A',
                         msg=f'Actual returns: "{est_returns}" is not same as Expected returns: "{"N/A"}"')

    def test_007_tap_boost_button_one_more_timeverify_that_odds_boost_popup_is_shown(self):
        """
        DESCRIPTION: Tap 'BOOST' button one more time
        DESCRIPTION: Verify that Odds boost popup is shown
        EXPECTED: The popup message is shown with the following elements:
        EXPECTED: - hardcoded 'Odds Boost Unavailable' title
        EXPECTED: - hardcoded 'Odds Boost is unavailable for SP selection' message text
        EXPECTED: - 'OK' button
        """
        self.odds_boost_header.boost_button.click()
        self.__class__.dialog = self.site.wait_for_dialog(
            dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_UNAVAILABLE_ON_BETSLIP,
            timeout=20)
        self.assertTrue(self.dialog, msg="Odss boost unavailable dialog not appeared")
        message = self.dialog.description
        self.assertEqual(message, vec.odds_boost.BETSLIP_DIALOG.unavailable_message,
                         msg=f'Actual message:"{message}" is not same as'
                             f'Expected message: "{vec.odds_boost.BETSLIP_DIALOG.unavailable_message}".')
        self.assertTrue(self.dialog.has_ok_button(), msg='"Ok" button is not displayed.')

    def test_008_tap_ok_buttonverify_that_odds_boost_popup_is_closed(self):
        """
        DESCRIPTION: Tap 'OK' button
        DESCRIPTION: Verify that Odds boost popup is closed
        EXPECTED: - The popup is closed
        EXPECTED: - Odds boost button is NOT selected to the boosted state ('BOOST' button is shown)
        EXPECTED: - SP price is shown
        EXPECTED: - N/A is shown for Est. Returns
        """
        self.test_006_tap_ok_buttonverify_that_odds_boost_popup_is_closed()
