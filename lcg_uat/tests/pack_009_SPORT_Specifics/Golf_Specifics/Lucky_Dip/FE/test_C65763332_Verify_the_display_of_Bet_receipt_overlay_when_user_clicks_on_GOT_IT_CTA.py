import pytest
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result, wait_for_haul


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@vtest
class Test_C65763332_Verify_the_display_of_Bet_receipt_overlay_when_user_clicks_on_GOT_IT_CTA(BaseGolfTest):
    """
    TR_ID: C65763332
    NAME: Verify the display of Bet receipt overlay, when user clicks on 'GOT IT' CTA
    DESCRIPTION: This testcase verifies the display of Bet Receipt overlay when user clicks on 'GOT IT' CTA in Lucky Dip Player card
    """
    keep_browser_open = True
    bet_amount = 0.1

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_structure()['LuckyDip']['enabled']
        if not cms_config_lucky_dip:
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')
        all_lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        event = all_lucky_dip_events[0]
        self.__class__.eventID = event['event']['id']

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to ladbrokes application
        EXPECTED: User logs in successfully
        """
        self.site.login()

    def test_002_navigate_to_golf_event_in_which_lucky_dip_market_is_configured(self):
        """
        DESCRIPTION: Navigate to Golf event in which Lucky Dip Market is configured
        EXPECTED: Golf EDP page is displayed with Luck Dip Market and respective Odds
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_003_click_on_the_odds(self):
        """
        DESCRIPTION: Click on the Odds
        EXPECTED: Lucky Dip Animation is displayed to the user with ODDS and prompts the user to enter stake and Placebet
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
        self.assertTrue(self.lucky_dip_section.lucky_dip_QB_splash_container.has_lucky_dip_animation(),
                        f"Lucky Dip animation is not displayed")

    def test_004_enter_the_required_amount_of_stake_and_click_on_place_bet_cta(self):
        """
        DESCRIPTION: Enter the required amount of stake and click on Place Bet CTA
        EXPECTED: Bet is placed successfully, and player selection card is displayed
        """
        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        wait_for_haul(3)
        self.quick_bet.content.amount_form.input.value = self.bet_amount
        amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(self.quick_bet.content.amount_form.input.value, amount,
                         msg=f'Actual amount "{self.quick_bet.content.amount_form.input.value}" does not match '
                             f'expected "{amount}"')
        self.site.quick_bet_panel.place_bet.click()
        lucky_dip_got_it_animation = wait_for_result(
            lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=10),
            timeout=3)
        self.assertTrue(lucky_dip_got_it_animation, msg='Lucky Dip Animation is not displayed to the user')

    def test_005_click_on_the_got_it_cta_in_the_player_card(self):
        """
        DESCRIPTION: Click on the 'GOT IT' CTA in the player card
        EXPECTED: Bet receipt Overlay should be displayed to the user
        """
        self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.click()
        bet_receipt_displayed = wait_for_result(lambda: self.site.quick_bet_panel.wait_for_lucky_dip_bet_receipt_displayed(), timeout=10)
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
