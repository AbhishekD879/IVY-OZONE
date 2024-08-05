import pytest
from tests.base_test import vtest
from crlat_siteserve_client.utils.exceptions import SiteServeException
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
class Test_C65763326_Verify_the_content_in_Player_selection_card_after_the_bet_placement(BaseGolfTest):
    """
    TR_ID: C65763326
    NAME: Verify the content in Player selection card after the bet placement
    DESCRIPTION: This testcase verifies the content displayed in Player selection card, after the user places a bet on Lucky Dip Market
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Lucky Dip should be configured in CMS
    """
    keep_browser_open = True
    bet_amount = 0.1

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
        self.__class__.event_fractional_odds = self.get_decimal_and_fractional_prices_in_ob_config_by_event(event=event).get('fractionalPrice')
        self.__class__.event_decimal_odds = self.get_decimal_and_fractional_prices_in_ob_config_by_event(event=event).get('decimalPrice')
        if not self.event_fractional_odds:
            raise SiteServeException(f'No odds available for the event {self.eventID}')
        self.cms_configuration = self.cms_config.get_lucky_dip_configuration()
        self.__class__.cms_player_card_description = self.cms_configuration['luckyDipFieldsConfig']['playerCardDesc'].strip()
        self.__class__.cms_potential_returns_description = self.cms_configuration['luckyDipFieldsConfig']['potentialReturnsDesc'].strip()
        self.__class__.cms_got_it_button = self.cms_configuration['luckyDipFieldsConfig']['gotItCTAButton'].strip()
        self.__class__.expected_potential_returns = self.calculate_estimated_returns(bet_amount=self.bet_amount, odds=[self.event_fractional_odds])

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
        self.__class__.lucky_dip_section = edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()
        self.lucky_dip_section.odds.click()
        lucky_dip_QB_splash_container = wait_for_result(
            lambda: self.lucky_dip_section.lucky_dip_QB_splash_container.has_lucky_dip_animation(timeout=10),
            timeout=3)
        self.assertTrue(lucky_dip_QB_splash_container, msg=f"Lucky Dip animation is not displayed after clicking odds")

    def test_004_enter_the_required_amount_of_stake_and_click_on_place_bet_cta(self):
        """
        DESCRIPTION: Enter the required amount of stake and click on Place Bet CTA
        EXPECTED: Bet is placed successfully, and player selection card is displayed
        """
        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        wait_for_haul(5)
        self.quick_bet.content.amount_form.input.value = self.bet_amount
        amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(self.quick_bet.content.amount_form.input.value, amount,
                         msg=f'Actual amount "{self.quick_bet.content.amount_form.input.value}" does not match '
                             f'expected "{amount}"')
        self.site.quick_bet_panel.place_bet.click()
        lucky_dip_got_it_animation = wait_for_result(lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=10),
                                                     timeout=3)
        self.assertTrue(lucky_dip_got_it_animation, msg='Lucky Dip Animation is not displayed to the user')
        self.__class__.expected_lucky_dip_player_name = self.site.lucky_dip_got_it_panel.lucky_dip_player_name


    def test_005_verify_the_content_displayed_in_player_selection_card(self):
        """
        DESCRIPTION: Verify the content displayed in Player selection card
        EXPECTED: The below content should be displayed on the player card and the content displayed should be the same as configured in cms
        EXPECTED: 1. Banner for Player selection card
        EXPECTED: 2.Title for the Animation card
        EXPECTED: 3.Odds for the player selected
        EXPECTED: 4.Potential returns for the selected player
        """
        actual_player_card_description = self.site.lucky_dip_got_it_panel.lucky_dip_player_card_description.upper()
        self.assertEqual(actual_player_card_description, self.cms_player_card_description.upper(),
                         f"Actual player card description {actual_player_card_description} does not match configured player card description {self.cms_player_card_description.upper()}")
        actual_potential_returns_description = self.site.lucky_dip_got_it_panel.lucky_dip_potential_returns_description.upper()
        self.assertEqual(actual_potential_returns_description, self.cms_potential_returns_description.upper(),
                         f"Actual potential returns description{actual_potential_returns_description} does not match configured potential returns description {self.cms_potential_returns_description.upper()}")
        actual_got_it_button = self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button_description.upper()
        self.assertEqual(actual_got_it_button, self.cms_got_it_button.upper(),
                         f"Actual got it button description {actual_got_it_button} does not match configured got it button description {self.cms_got_it_button.upper()}")
        actual_outcome_value = self.site.lucky_dip_got_it_panel.outcome_value
        self.assertEqual(actual_outcome_value, self.event_fractional_odds,
                         f"Actual outcome value{actual_outcome_value} does not match configured outcome value {self.event_fractional_odds}")
        actual_potential_returns_value = self.site.lucky_dip_got_it_panel.lucky_dip_potential_returns_value
        self.assertEqual(float(actual_potential_returns_value), float(self.expected_potential_returns),
                         f"Actual potential returns value{actual_potential_returns_value}does not match configured potential returns value {self.expected_potential_returns}")