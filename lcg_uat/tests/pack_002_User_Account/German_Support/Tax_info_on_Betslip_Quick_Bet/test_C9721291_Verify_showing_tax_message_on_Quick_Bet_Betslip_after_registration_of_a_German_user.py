import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


# @pytest.mark.lad_tst2 # VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.betslip
@pytest.mark.desktop
@pytest.mark.quick_bet
@pytest.mark.safari
@vtest
class Test_C9721291_Verify_showing_tax_message_on_Quick_Bet_Betslip_after_registration_of_a_German_user(BaseSportTest, BaseBetSlipTest):
    """
    TR_ID: C9721291
    NAME: Verify showing tax message on Quick Bet/Betslip after registration of a German user
    DESCRIPTION: This test case verifies displaying of a tax message on 'Betslip' for a German user after registration
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: 1. devtools > Application tab > Local Storage > is cleared (so no "OX.countryCode" is available)
    PRECONDITIONS: 2. Login pop-up is opened on mobile
    """
    keep_browser_open = True
    bet_amount = 1.00

    def test_000_preconditions(self):
        """
        DESCRIPTION: create an event
        """
        category_id = self.ob_config.football_config.category_id
        if tests.settings.backend_env == 'prod':
            self.__class__.event = self.get_active_events_for_category(category_id=category_id)[0]
            self.__class__.selection_ids = self.get_active_event_selections_for_category(
                category_id=self.ob_config.football_config.category_id)
            self.__class__.event_id = self.event['event']['id']
            self.__class__.team1 = list(self.selection_ids.keys())[0]
            market_name = next((market['market']['name'] for market in self.event['event']['children']
                                if market.get('market').get('templateMarketName') == 'Match Betting'), None)
        else:
            self.__class__.event = self.ob_config.add_autotest_premier_league_football_event()
            self.__class__.event_id, self.__class__.team1, self.__class__.selection_ids = \
                self.event.event_id, self.event.team1, self.event.selection_ids
            market_name = self.ob_config.football_config.autotest_class.autotest_premier_league.market_name.replace('|',
                                                                                                                    '')
        self.__class__.expected_market_name = self.get_accordion_name_for_market_from_ss(ss_market_name=market_name)

    def test_001_tap_join_now(self):
        """
        DESCRIPTION: Tap 'Join now'
        EXPECTED: User is redirected to Account One
        """
        self.site.register_new_user(country='Germany', currency='EUR', state='Hamburg')
        # fix deposit during GVC adaptation
        # self.site.deposit_via_card(deposit_value=5)

        if self.device_type == 'desktop':
            self.navigate_to_page(name='/')
        else:
            self.site.wait_content_state('Homepage')

    def test_002_in_account_one__fill_in_all_necessary_fields_to_register_user__select_country_germany__tap_open_account_save_my_preferences__add_credit_cards_on_deposit_page__deposit_money_to_added_credit_card__close_deposit_page(self):
        """
        DESCRIPTION: In Account One:
        DESCRIPTION: - Fill in all necessary fields to register user
        DESCRIPTION: - Select Country 'Germany'
        DESCRIPTION: - Tap 'Open account', 'Save my preferences'
        DESCRIPTION: - Add credit cards on Deposit page
        DESCRIPTION: - Deposit money to added credit card
        DESCRIPTION: - Close Deposit page
        EXPECTED: - German user is navigated back to an app
        EXPECTED: - German user is logged in
        EXPECTED: - German user is navigated to Home page
        EXPECTED: - In Application > Local Storage > "OX.countryCode"="DE"
        """
        key_value = self.get_local_storage_cookie_value_as_dict('OX.USER').get('countryCode')
        self.assertEqual(key_value, 'DE',
                         msg=f'Value of cookie "OX.countryCode" does not match expected result "DE".'
                         f'Actual value of "OX.countryCode" is "{key_value}"')

    def test_003_mobileadd_any_selection_to_quick_bet(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Add any selection to 'Quick Bet'
        EXPECTED: - 'Quick Bet' appears with an added selection
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        if self.device_type in ['mobile', 'tablet']:
            self.navigate_to_edp(event_id=self.event_id)
            self.add_selection_from_event_details_to_quick_bet(market_name=self.expected_market_name)
            self.assertTrue(self.site.wait_for_quick_bet_panel(), msg='Quick Bet is not present')
            self.assertTrue(self.site.quick_bet_panel.has_german_tax_message(),
                            msg=f'"{vec.quickbet.TAX_5}" is not displayed')
            self.assertEqual(self.site.quick_bet_panel.german_tax_message_text, vec.quickbet.TAX_5,
                             msg=f'Mismatch in Actual: "{self.site.quick_bet_panel.german_tax_message_text}" and Expected: "{vec.quickbet.TAX_5}"')

    def test_004_mobileenter_valid_stake_amount__tap_bet_now(self):
        """
        DESCRIPTION: **Mobile:**
        DESCRIPTION: Enter valid Stake amount > Tap 'Bet Now'
        EXPECTED: - Bet is successfully placed
        EXPECTED: - Bet Receipt is displayed on 'Quick Bet'
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        if self.device_type in ['mobile', 'tablet']:
            quick_bet = self.site.quick_bet_panel.selection
            quick_bet.content.amount_form.input.value = self.bet_amount
            amount = float(quick_bet.content.amount_form.input.value)
            self.assertEqual(amount, self.bet_amount,
                             msg=f'Entered amount "{amount}" is not equal to expected "{self.bet_amount}"')
            self.site.quick_bet_panel.place_bet.click()
            bet_receipt_displayed = self.site.quick_bet_panel.wait_for_bet_receipt_displayed(timeout=25)
            self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
            self.assertTrue(self.site.quick_bet_panel.has_german_tax_message(),
                            msg=f'"{vec.quickbet.TAX_5}" is not displayed')
            self.assertEqual(self.site.quick_bet_panel.german_tax_message_text, vec.quickbet.TAX_5,
                             msg=f'Mismatch in Actual: "{self.site.quick_bet_panel.german_tax_message_text}" and Expected: "{vec.quickbet.TAX_5}"')

    def test_005___add_selections_to_betslip__open_betslip(self):
        """
        DESCRIPTION: - Add selection(s) to 'Betslip'
        DESCRIPTION: - Open 'Betslip'
        EXPECTED: - Added selection(s) is(are) available in the 'Betslip'
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        self.open_betslip_with_selections(selection_ids=(self.selection_ids[self.team1]))
        self.__class__.singles_section = self.get_betslip_sections().Singles
        self.assertTrue(self.singles_section, msg='Betslip Singles section is not displayed.')
        betslip = self.get_betslip_content()
        self.assertEquals(betslip.german_tax_message_text, vec.betslip.TAX_5,
                          msg=f'Actual: {betslip.german_tax_message_text} is not matched with '
                          f'Expected: "{vec.betslip.TAX_5}"')

    def test_006_enter_valid_stake_amount__tap_bet_now(self):
        """
        DESCRIPTION: Enter valid Stake amount > Tap 'Bet Now'
        EXPECTED: - Bet is successfully placed
        EXPECTED: - Bet Receipt is displayed on 'Betslip'
        EXPECTED: - Message: "A fee of 5% is applicable on winnings" is displayed below 'Stake' & 'Est. Returns'
        """
        self.place_single_bet()
        self.check_bet_receipt_is_displayed(timeout=25)
        bet_receipt_name = self.site.bet_receipt.footer
        self.assertTrue(bet_receipt_name.has_german_tax_message(), msg=f'"{vec.betslip.TAX_5}" is not displayed on betslip')
        self.assertEquals(bet_receipt_name.german_tax_message_text, vec.betslip.TAX_5,
                          msg=f'Actual: {bet_receipt_name.german_tax_message_text} is not matched with '
                          f'Expected: "{vec.betslip.TAX_5}"')
