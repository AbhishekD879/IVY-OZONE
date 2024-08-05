import pytest
from crlat_siteserve_client.utils.exceptions import SiteServeException
import tests
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
class Test_C65765001_Verify_the_contents_displayed_in_Lucky_Dip_Landing_page(BaseGolfTest):
    """
    TR_ID: C65765001
    NAME: Verify the contents displayed in Lucky Dip Landing page
    DESCRIPTION: This testcase verifies the content displayed in Lucky Dip Landing page.
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Lucky Dip should be configured in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be enabled in CMS
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_structure()['LuckyDip']['enabled']
        if not cms_config_lucky_dip:
            raise CmsClientException(f'Lucky Dip is not enabled in CMS')
        all_lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        event = all_lucky_dip_events[0]
        self.__class__.eventID = event['event']['id']
        self.__class__.expected_event_odds = self.get_decimal_and_fractional_prices_in_ob_config_by_event(event=event).get('fractionalPrice')
        if not self.expected_event_odds:
            raise SiteServeException(f'No odds available for the event {self.eventID}')
        cms_luckydip_configuaion = self.cms_config.get_lucky_dip_configuration()
        luckydip_fields_config = cms_luckydip_configuaion.get('luckyDipFieldsConfig')
        self.__class__.expected_luckydip_welcome_message = luckydip_fields_config['welcomeMessage'].strip()
        self.__class__.expected_luckydip_bet_placement_title = luckydip_fields_config['betPlacementTitle'].strip()
        self.__class__.expected_luckydip_bet_placement_step1 = luckydip_fields_config['betPlacementStep1'].strip()
        self.__class__.expected_luckydip_bet_placement_step2 = luckydip_fields_config['betPlacementStep2'].strip()
        self.__class__.expected_luckydip_bet_placement_step3 = luckydip_fields_config['betPlacementStep3'].strip()
        self.__class__.expected_luckydip_terms_and_conditions_URL = luckydip_fields_config['termsAndConditionsURL']
        start_index = self.expected_luckydip_terms_and_conditions_URL.find('href="') + 6
        end_index = self.expected_luckydip_terms_and_conditions_URL.find('">', start_index)
        self.__class__.expected_terms_and_conditions_url = self.expected_luckydip_terms_and_conditions_URL[start_index:end_index]

    def test_001_log_in_to_ladbrokes_application_and_navigate_to_golf_event_to_which_lucky_dip_market_is_configured(self):
        """
        DESCRIPTION: Log in to Ladbrokes application and Navigate to Golf event to which Lucky Dip Market is configured
        EXPECTED: User is Navigated to Golf EDP with Lucky Dip Market. Odds are displayed beside the Market
        """
        self.site.login()
        self.navigate_to_edp(event_id=self.eventID)
        self.edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.edp_market_sections_name = [market.upper() for market in self.edp_market_sections.keys()]
        self.assertIn("LUCKY DIP", self.edp_market_sections_name,
                      msg=f'Lucky Dip market is not displayed in EDP page')
        market_key = next(
            (section_name for section_name in self.edp_market_sections if section_name.upper() == 'LUCKY DIP'),
            None)
        self.__class__.lucky_dip_section = self.edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()
        self.assertTrue(self.lucky_dip_section.odds, f"Odds are not displayed beside the Market")

    def test_002_click_on_the_odds(self):
        """
        DESCRIPTION: Click on the Odds
        EXPECTED: Lucky Dip Animation is displayed. User is in Lucky Dip Landing Page
        EXPECTED: Lucky Dip banner is displayed to the user
        """
        self.lucky_dip_section.odds.click()
        self.assertTrue(self.lucky_dip_section.lucky_dip_QB_splash_container.has_lucky_dip_animation(expected_result=True), f"Lucky Dip animation is not displayed")

    def test_003_verify_the_content_displayed_in_lucky_dip_landing_page(self):
        """
        DESCRIPTION: Verify the content displayed in Lucky Dip Landing Page
        EXPECTED: The below content should be displayed to the user.
        EXPECTED: 1.Lucky Dip banner should be displayed below the respective league/competition/championship
        EXPECTED: 2.Description is displayed below the banner. Description content should be same as the content configured in CMS Description field
        EXPECTED: 3.Bet Placement information title, Step1, Step2, Step3
        EXPECTED: 4.Terms and conditions link
        EXPECTED: 5.When clicked on terms and conditions link, User should be redirected to the url configured for terms and conditions url in cms
        EXPECTED: 6.Odds and stake field should be displayed
        EXPECTED: 7.Number Keypad to enter the stake
        EXPECTED: 8.Close (X) icon is displayed on top right corner on the lucky dip banner
        """
        wait_for_result(lambda: self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_info,timeout=5)
        actual_luckydip_welcome_message = self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_info.upper()
        if self.expected_luckydip_welcome_message.upper() != actual_luckydip_welcome_message:
            wait_for_haul(3)
            actual_luckydip_welcome_message = self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_info.upper()
        self.assertEqual(self.expected_luckydip_welcome_message.upper(), actual_luckydip_welcome_message,
                         msg=f'Actual welcome message is "{actual_luckydip_welcome_message}" but expected is "{self.expected_luckydip_welcome_message.upper()}"')
        actual_luckydip_bet_placement_title = self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_title.upper()
        self.assertEqual(self.expected_luckydip_bet_placement_title.upper(), actual_luckydip_bet_placement_title,
                         msg=f'Actual bet placement title is "{actual_luckydip_bet_placement_title}" but expected is "{self.expected_luckydip_bet_placement_title.upper()}"')
        actual_luckydip_bet_placement_step1 = self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_step(step="1").upper()
        self.assertEqual(self.expected_luckydip_bet_placement_step1.upper(), actual_luckydip_bet_placement_step1,
                         msg=f'Actual bet placement step1 is "{actual_luckydip_bet_placement_step1}" but expected is "{self.expected_luckydip_bet_placement_step1.upper()}"')
        actual_luckydip_bet_placement_step2 = self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_step(step='2').upper()
        self.assertEqual(self.expected_luckydip_bet_placement_step2.upper(), actual_luckydip_bet_placement_step2,
                         msg=f'Actual bet placement step2 is "{actual_luckydip_bet_placement_step2}" but expected is "{self.expected_luckydip_bet_placement_step2.upper()}"')
        actual_luckydip_bet_placement_step3 = self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_step(step='3').upper()
        self.assertEqual(self.expected_luckydip_bet_placement_step3.upper(), actual_luckydip_bet_placement_step3,
                         msg=f'Actual bet placement step3 is "{actual_luckydip_bet_placement_step3}" but expected is "{self.expected_luckydip_bet_placement_step3.upper()}"')
        is_close_icon_exists = self.lucky_dip_section.lucky_dip_QB_splash_container.has_close_icon_on_lucky_dip_popup(expected_result=True)
        self.assertTrue(is_close_icon_exists, f"Close(X) icon on Lukcy dip popup is not displayed")
        is_terms_and_conditions_link_exists = self.lucky_dip_section.lucky_dip_QB_splash_container.has_lucky_dip_content_terms_and_conditions_link(expected_result=True)
        self.assertTrue(is_terms_and_conditions_link_exists,
                        f"Terms and conditions link on Lukcy dip popup is not displayed")
        actual_terms_and_conditions_url = self.lucky_dip_section.lucky_dip_QB_splash_container.lucky_dip_content_terms_and_conditions_link.get_attribute("href")
        self.assertEqual(self.expected_terms_and_conditions_url, actual_terms_and_conditions_url, f'Actual terms and conditions link is "{actual_terms_and_conditions_url}" but expected is "{self.expected_terms_and_conditions_url}"')
        self.quick_bet = self.site.quick_bet_panel.selection
        self.actual_event_odds = self.quick_bet.content.odds_value
        self.assertIn(self.expected_event_odds,self.actual_event_odds,msg=f'Actual event odds are "{self.actual_event_odds}" but expected is "{self.expected_event_odds}"')
        self.assertTrue(self.quick_bet.content.amount_form.input.is_displayed(),msg='Stake field is not displayed')


