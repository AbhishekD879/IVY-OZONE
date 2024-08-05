import pytest
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
import voltron.environments.constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@vtest
class Test_C65765062_Verify_Login_and_Place_ber_CTA_should_be_greyed_out_till_the_user_enters_desired_stake(BaseGolfTest):
    """
    TR_ID: C65765062
    NAME: Verify Login and Place ber CTA should be greyed out, till the user enters desired stake
    DESCRIPTION: This testcase verifies that the LOGIN and PLACE BET CTA should be greyed out, till the stake is entered
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Lucky Dip should be configured in CMS
    """
    keep_browser_open = True
    bet_button_name = vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_structure()['LuckyDip']['enabled']
        if not cms_config_lucky_dip:
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')
        all_lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        event = all_lucky_dip_events[0]
        self.__class__.eventID = event['event']['id']

    def test_001_launch_ladbrokes_application_and_navigate_to_golf_event_to_which_lucky_dip_market_is_configured(self):
        """
        DESCRIPTION: Launch Ladbrokes application and Navigate to Golf event to which Lucky Dip Market is configured
        EXPECTED: User is Navigated to Golf EDP with Lucky Dip Market. Odds are displayed beside the Market
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_002_click_on_the_odds(self):
        """
        DESCRIPTION: Click on the Odds
        EXPECTED: Lucky dip Animation is displayed, and user is displayed with Lucky Dip landing page
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

    def test_003_verify_login_and_placebet_cta_on_lucky_dip_landing_page(self):
        """
        DESCRIPTION: Verify LOGIN and PLACEBET CTA on Lucky DIP landing page
        EXPECTED: LOGIN AND PLACEBET CTA should be disabled
        """
        self.betnow_btn = self.site.quick_bet_panel.place_bet
        betnow_btn_enabled_status = self.betnow_btn.is_enabled()
        self.assertFalse(betnow_btn_enabled_status, msg='Bet Now button is not disabled')
        self.betnow_btn_name = self.betnow_btn.name
        if isinstance(self.bet_button_name, (list, tuple)):
            self.assertTrue(any(True for i in self.bet_button_name if self.betnow_btn_name == i),
                            msg=f'Button text "{self.betnow_btn_name}" does not match any of expected "{self.bet_button_name}"')
        else:
            self.assertEqual(self.betnow_btn_name, self.bet_button_name,
                             msg=f'Button text "{self.betnow_btn_name}" does not match expected "{self.bet_button_name}"')



    def test_004_enter_the_stake_and_verify_login_and_placebet_cta(self):
        """
        DESCRIPTION: Enter the stake and verify LOGIN AND PLACEBET CTA
        EXPECTED: LOGIN AND PLACEBET CTA should be enabled
        """
        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        self.quick_bet.content.amount_form.input.value = self.bet_amount
        amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(self.quick_bet.content.amount_form.input.value, amount,
                         msg=f'Actual amount "{self.quick_bet.content.amount_form.input.value}" does not match '
                             f'expected "{amount}"')
        self.betnow_btn = self.site.quick_bet_panel.place_bet
        betnow_btn_enabled_status = self.betnow_btn.is_enabled()
        self.assertTrue(betnow_btn_enabled_status, msg='Bet Now button is not disabled')
        self.betnow_btn_name = self.betnow_btn.name
        if isinstance(self.bet_button_name, (list, tuple)):
            self.assertTrue(any(True for i in self.bet_button_name if self.betnow_btn_name == i),
                            msg=f'Button text "{self.betnow_btn_name}" does not match any of expected "{self.bet_button_name}"')
        else:
            self.assertEqual(self.betnow_btn_name, self.bet_button_name,
                             msg=f'Button text "{self.betnow_btn_name}" does not match expected "{self.bet_button_name}"')

