import pytest

import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod - Can't grant odds boost tokens on prod
# @pytest.mark.hl - Can't grant odds boost tokens on prod
@pytest.mark.high
@pytest.mark.betslip
@pytest.mark.odds_boost
@pytest.mark.quick_bet
@pytest.mark.mobile_only  # available for tablet as well
@pytest.mark.slow
@pytest.mark.login
@vtest
class Test_C2605931_Verify_displaying_odds_boost_button_in_Quick_Bet_for_logged_in_user(BaseSportTest, BaseBetSlipTest,
                                                                                        BaseUserAccountTest):
    """
    TR_ID: C2605931
    VOL_ID: C14468550
    NAME: Verify displaying odds boost button in Quick Bet for logged in user
    DESCRIPTION: This test case verifies that odds boost button displaying in Quickbet for logged in user
    PRECONDITIONS: "Odds Boost" Feature Toggle is enabled in CMS
    PRECONDITIONS: Quickbet is enabled
    PRECONDITIONS: Generate for user Odds boost token in http://backoffice-tst2.coral.co.uk/office for User1
    PRECONDITIONS: Fractional odds selected for User1
    PRECONDITIONS: Load application and do NOT login
    """
    keep_browser_open = True
    bet_amount = 0.11

    def test_000_preconditions(self):
        """
        DESCRIPTION: "Odds Boost" Feature Toggle is enabled in CMS. Football event is created
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost')
        if odds_boost is None:
            raise CmsClientException('Odds Boost config is disabled in CMS')
        if not odds_boost['enabled']:
            raise CmsClientException('Odds Boost is disabled in CMS')

        self.__class__.username = tests.settings.odds_boost_user

        self.__class__.eventID = self.ob_config.add_football_event_to_spanish_la_liga().event_id
        market_name = self.ob_config.football_config.spain.spanish_la_liga.market_name.replace('|', '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_add_selection_with_odds_boost_available_verify_that_quick_bet_popup_is_shown_without_boost_button(self):
        """
        DESCRIPTION: Add selection with odds boost available
        DESCRIPTION: Verify that Quick Bet popup is shown WITHOUT 'BOOST' button
        EXPECTED: 'BOOST' button is not shown
        """
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
        quick_bet = self.site.quick_bet_panel
        self.assertFalse(quick_bet.has_odds_boost_button(expected_result=False),
                         msg='Odds boost button is present on Quickbet panel')
        quick_bet.header.close_button.click()
        self.site.wait_quick_bet_overlay_to_hide()

        outcome = self.get_selection_bet_button(market_name=self.expected_market_name)
        outcome.click()
        self.site.wait_content_state(state_name='EventDetails')
        self.site.go_to_home_page()

    def test_002_login_with_user1_add_selection_with_odds_boost_available(self):
        """
        DESCRIPTION: Login with User1
        DESCRIPTION: Add selection with odds boost available
        DESCRIPTION: Verify that Quick Bet popup is shown WITH 'BOOST' button
        EXPECTED: Quick Bet is shown
        EXPECTED: 'BOOST' button is shown in Quick Bet
        """
        self.site.login(username=self.username, async_close_dialogs=False, timeout=20)
        offer_id = self.ob_config.backend.ob.odds_boost_offer_non_adhoc.general_offer.offer_id
        self.ob_config.grant_odds_boost_token(username=self.username, level='selection', offer_id=offer_id)
        self.navigate_to_edp(event_id=self.eventID)
        self.site.wait_content_state(state_name='EventDetails')
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
        self.site.wait_content_state(state_name='EventDetails')
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.assertTrue(self.quick_bet.has_odds_boost_button(), msg='Odds boost button is not present on Quickbet panel')

    def test_003_add_stake_to_selection(self):
        """
        DESCRIPTION: Add Stake to selection
        EXPECTED: Potential returns/total potential returns are shown according to added stake
        """
        quick_bet = self.quick_bet.selection
        amount = quick_bet.content.amount_form.input
        self.assertTrue(amount.is_displayed(timeout=3),
                        msg='Amount field is not displayed')
        amount.click()
        self.assertTrue(amount.is_enabled(timeout=1),
                        msg='Amount field is not enabled.')
        amount.value = self.bet_amount
        amount = float(quick_bet.content.amount_form.input.value)
        self.assertEqual(amount, self.bet_amount,
                         msg=f'Entered amount "{amount}" is not equal to expected "{self.bet_amount}"')
        self.__class__.initial_total_est_returns = self.quick_bet.selection.bet_summary.total_estimate_returns

    def test_004_tap_boost_button_verify_that_odds_boost_button_is_shown(self, expected_odds_format='fraction'):
        """
        DESCRIPTION: Tap 'BOOST' button
        DESCRIPTION: Verify that odds boost button is shown with animation and the odds are boosted
        EXPECTED: Quick Bet is displayed with the following elements:
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/total potential returns are shown
        """
        self.__class__.start_price = self.quick_bet.selection.content.odds_value
        self.quick_bet.odds_boost_button.click()
        result = wait_for_result(lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')
        self.assertTrue(self.quick_bet.selection.content.boosted_odds_container.is_displayed(timeout=3),
                        msg='Boosted odds are not shown')
        self.check_odds_format(odds=self.quick_bet.selection.content.boosted_odds_container.price_value,
                               expected_odds_format=expected_odds_format)

        self.assertTrue(self.quick_bet.selection.content.is_original_odds_crossed,
                        msg='Original odds are not crossed out')

        boosted_total_est_returns = self.quick_bet.selection.bet_summary.total_estimate_returns
        self.assertNotEqual(boosted_total_est_returns, self.initial_total_est_returns,
                            msg=f'Boosted Total Est. Returns value "{boosted_total_est_returns}" '
                                f'is the same as initial value "{self.initial_total_est_returns}"')

    def test_005_tap_boosted_button_verify_that_odds_boost_button_is_shown(self):
        """
        DESCRIPTION: Tap 'BOOSTED' button
        DESCRIPTION: Verify that odds boost button is shown with animation and the odds boost is removed
        EXPECTED: - 'BOOSTED' button is changed to 'BOOST' button with animation
        EXPECTED: - Original odds (fractional) is shown
        EXPECTED: - Boosted odds is removed
        EXPECTED: - Potential returns/ total potential returns is rolled back
        """

        self.quick_bet.odds_boost_button.click()
        result = wait_for_result(
            lambda: self.quick_bet.odds_boost_button.name == vec.odds_boost.BOOST_BUTTON.disabled,
            name='"BOOSTED" button to become "BOOST" button with animation',
            timeout=2)
        self.assertTrue(result, msg='"BOOSTED" button did not change to "BOOST" button')
        self.assertEquals(self.quick_bet.selection.content.odds_value, self.start_price,
                          msg=f'{self.quick_bet.selection.content.odds_value} is not equal to {self.start_price}')
        self.assertFalse(self.quick_bet.selection.content.has_boosted_odds, msg=f'Boosted odds is showing up')
        boosted_total_est_returns = self.quick_bet.selection.bet_summary.total_estimate_returns
        self.assertEqual(boosted_total_est_returns, self.initial_total_est_returns,
                         msg=f'Boosted Total Est. Returns value "{boosted_total_est_returns}" is the '
                             f'not same as initial value "{self.initial_total_est_returns}"')

    def test_006_tap_boost_button_one_more_time(self, expected_odds_format='fraction'):
        """
        DESCRIPTION: Tap 'BOOST' button one more time
        DESCRIPTION: Verify that odds boost button is shown with animation and the odds are boosted
        EXPECTED: - 'BOOST' button is changed to 'BOOSTED' button with animation
        EXPECTED: - Boosted odds (fractional) is shown
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/total potential returns are shown
        """
        self.test_004_tap_boost_button_verify_that_odds_boost_button_is_shown(expected_odds_format=expected_odds_format)

    def test_007_tap_add_to_betslip_button_and_navigate_to_betslip(self, expected_odds_format='fraction'):
        """
        DESCRIPTION: Tap 'Add to Betslip' button and navigate to Betslip
        DESCRIPTION: Verify that BOOSTED odds is shown in Betslip
        EXPECTED: Betslip is displayed with the following elements:
        EXPECTED: - 'BOOSTED' button with animation
        EXPECTED: - Boosted odds (fractional)
        EXPECTED: - Original odds (fractional) is displayed as crossed out
        EXPECTED: - Updated (to reflect the boosted odds) potential returns/total potential returns
        """
        self.quick_bet.add_to_betslip_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.site.open_betslip()

        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        if self.brand == 'bma':
            self.assertTrue(odds_boost_header.boost_button.has_boost_indicator,
                            msg='Boost button does not have boost indicator')
        elif self.brand == 'ladbrokes':
            self.assertIn('enabled', odds_boost_header.boost_button.boost_indicator,
                          msg='Boost-meter did not animate during odds boosting')

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.boosted_odds_container.is_displayed(timeout=3), msg='Boosted odds are not shown')

        self.check_odds_format(odds=stake.boosted_odds_container.price_value, expected_odds_format=expected_odds_format)
        self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')

        boosted_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(boosted_total_est_returns, self.initial_total_est_returns,
                            msg=f'Boosted Total Est. Returns value "{boosted_total_est_returns}" '
                                f'is the same as initial value "{self.initial_total_est_returns}"')
        self.clear_betslip()
        self.__class__.expected_betslip_counter_value = 0
        format_changed = self.site.change_odds_format(odds_format=vec.bma.USER_SETTINGS_ODDS_FORMAT_DEC)
        self.assertTrue(format_changed, msg='Odds format is not changed to Decimal')
        self.verify_selected_option_on_preferences_page(expected_selected_option='decimal')
        self.site.logout()

    def test_008_change_odds_format_to_decimal_verify_that_this_functionality_works_the_same_with_decimal_odds(self):
        """
        DESCRIPTION: Change odds format to Decimal
        DESCRIPTION: Verify that this functionality works the same with decimal odds
        EXPECTED: - Boosted odds is shown in decimal
        EXPECTED: - Original odds is displayed as crossed out in decimal
        """
        self.test_001_add_selection_with_odds_boost_available_verify_that_quick_bet_popup_is_shown_without_boost_button()

        self.site.login(username=self.username)
        self.navigate_to_edp(event_id=self.eventID)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
        self.site.wait_content_state(state_name='EventDetails')
        self.__class__.quick_bet = self.site.quick_bet_panel
        self.assertTrue(self.quick_bet.has_odds_boost_button(), msg='Odds boost button is present on Quickbet panel')

        self.test_003_add_stake_to_selection()
        self.test_004_tap_boost_button_verify_that_odds_boost_button_is_shown(expected_odds_format='decimal')
        self.test_005_tap_boosted_button_verify_that_odds_boost_button_is_shown()
        self.test_006_tap_boost_button_one_more_time(expected_odds_format='decimal')

        self.quick_bet.add_to_betslip_button.click()
        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is not closed')
        self.site.open_betslip()

        odds_boost_header = self.get_betslip_content().odds_boost_header
        result = wait_for_result(lambda: odds_boost_header.boost_button.name == vec.odds_boost.BOOST_BUTTON.enabled,
                                 name='"BOOST" button to become "BOOSTED" button with animation',
                                 timeout=2)
        self.assertTrue(result, msg='"BOOST" button did not change to "BOOSTED" button')

        if self.brand == 'bma':
            self.assertTrue(odds_boost_header.boost_button.has_boost_indicator,
                            msg='Boost button does not have boost indicator')
        elif self.brand == 'ladbrokes':
            self.assertIn('enabled', odds_boost_header.boost_button.boost_indicator,
                          msg='Boost-meter did not animate during odds boosting')

        singles_section = self.get_betslip_sections().Singles
        stake_name, stake = list(singles_section.items())[0]
        self.assertTrue(stake.boosted_odds_container.is_displayed(timeout=3), msg='Boosted odds are not shown')
        self.check_odds_format(odds=stake.boosted_odds_container.price_value, expected_odds_format='decimal')
        self.assertTrue(stake.is_original_odds_crossed, msg='Original odds are not crossed out')

        boosted_total_est_returns = self.get_betslip_content().total_estimate_returns
        self.assertNotEqual(boosted_total_est_returns, self.initial_total_est_returns,
                            msg=f'Boosted Total Est. Returns value "{boosted_total_est_returns}" '
                                f'is the same as initial value "{self.initial_total_est_returns}"')
