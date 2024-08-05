import pytest
import tests
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - can't grant odds boost tokens on prod
# @pytest.mark.hl - can't grant odds boost tokens on hl
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.odds_boost
@pytest.mark.bet_placement
@pytest.mark.login
@pytest.mark.soc
@vtest
class Test_C12834352_Odds_Boost_functionality_in_Betslip(BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C12834352
    NAME: Odds Boost functionality in Betslip
    DESCRIPTION: This test case verifies Odds Boost functionality in Bet Slip
    DESCRIPTION: this test is only suitable for TST2/STG2 endpoints
    """
    keep_browser_open = True
    bet_amount = 0.5

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 'Odds Boost' Feature Toggle is enabled in CMS
        PRECONDITIONS: Generate for user Odds boost token with Any token value in http://backoffice-tst2.coral.co.uk/office
        PRECONDITIONS: How to add OB token https://confluence.egalacoral.com/display/SPI/How+to+add+Odds+boost+token
        PRECONDITIONS: Note: Selection appropriate for odds boost should have 'Enhance Odds available' checked on all hierarchy level
        PRECONDITIONS: Load application and do NOT log in
        PRECONDITIONS: Fractional odds format selected for User1
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
        offer_id = self.ob_config.backend.ob.odds_boost_offer_non_adhoc.general_offer.offer_id
        self.__class__.username = tests.settings.odds_boost_user
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', id=self.selection_id,
                                              offer_id=offer_id)
        self.site.wait_content_state('Homepage')

    def test_001_add_a_single_selection_with_added_stake_to_the_betslipverify_that_odds_boost_button_is_not_shown_in_betslip(self):
        """
        DESCRIPTION: Add a single selection with added Stake to the Betslip
        DESCRIPTION: Verify that 'Odds boost' button is NOT shown in Betslip
        EXPECTED: 'BOOST' button is NOT shown in Betslip
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.assertFalse(self.get_betslip_content().has_odds_boost_header, msg='Odds Boost header is displayed on betslip')
        singles_section = self.get_betslip_sections().Singles
        stake = list(singles_section.items())[0]
        self.enter_stake_amount(stake=stake)

        self.site.close_betslip()

    def test_002_login_into_application_by_user_with_any_type_odds_boost_token_available(self):
        """
        DESCRIPTION: Login into Application by user with Any type Odds Boost token available
        EXPECTED: User is logged in successfully
        EXPECTED: The "Odds Boost" token notification is displayed
        """
        self.site.login(username=self.username, async_close_dialogs=False,
                        ignored_dialogs=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, close_free_bets_notification=False)
        dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_ODDS_BOOST, verify_name=False, timeout=10)
        self.assertTrue(dialog, msg='Odds Boost dialog is not displayed.')
        dialog.thanks_link.click()
        dialog_closed = dialog.wait_dialog_closed(timeout=5)
        self.assertTrue(dialog_closed, msg='Odds Boost dialog was not closed')
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')

    def test_003_navigate_to_the_betslip_verify_that_odds_boost_button_is_shown_in_betslip(self):
        """
        DESCRIPTION: Navigate to the Betslip
        DESCRIPTION: Verify that Odds Boost button is shown in Betslip
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOST' button is available
        EXPECTED: - 'Tap to boost your betslip' text
        EXPECTED: - 'i' icon (with popup 'Hint Boost to increase the odds of the bets in your betslip! You can boost up to 50.00 total stake')
        EXPECTED: Est.returns/ Estimated returns(Coral), Pot. Returns / Potential returns(Ladbrokes)
        """
        self.site.open_betslip()
        self.assertTrue(self.site.has_betslip_opened(), msg='Failed to open betslip')
        self.assertTrue(self.get_betslip_content().has_odds_boost_header, msg='Odds Boost header is not displayed on betslip')

        self.__class__.odds_boost_header = self.get_betslip_content().odds_boost_header

        self.assertTrue(self.odds_boost_header.tap_to_boost_your_betslip_label.is_displayed(),
                        msg=f'"{vec.odds_boost.BETSLIP_HEADER.subtitle}" text is not displayed')
        self.assertEqual(self.odds_boost_header.tap_to_boost_your_betslip_label.name, vec.odds_boost.BETSLIP_HEADER.subtitle,
                         msg=f'"{vec.odds_boost.BETSLIP_HEADER.subtitle}" text is not displayed and '
                             f'"{self.odds_boost_header.tap_to_boost_your_betslip_label.name}" is displayed instead')
        self.assertTrue(self.odds_boost_header.info_button.is_displayed(),
                        msg='Info button is not displayed')
        self.odds_boost_header.info_button.click()
        info_popup = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_INFORMATION, timeout=5, verify_name=False)
        self.assertTrue(info_popup, msg='Information pop-up is not shown')
        info_popup_name = vec.dialogs.DIALOG_MANAGER_ODDS_BOOST_ON_BETSLIP.replace("lad", "")
        self.assertEqual(info_popup.name, info_popup_name,
                         msg=f'"{info_popup.name}" is not the same as expected "{info_popup_name}"')
        info_popup_description = info_popup.description
        self.assertEqual(info_popup_description, vec.odds_boost.INFO_DIALOG.text,
                         msg=f'Hint text "{info_popup_description}" is not the same as expected "{vec.odds_boost.INFO_DIALOG.text}"')
        info_popup.click_ok()
        self.assertTrue(info_popup.wait_dialog_closed(timeout=1), msg='Information pop-up is not closed')

        singles_section = self.get_betslip_sections().Singles
        self.__class__.stake_name, self.__class__.stake = list(singles_section.items())[0]
        self.__class__.original_est_returns = self.stake.est_returns
        self.assertTrue(self.original_est_returns, msg='Estimated returns are not displayed on betslip')

    def test_004_tap_boost_buttonverify_that_odds_are_boosted_and_odds_boost_button_is_displaying(self):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds are boosted and odds boost button is displaying
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button
        EXPECTED: - Boosted odds is shown
        EXPECTED: - Original odds is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) returns are shown
        """
        self.odds_boost_header.boost_button.click()

        result = wait_for_result(lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        self.assertTrue(self.stake.boosted_odds_container.is_displayed(), msg='Boosted odds are not shown')
        self.assertTrue(self.stake.is_original_odds_crossed, msg='Original odds are not crossed out')
        self.__class__.selection_name = self.stake_name
        self.__class__.boosted_odds = self.stake.boosted_odds_container.price_value
        self.__class__.boosted_est_returns = self.stake.est_returns

        self.assertNotEqual(self.original_est_returns, self.boosted_est_returns,
                            msg=f'Boosted estimated returns "{self.boosted_est_returns}" are the same as '
                                f'original estimated returns "{self.original_est_returns}"')

    def test_005_tap_boosted_buttonverify_that_odds_boost_button_is_shown_and_the_odds_boost_is_removed(self):
        """
        DESCRIPTION: Tap 'BOOSTED' button
        DESCRIPTION: Verify that odds boost button is shown and the odds boost is removed
        EXPECTED: - 'BOOSTED' button is changed back to 'BOOST' button
        EXPECTED: - Boosted odds are removed
        EXPECTED: - Est. returns/ Estimated returns(Coral), Pot. Returns / Potential returns(Ladbrokes) are updated back
        """
        self.odds_boost_header.boost_button.click()
        result = wait_for_result(
            lambda: self.odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
            name='"BOOSTED" button to become "BOOST" button with animation',
            timeout=2)
        self.assertTrue(result, msg='"BOOSTED" button did not change to "BOOST" button')

        singles_section = self.get_betslip_sections().Singles
        self.assertIsNotNone(singles_section, msg='Singles section not found')
        stake_name, stake = list(singles_section.items())[0]

        self.assertFalse(stake.has_boosted_odds, msg=f'"{stake_name}" should not have boosted odds')

    def test_006_tap_boost_button_one_more_time_and_then_tap_place_bet_buttonverify_that_bet_receipt_is_shown(self):
        """
        DESCRIPTION: Tap 'BOOST' button one more time and then tap 'Place Bet' button.
        DESCRIPTION: Verify that bet receipt is shown
        EXPECTED: Bet receipt is shown with the following elements:
        EXPECTED: - boost icon
        EXPECTED: - hardcoded text: "This bet has been boosted!"
        EXPECTED: - boost odds was taken by the user
        EXPECTED: - Est. returns/ Estimated returns(Coral), Pot. Returns / Potential returns(Ladbrokes appropriate to boosted odds
        """
        self.odds_boost_header.boost_button.click()
        self.assertTrue(self.get_betslip_content().has_bet_now_button(), msg='Place Bet button is not present.')
        place_bet_button = self.get_betslip_content().bet_now_button
        self.assertTrue(place_bet_button.is_displayed(), msg='Place Bet button is not displayed.')
        self.assertTrue(place_bet_button.is_enabled(), msg='Place Bet button is not enabled.')
        place_bet_button.click()
        self.check_bet_receipt_is_displayed()

        sections = self.site.bet_receipt.bet_receipt_sections_list.items_as_ordered_dict
        self.assertTrue(sections, msg='Bet receipt sections not found')
        single_sections = sections.get(vec.betslip.SINGLE)
        self.assertIsNotNone(single_sections, msg='Single sections not found')
        single_section = single_sections.items_as_ordered_dict
        bet = single_section.get(self.selection_name)
        self.assertIsNotNone(bet, msg=f'Bet "{bet.name}" not found in single section')

        self.assertTrue(bet.boosted_section.icon.is_displayed(),
                        msg='Boost icon is not displayed')
        self.assertEqual(bet.boosted_section.text, vec.betslip.BOOSTED_MSG,
                         msg=f'Boosted bet text "{bet.boosted_section.text}" '
                             f'is not the same as expected "{vec.betslip.BOOSTED_MSG}"')
        self.assertEqual(bet.odds, self.boosted_odds,
                         msg=f'Boosted odds "{bet.odds}" '
                             f'are not the same as expected "{self.boosted_odds}"')
        self.verify_estimated_returns(est_returns=float(self.boosted_est_returns), odds=self.boosted_odds,
                                      bet_amount=self.bet_amount)
        self.site.bet_receipt.close_button.click()

    def test_007_provide_same_verifications_with_decimal_odds_format(self):
        """
        DESCRIPTION: Provide same verifications with decimal odds format
        """
        is_format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(is_format_changed, msg='Odds format is not changed to Decimal')
        if self.device_type != 'desktop':
            if self.site.cookie_banner:
                self.site.cookie_banner.ok_button.click()
            self.site.go_to_home_page()
        self.site.logout()
        self.assertTrue(self.site.wait_logged_out(), msg='User is not logged out')
        self.ob_config.grant_odds_boost_token(username=self.username)
        self.__class__.expected_betslip_counter_value = 0
        self.test_001_add_a_single_selection_with_added_stake_to_the_betslipverify_that_odds_boost_button_is_not_shown_in_betslip()
        self.test_002_login_into_application_by_user_with_any_type_odds_boost_token_available()
        self.test_003_navigate_to_the_betslip_verify_that_odds_boost_button_is_shown_in_betslip()
        self.test_004_tap_boost_buttonverify_that_odds_are_boosted_and_odds_boost_button_is_displaying()
        self.test_005_tap_boosted_buttonverify_that_odds_boost_button_is_shown_and_the_odds_boost_is_removed()
        self.test_006_tap_boost_button_one_more_time_and_then_tap_place_bet_buttonverify_that_bet_receipt_is_shown()
