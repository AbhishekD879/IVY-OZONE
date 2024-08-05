import pytest
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException

@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@vtest

class Test_C65763329_Verify_the_Odds_displayed_in_the_Player_selection_card_are_fetched_from_Open_Bet(BaseGolfTest):
    """
    TR_ID: C65763329
    NAME: Verify the Odds displayed in the Player selection card are fetched from Open Bet
    DESCRIPTION: This testcase verifies the Odds displayed in the Player selection card are fetched from Open bet
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_structure()['LuckyDip']['enabled']
        if not cms_config_lucky_dip:
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')
        all_lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        self.__class__.event = all_lucky_dip_events[0]
        self.__class__.eventID = self.event['event']['id']
        event_odds = self.event['event']['children'][0]['market']['children'][0]['outcome']['children'][0]['price']
        if event_odds:
            price_num = event_odds['priceNum']
            price_den = event_odds['priceDen']
            self.__class__.expected_fractional_odds = f"{price_num}/{price_den}"
        else:
            raise SiteServeException(f'No odds available for the event {self.eventID}')

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
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
        lucky_dip_section = edp_market_sections.get(market_key)
        lucky_dip_section.scroll_to()
        self.assertTrue(lucky_dip_section.odds.is_displayed(), msg='odds not available')
        selection_odds = lucky_dip_section.odds.text
        self.assertEqual(selection_odds, self.expected_fractional_odds, msg="The displayed odds do not match the fetched odds")
        lucky_dip_section.odds.click()
        self.assertTrue(lucky_dip_section.lucky_dip_QB_splash_container.has_lucky_dip_animation(),
                        f"Lucky Dip animation is not displayed")

    def test_004_verify_the_odds_displayed_in_lucky_dip_landing_page(self):
        """
        DESCRIPTION: Verify the Odds displayed in Lucky Dip landing page
        EXPECTED: Odds displayed in the landing page should be fetched from openbet
        """
        actual_quick_bet_odds = self.site.quick_bet_panel.selection.content.odds
        self.assertEqual(actual_quick_bet_odds, self.expected_fractional_odds,
                         msg=f"Actual odds {actual_quick_bet_odds} does not match with the expected {self.expected_fractional_odds}")