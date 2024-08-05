import pytest
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul, wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@vtest
class Test_C65763183_Verify_whether_the_user_is_displayed_with_bet_receipt_popup_after_clicking_on_Got_it_CTA_in_luck_dip_animation_page(BaseGolfTest):
    """
    TR_ID: C65763183
    NAME: Verify whether the user is displayed with bet receipt popup after clicking on 'Got it' CTA in luck dip animation page
    DESCRIPTION: This test case verifies whether the user is displayed with betreceipt popup after clicking on 'Got it' CTA in luck dip animation page
    PRECONDITIONS: Lucky dip market should be created in OB for Golf sport
    PRECONDITIONS: Lucky dip should be configured in CMS
    """
    keep_browser_open = True
    bet_amount = 0.1

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_item('LuckyDip')
        if len(cms_config_lucky_dip) == 0 or not cms_config_lucky_dip.get('enabled'):
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')
        all_lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        event = all_lucky_dip_events[0]
        self.__class__.eventID = event['event']['id']

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes Application
        EXPECTED: User logs in successfully
        """
        self.site.login()

    def test_002_navigate_to_golf_edp_and_verify_if_the_lucky_dip_market_is_present(self):
        """
        DESCRIPTION: Navigate to Golf EDP and verify if the lucky dip market is present
        EXPECTED: Lucky dip market should be present in Golf EDP
        """
        self.navigate_to_edp(event_id = self.eventID)

    def test_003_click_on_the_lucky_dip_market_selection(self):
        """
        DESCRIPTION: Click on the lucky dip market selection
        EXPECTED: User should be navigated to lucky dip Landing page on clicking the selection
        """
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in edp_market_sections.keys()]
        self.assertIn("LUCKY DIP", edp_market_sections_name,
                      msg=f'Expected Lucky Dip market is not displayed in EDP page')
        market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'),
                          None)
        self.__class__.lucky_dip_section = edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()
        self.lucky_dip_section.odds.click()

    def test_004_verify_if_the_user_is_displayed_with_number_keypad_to_enter_stake_and_place_bet_button_in_lucky_dip_landing_page(self):
        """
        DESCRIPTION: Verify if the user is displayed with Number keypad to enter stake and place bet button in lucky dip landing page
        EXPECTED: User should be able to enter stake and able to click on place bet
        """
        quick_bet = wait_for_result(lambda : self.site.quick_bet_panel.selection, timeout=5)
        self.assertTrue(quick_bet, msg="lucky dip landing page is not displayed for place bet")
        wait_for_haul(3)
        quick_bet.content.amount_form.input.value = self.bet_amount
        amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(quick_bet.content.amount_form.input.value, amount,
                         msg=f'Actual amount "{quick_bet.content.amount_form.input.value}" does not match '
                             f'expected "{amount}"')
        place_bet_button = self.site.quick_bet_panel.place_bet
        self.assertTrue(place_bet_button, msg="place bet button is not available")
        place_bet_button.click()

    def test_005_verify_if_the_user_is_displayed_with_lucky_dip_animation_page(self):
        """
        DESCRIPTION: Verify if the user is displayed with lucky dip animation page
        EXPECTED: 'Lucky dip' animation page should be displayed with below content
        EXPECTED: 1. Player name(generated with RNG algorithm)
        EXPECTED: 2. Potential returns
        EXPECTED: 3. 'Got it' CTA
        """
        lucky_dip_got_it_animation = wait_for_result(
            lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=10), timeout=5)
        self.assertTrue(lucky_dip_got_it_animation, msg='Lucky Dip Animation is not displayed to the user')
        lucky_dip_player_name = self.site.lucky_dip_got_it_panel.lucky_dip_player_name
        self.assertTrue(lucky_dip_player_name, msg="Player name is not present in 'lucky dip' animation page")
        lucky_dip_potential_returns = self.site.lucky_dip_got_it_panel.lucky_dip_potential_returns_value
        self.assertTrue(lucky_dip_potential_returns,
                        msg="Potential returns is not present in 'lucky dip' animation page")
        got_it_cta_button = self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button
        self.assertTrue(got_it_cta_button, msg="'Got it' CTA button is not present in 'lucky dip' animation page")
        got_it_cta_button.click()
    def test_006_verify_if_the_user_is_displayed_bet_receipt_pop_up_on_clicking_got_it_cta(self):
        """
        DESCRIPTION: Verify if the user is displayed bet receipt pop-up on clicking 'Got it' CTA
        EXPECTED: User should be displayed with bet receipt popup with luck dip market details, stake and potential returns.
        """
        bet_receipt_displayed = wait_for_result(
            lambda: self.site.quick_bet_panel.wait_for_lucky_dip_bet_receipt_displayed(), timeout=10)
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')