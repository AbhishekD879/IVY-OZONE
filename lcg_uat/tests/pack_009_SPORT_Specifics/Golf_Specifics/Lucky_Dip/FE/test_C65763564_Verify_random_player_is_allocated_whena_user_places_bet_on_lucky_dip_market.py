import pytest
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_haul, wait_for_result
import voltron.environments.constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.lucky_dip
@pytest.mark.mobile_only
@pytest.mark.quick_bet
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest

class Test_C65763564_Verify_random_player_is_allocated_whena_user_places_bet_on_lucky_dip_market(BaseGolfTest):
    """
    TR_ID: C65763564
    NAME: Verify random player is allocated , whena user places bet on lucky dip market
    DESCRIPTION: This testcase verifies, that a random player is allocated, when a user places bet on Lucky Dip market
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Lucky Dip should be configured in CMS
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
        self.__class__.playerName = self.get_selected_golfer_name_in_ob_config(event=event)
        lucky_dip_configurations = self.cms_config.get_lucky_dip_configuration()
        self.__class__.expected_step1 = lucky_dip_configurations['luckyDipFieldsConfig']['betPlacementStep1'].strip()
        self.__class__.expected_step2 = lucky_dip_configurations['luckyDipFieldsConfig']['betPlacementStep2'].strip()
        self.__class__.expected_step3 = lucky_dip_configurations['luckyDipFieldsConfig']['betPlacementStep3'].strip()



    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User successfully logs in.
        """
        self.site.login()

    def test_002_navigate_to_golf_event_in_which_lucky_dip_market_is_configured(self):
        """
        DESCRIPTION: Navigate to Golf event in which Lucky Dip Market is configured
        EXPECTED: Golf EDP page is displayed with Luck Dip Market and respective Odds
        """
        self.navigate_to_edp(event_id=self.eventID)

    def test_003_click_on_odds(self):
        """
        DESCRIPTION: Click on odds
        EXPECTED: Lucky Dip Animation is displayed to the user with ODDS and prompts the user to enter stake and Placebet
        """
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in edp_market_sections.keys()]
        self.assertIn("OUTRIGHT", edp_market_sections_name,
                      msg=f'Expected OUTRIGHT market is not displayed in EDP page')
        market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'OUTRIGHT'),
                          None)
        outright_section = edp_market_sections.get(market_key)
        outright_section.show_all_button.scroll_to()
        outright_section.show_all_button.click()
        outright_section.scroll_to()
        outright_players = outright_section.items_as_ordered_dict
        self.__class__.outright_players = [player_name.upper() for player_name in outright_players]
        self.assertIn("LUCKY DIP", edp_market_sections_name,
                      msg=f'Expected Lucky Dip market is not displayed in EDP page')
        market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'),None)
        self.lucky_dip_section = edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()
        self.lucky_dip_section.odds.click()
        self.assertTrue(
            self.lucky_dip_section.lucky_dip_QB_splash_container.has_lucky_dip_animation(expected_result=True),
            f"Lucky Dip animation is not displayed after clicking on odds")
        Actual_step1 = self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_step("1")
        if Actual_step1 != self.expected_step1:
            wait_for_haul(3)
            Actual_step1 = self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_step("1")
        Actual_step2 = self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_step("2")
        Actual_step3 = self.lucky_dip_section.lucky_dip_QB_splash_container.get_lucky_dip_content_step("3")
        self.assertEqual(Actual_step1, self.expected_step1, f'Actual Step 1 message : "{Actual_step1}" is not same as expected step 1 message : {self.expected_step1}')
        self.assertEqual(Actual_step2, self.expected_step2, f'Actual Step 2 message : "{Actual_step2}" is not same as expected step 2 message : {self.expected_step2}')
        self.assertEqual(Actual_step3, self.expected_step3, f'Actual Step 3 message : "{Actual_step3}" is not same as expected step 3 message : {self.expected_step3}')
        self.assertTrue(self.site.quick_bet_panel.selection.content.odds_value, f'Odds are not displayed in quick bet panel')

    def test_004_enter_the_stake_and_click_on_place_bet_cta(self):
        """
        DESCRIPTION: Enter the stake and click on Place Bet CTA
        EXPECTED: Bet placement should be successful. Player should be randomly allocated to the user
        """
        self.quick_bet = self.site.quick_bet_panel.selection
        wait_for_haul(3)
        self.quick_bet.content.amount_form.input.value = self.bet_amount
        amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(self.quick_bet.content.amount_form.input.value, amount,
                         msg=f'Actual amount "{self.quick_bet.content.amount_form.input.value}" does not match '
                             f'expected "{amount}"')
        self.odds = self.quick_bet.content.odds_value
        self.total_stake = self.quick_bet.bet_summary.total_stake
        self.total_est_return = self.quick_bet.bet_summary.total_estimate_returns
        self.market_name = self.quick_bet.content.market_name
        self.event_name = self.quick_bet.content.event_name
        self.site.quick_bet_panel.place_bet.click()
        lucky_dip_animation = wait_for_result(lambda: self.site.lucky_dip_got_it_panel.lucky_dip_player_name,
                                              timeout=10)
        self.assertTrue(lucky_dip_animation, msg='Lucky Dip Animation is not displayed to the user')
        self.actual_player_name = self.site.lucky_dip_got_it_panel.lucky_dip_player_name
        self.assertNotEquals(self.actual_player_name, self.playerName, msg=f'Actual player name : {self.actual_player_name} is same as selected player name in OB : {self.playerName}')
        self.assertIn(self.actual_player_name.upper(), self.outright_players,
                      msg=f'Actual player name" "{self.actual_player_name}" '
                          f'not in expected player names: "{self.outright_players}"')
        self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.click()
        self.bet_receipt_displayed = wait_for_result(
            lambda: self.site.quick_bet_panel.wait_for_lucky_dip_bet_receipt_displayed(), timeout=10)
        self.assertTrue(self.bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.bet_receipt = self.site.quick_bet_panel.lucky_dip_outright_bet_receipt
        self.assertEqual(self.bet_receipt.lucky_dip_bet_placement_messeage, vec.betslip.SUCCESS_BET,
                         msg=f'Text "{self.bet_receipt.lucky_dip_bet_placement_messeage}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        lucky_dip_bet_receipt_player_name = self.bet_receipt.lucky_dip_player_name.split('to')[0].strip()
        self.assertEqual(lucky_dip_bet_receipt_player_name.upper(), self.actual_player_name.upper(),
                         msg=f'Actual player name" "{lucky_dip_bet_receipt_player_name.upper()}" '
                             f'does not match with expected player name: "{self.actual_player_name.upper()}"')
