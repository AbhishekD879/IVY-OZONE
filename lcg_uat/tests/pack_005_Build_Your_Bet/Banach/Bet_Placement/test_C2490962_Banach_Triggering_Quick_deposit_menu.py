import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from time import sleep
from tests.pack_002_User_Account.BaseUserAccountTest import BaseUserAccountTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from tests.pack_005_Build_Your_Bet.BaseBuildYourBetTest import BaseBanachTest
from voltron.utils.exceptions.third_party_data_exception import ThirdPartyDataException


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.banach
@pytest.mark.build_your_bet
@pytest.mark.quick_deposit
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.login
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1532')
@vtest
class Test_C2490962_Banach_Triggering_Quick_deposit_menu(BaseBanachTest, BaseBetSlipTest, BaseUserAccountTest):
    """
    TR_ID: C2490962
    NAME: Banach. Triggering Quick deposit menu
    DESCRIPTION: Test case verifies triggering Quick deposit menu and entering CVV and Amount to continue Banach betting
    PRECONDITIONS: Build Your Bet CMS configuration:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/CMS+documentation+for+Build+Your+Bet
    PRECONDITIONS: **User has added Banach selections dashboard and tapped PLACE BET button**
    """
    keep_browser_open = True
    proxy = None
    quick_deposit_button = None
    blocked_hosts = ['*spark-br.*']

    def test_000_preconditions(self):
        """
        DESCRIPTION: Find active event with Banach markets
        DESCRIPTION: Login and navigate to EDP using derived event_id
        """
        if not tests.settings.quick_deposit_card:
            raise ThirdPartyDataException('There is no quick deposit payment card')

        self.__class__.eventID = self.get_ob_event_with_byb_market()
        self.site.login(username=tests.settings.quick_deposit_user)
        self.navigate_to_edp(event_id=self.eventID)
        byb_tab = self.site.sport_event_details.markets_tabs_list.open_tab(self.expected_market_tabs.build_your_bet)
        self.assertTrue(byb_tab, msg=f'{self.expected_market_tabs.build_your_bet} tab is not active')
        #  w/a for empty response from BYB
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        match_betting = self.get_market(market_name=self.expected_market_sections.match_betting)
        match_betting_selection_name = match_betting.set_market_selection(selection_index=1)[0]
        match_betting.set_market_selection(selection_index=1, time=True)
        self.assertTrue(match_betting_selection_name, msg='No selections added to Dashboard')
        self.assertTrue(match_betting_selection_name, msg='Match betting selection is not added to Dashboard')
        match_betting.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(
            self.initial_counter)
        self.__class__.initial_counter += 1

        both_teams_to_score_market = self.get_market(market_name=self.expected_market_sections.both_teams_to_score)
        both_teams_to_score_names = both_teams_to_score_market.set_market_selection(selection_index=1, time=True)
        self.assertTrue(both_teams_to_score_names, msg='No one selection added to Dashboard')
        both_teams_to_score_market.add_to_betslip_button.click()
        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.wait_for_counter_change(self.initial_counter)
        self.__class__.initial_counter += 1

    def test_001_enter_a_stake_higher_then_current_user_balance_in_a_stake(self):
        """
        DESCRIPTION: Enter a stake higher then current user balance in a stake
        EXPECTED: - Stake and Est.Returned are populated with the values
        EXPECTED: Total Stake - amount entered by user
        EXPECTED: Est.Returns - calculated based on Odds value: (odds + 1)*stake
        EXPECTED: - User message above Betslip:
        EXPECTED: **Funds needed for bet: %**
        EXPECTED: where % is a difference between entered amount and current balance
        EXPECTED: - Buttons **Back** and **Make a quick deposit** are present below Betslip
        """
        user_balance = self.site.header.user_balance
        stake = user_balance + 5
        if self.site.sport_event_details.tab_content.dashboard_panel.has_price_not_available_message():
            self.assertFalse(
                self.site.sport_event_details.tab_content.dashboard_panel.price_not_available_message.is_displayed(
                    expected_result=False),
                msg=f'Message: "{vec.yourcall.PRICE_NOT_AVAILABLE}" displayed')
        odds = self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.value_text
        calculated_est_returns = self.calculate_estimated_returns(bet_amount=stake, odds=[odds])

        self.site.sport_event_details.tab_content.dashboard_panel.byb_summary.place_bet.click()
        self.assertTrue(self.site.wait_for_byb_betslip_panel(), msg='BYB Betslip has not appeared')
        self.site.byb_betslip_panel.selection.content.amount_form.enter_amount(stake)

        total_stake = float(self.site.byb_betslip_panel.selection.bet_summary.total_stake)
        self.assertAlmostEqual(total_stake, stake, delta=0.01,
                               msg=f'Total Stake amount value "{total_stake}" is not the same as expected "{stake}"'
                                   f'with delta 0.01')

        total_estimate_returns = float(self.site.byb_betslip_panel.selection.bet_summary.total_estimate_returns)
        self.assertAlmostEqual(total_estimate_returns, calculated_est_returns, delta=0.03,
                               msg=f'Est Returns amount value "{total_estimate_returns}" is not the same '
                               f'as expected "{calculated_est_returns}"')
        if self.brand == 'ladbrokes':
            result = self.site.byb_betslip_panel.selection.wait_for_deposit_info_message()
            self.assertTrue(result, msg=f'"Min Deposit" message is not shown')
            message = self.site.byb_betslip_panel.selection.deposit_info_message.text
        else:
            result = self.site.byb_betslip_panel.wait_for_quick_bet_info_panel()
            self.assertTrue(result, msg=f'"Min Deposit" message is not shown')

            message = self.site.byb_betslip_panel.info_panels.text
        expected_message = vec.quickbet.QUICKBET_DEPOSIT_NOTIFICATION.format(stake - user_balance)
        self.assertEqual(message, expected_message,
                         msg=f'Actual message "{message}" is not the same as expected "{expected_message}"')

        back_button = self.site.byb_betslip_panel.back_button
        self.assertTrue(back_button.is_displayed(), msg='"BACK" button is not displayed below BetSlip')

        self.__class__.quick_deposit_button = self.site.byb_betslip_panel.make_quick_deposit_button
        self.assertTrue(self.quick_deposit_button.is_displayed(),
                        msg='"MAKE A QUICK DEPOSIT" button is not displayed below BetSlip')

    def test_002_tap_on_make_a_quick_deposit_button(self):
        """
        DESCRIPTION: Tap on MAKE A QUICK DEPOSIT button
        EXPECTED: - Quick deposit menu is opened
        EXPECTED: - DEPOSIT AND PLACE BET button is disabled
        """
        self.quick_deposit_button.click()
        self.assertTrue(self.site.byb_betslip_panel.wait_for_quick_deposit_panel(),
                        msg='Quick deposit menu is not opened')
        self.__class__.quick_deposit = self.site.byb_betslip_panel.quick_deposit_panel.stick_to_iframe()
        self.assertFalse(self.quick_deposit.deposit_and_place_bet_button.is_enabled(expected_result=False),
                         msg='"DEPOSIT & PLACE BET" button is not disabled')

    def test_003_enter_cvv_and_amount(self):
        """
        DESCRIPTION: Enter CVV and Amount
        EXPECTED: DEPOSIT AND PLACE BET button is enabled
        """
        if self.device_type == 'mobile':
            self.quick_deposit.cvv_2.click()
            keyboard = self.quick_deposit.keyboard
            self.assertTrue(keyboard.is_displayed(name='Numeric keyboard shown', timeout=3),
                            msg='Numeric keyboard is not shown')
            keyboard.enter_amount_using_keyboard(value=tests.settings.quick_deposit_card_cvv)
            keyboard.enter_amount_using_keyboard(value='enter')
        else:
            self.quick_deposit.cvv_2.input.value = tests.settings.quick_deposit_card_cvv
        sleep(3)
        self.assertTrue(self.quick_deposit.deposit_and_place_bet_button.is_enabled(),
                        msg='"DEPOSIT & PLACE BET" button is not enabled')
