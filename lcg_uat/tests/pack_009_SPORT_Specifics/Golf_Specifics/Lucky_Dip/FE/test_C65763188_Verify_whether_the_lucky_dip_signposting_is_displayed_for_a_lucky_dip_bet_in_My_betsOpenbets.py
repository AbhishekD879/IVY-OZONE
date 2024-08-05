import pytest
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from voltron.utils.waiters import wait_for_result, wait_for_haul
import voltron.environments.constants as vec


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@vtest
class Test_C65763188_Verify_whether_the_lucky_dip_signposting_is_displayed_for_a_lucky_dip_bet_in_My_betsOpenbets(BaseGolfTest):
    """
    TR_ID: C65763188
    NAME: Verify whether the lucky dip signposting is displayed for a lucky dip bet in My bets>Openbets
    DESCRIPTION: This test case verifies whether the lucky dip signposting is displayed for a lucky dip bet in My bets&gt;Openbets
    PRECONDITIONS: Lucky dip market should be created in OB for Golf sport
    PRECONDITIONS: Lucky dip should be configured in CMS
    PRECONDITIONS: Lucky dip bet should be placed
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
        event= self.get_active_lucky_dip_events(all_available_events=True)[0]
        self.__class__.eventID = event['event']['id']

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes Application
        EXPECTED: User logs in successfully
        """
        self.site.login()

    def test_002_navigate_to_golf_edp_and_place_a_bet_on_luck_dip_market(self):
        """
        DESCRIPTION: Navigate to Golf EDP and place a bet on luck dip market
        EXPECTED: User should be able to place lucky dip bet
        """
        self.navigate_to_edp(event_id=self.eventID)
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in edp_market_sections.keys()]
        self.assertIn("LUCKY DIP", edp_market_sections_name,
                      msg=f'Expected Lucky Dip market is not displayed in EDP page')
        market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'),
                          None)
        self.__class__.lucky_dip_section = edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()
        self.lucky_dip_section.odds.click()
        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        wait_for_haul(3)
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
        self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.click()
        bet_receipt_displayed = wait_for_result(lambda: self.site.quick_bet_panel.wait_for_lucky_dip_bet_receipt_displayed(), timeout=10)
        self.assertTrue(bet_receipt_displayed, msg='Bet Receipt is not shown')
        self.__class__.bet_receipt = self.site.quick_bet_panel.lucky_dip_outright_bet_receipt
        self.assertEqual(self.bet_receipt.lucky_dip_bet_placement_messeage, vec.betslip.SUCCESS_BET,
                         msg=f'Actual Bet Placement success Message: "{self.bet_receipt.lucky_dip_bet_placement_messeage}" '
                             f'is not equal to expected "{vec.betslip.SUCCESS_BET}"')
        self.__class__.lucky_dip_bet_receipt_player_name = self.bet_receipt.lucky_dip_player_name.split('to')[0].strip()
        self.assertEqual(self.lucky_dip_bet_receipt_player_name.upper(), self.expected_lucky_dip_player_name.upper(),
                         msg=f'Actual Player name" "{self.lucky_dip_bet_receipt_player_name.upper()}" '
                             f'does not match with expected player name: "{self.expected_lucky_dip_player_name.upper()}"')
        self.bet_receipt.lucky_dip_close_button.click()
    def test_003_check_whether_the_lucky_dip_bet_is_displayed_in_my_betsampgtopen_bets(self):
        """
        DESCRIPTION: Check whether the lucky dip bet is displayed in My bets&amp;gt;Open bets
        EXPECTED: Lucky dip bet should be displayed in My bets&amp;gt;Open bets like other bets
        """
        self.site.open_my_bets_open_bets()
        open_bets = wait_for_result(lambda: self.site.open_bets.tab_content.accordions_list.items_as_ordered_dict,
                                    name='waiting for bets found on "Open Bets" page', expected_result=True,
                                    timeout=20)
        self.assertTrue(open_bets, msg='No bets found in open bet')
        self.__class__.bet_leg = list(open_bets.values())[0]
        player_name = self.bet_leg.outcome_name
        self.assertEqual(player_name, self.lucky_dip_bet_receipt_player_name,
                      msg=f'Actual Player Name:"{player_name}" is not same as'
                          f'Expected Player Name: "{self.lucky_dip_bet_receipt_player_name}"')

    def test_004_check_if_the_lucky_dip_signposting_is_displayed_for_a_placed_bet_in_my_betsampgtopen_bets(self):
        """
        DESCRIPTION: Check if the lucky dip signposting is displayed for a placed bet in My bets&amp;gt;Open bets
        EXPECTED: Lucky dip signposting should be displayed for a placed bet in My bets&amp;gt;open bets
        """
        lucky_dip_icon_text = self.bet_leg.lucky_dip_icon
        self.assertEqual(lucky_dip_icon_text, "LUCKY DIP",
                      msg=f'Actual Lucky Dip signpost:"{lucky_dip_icon_text}" is not same as'
                          f'Expected Lucky dip signpost: "{"LUCKY DIP"}"')
