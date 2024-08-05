import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.betslip
@pytest.mark.bet_placement
@pytest.mark.overask
@pytest.mark.quick_bet
@pytest.mark.event_details
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.login
@vtest
class Test_C884502_Verify_Overask_redirection_to_Main_Betslip(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C884502
    VOL_ID: C9698361
    NAME: Verify Overask redirection to Main Betslip
    DESCRIPTION: This test case verifies Overask handling within Quick Bet
    PRECONDITIONS: Oxygen application is loaded
    """
    keep_browser_open = True
    max_bet = 5
    stake_delta = 2.43

    def test_000_preconditions(self):
        """
        DESCRIPTION: Log in and create event
        """
        self.__class__.username = tests.settings.overask_enabled_user
        self.site.login(username=self.username)
        self.__class__.event_params = self.ob_config.add_autotest_premier_league_football_event(max_bet=self.max_bet)
        market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|',
                                                                                                                '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_select_sport_race_selection(self):
        """
        DESCRIPTION: Select <Sport>/<Race> selection
        """
        self.navigate_to_edp(event_id=self.event_params.event_id)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name,
                                                           selection_name=self.event_params.team1)

    def test_002_enter_higher_than_max_allowed_stake_value_and_tap_on_place_bet(self):
        """
        DESCRIPTION: Enter higher than max allowed stake value and tap on 'PLACE BET'
        EXPECTED: Quick Bet is closed
        EXPECTED: Betslip is opened with selection added
        EXPECTED: Overask overlay appears
        """
        self.assertTrue(self.site.quick_bet_panel.selection.content.amount_form.input.is_displayed(timeout=2),
                        msg='Amount input field is not displayed')

        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.max_bet + self.stake_delta

        self.site.quick_bet_panel.place_bet.click()

        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is shown')
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip not opened')
        overask_spinner = self.get_betslip_content().overask.overask_spinner.is_displayed(timeout=10)
        self.assertTrue(overask_spinner, msg='Overask spinner is not shown')

    def test_003_verify_that_overask_is_triggered_by_default(self):
        """
        DESCRIPTION: Verify that Overask is triggered by default
        EXPECTED: Stake field and 'Delete' button are disabled
        EXPECTED: Spinning icon is displayed instead of 'Bet Now' on green button
        EXPECTED: Warning message is shown to user on yellow background
        """
        overask_exceeds_message = self.get_betslip_content().overask.overask_exceeds.is_displayed()
        self.assertTrue(overask_exceeds_message, msg='Overask exceeds message is not shown')

        overask_spinner = self.get_betslip_content().overask.overask_spinner.is_displayed()
        self.assertTrue(overask_spinner, msg='Overask spinner is not shown')

    def test_004_reload_the_page_and_try_to_add_one_more_selection(self):
        """
        DESCRIPTION: Reload the page or app and try to add one more selection
        EXPECTED: Selection can not be added during Overask process
        EXPECTED: After trying to add selection user is navigated to Betslip with bet in review automatically
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()

        markets = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(markets, msg='No items found on market selection list')
        self.assertIn(self.expected_market_sections.match_result, markets,
                      msg=f'Match Result market is not in markets {markets.keys()}')
        market = markets.get(self.expected_market_sections.match_result)

        market.expand()

        outcomes = market.outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg=f'No items found on {self.expected_market_sections.match_result} market outcomes')

        button_name = 'DRAW' if self.brand == 'ladbrokes' else 'Draw'
        outcomes[button_name].click()

        self.assertFalse(self.site.wait_for_quick_bet_panel(expected_result=False), msg='Quick Bet is shown')
        self.assertTrue(self.site.has_betslip_opened(), msg='Betslip not opened')
        overask_spinner = self.get_betslip_content().overask.overask_spinner.is_displayed(timeout=10)
        self.assertTrue(overask_spinner, msg='Overask spinner is not shown')

    def test_005_open_betslip_and_proceed_with_overask_in_backoffice(self):
        """
        DESCRIPTION: Open Betslip and proceed with Overask in Backoffice: * accept/decline/make an offer/split offer
        EXPECTED: Main Betslip reflects to Trader action in Backoffice
        """
        account_id, bet_id, betslip_id = self.bet_intercept.find_bet_for_review(username=self.username,
                                                                                event_id=self.event_params.event_id)
        self._logger.debug(f'*** Bet id "{bet_id}", betslip id "{bet_id}"')
        suggested_max_bet = 3.5
        self.bet_intercept.offer_stake(
            account_id=account_id, bet_id=bet_id, betslip_id=betslip_id, max_bet=suggested_max_bet, price_type='S')
        overask_trader_message = self.get_betslip_content().overask_trader_section.trader_message
        self.assertTrue(overask_trader_message, msg='Trader message is not shown')

    def test_006_in_the_betslip_choose_cancel_button(self):
        """
        DESCRIPTION: In the betslip choose "Cancel" button
        EXPECTED: Selection with the offer was removed
        """
        self.get_betslip_content().cancel_button.click()
        dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_CANCEL_OFFER, timeout=5)
        dialog.cancel_offer_button.click()
        dialog.wait_dialog_closed()
        self.assertFalse(self.site.has_betslip_opened(expected_result=False, timeout=5),
                         msg='Betslip widget was not closed')

    def test_007_log_out_and_log_in_under_user_positive_balance_and_disabled_overask(self):
        """
        DESCRIPTION: Log out and log in under user with positive balance and disabled Overask
        """
        self.site.logout()
        self.site.login(username=tests.settings.disabled_overask_user)

    def test_008_repeat_step_1_2(self):
        """
        DESCRIPTION: Repeat step # 1-2
        EXPECTED: Bet is not places and Overask is not triggered
        EXPECTED: 'The stake specified in the bet is too high.' error message is shown
        EXPECTED: Bet remains in Quick Bet
        """
        self.navigate_to_edp(event_id=self.event_params.event_id)
        self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name,
                                                           selection_name=self.event_params.team1)
        self.assertTrue(self.site.quick_bet_panel.selection.content.amount_form.input.is_displayed(timeout=2),
                        msg='Amount input field is not displayed')

        self.site.quick_bet_panel.selection.content.amount_form.input.value = self.max_bet + self.stake_delta

        self.site.quick_bet_panel.place_bet.click()

        message = self.site.quick_bet_panel.info_panels.text
        expected_big_stake_message = vec.quickbet.BET_PLACEMENT_ERRORS.stake_high.format(self.max_bet)
        self.assertEqual(message, expected_big_stake_message,
                         msg=f'Actual message "{message}" does not match expected "{expected_big_stake_message}"')
