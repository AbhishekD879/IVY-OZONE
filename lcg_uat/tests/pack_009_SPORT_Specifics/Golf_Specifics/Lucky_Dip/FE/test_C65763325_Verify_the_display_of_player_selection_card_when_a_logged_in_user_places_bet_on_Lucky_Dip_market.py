import pytest
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
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
class Test_C65763325_Verify_the_display_of_player_selection_card_when_a_logged_in_user_places_bet_on_Lucky_Dip_market(BaseSportTest, BaseGolfTest):
    """
    TR_ID: C65763325
    NAME: Verify the display of player selection card, when a logged in user places bet on Lucky Dip market
    DESCRIPTION: This testcase verifies the display of player selection card, for a logged in user after placing the bet on lucky Dip market
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Lucky Dip should be configured in CMS
    """
    keep_browser_open = True
    bet_amount = 0.10

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_structure()['LuckyDip']['enabled']
        if not cms_config_lucky_dip:
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')
        event = self.get_active_lucky_dip_events(number_of_events=1, all_available_events=True)[0]['event']
        self.__class__.sport_name = event['categoryCode'].upper()
        self.__class__.event_name = event['name'].upper()
        self.__class__.event_section_name = event['className'].upper() + " - " + event['typeName'].upper()

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User logs in successfully
        """
        self.site.login()

    def test_002_navigate_to_golf_sport_and_click_on_the_event_on_which_lucky_dip_market(self):
        """
        DESCRIPTION: Navigate to Golf Sport and click on the event on which Lucky Dip Market
        EXPECTED: Lucky Dip Market with respective Odds are displayed in the EDP page
        """
        # Mobile specific
        self.site.open_sport(name=vec.SB.ALL_SPORTS)
        self.site.all_sports.a_z_sports_section.click_item(item_name=self.sport_name)
        self.expected_sport_tab = self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,
                                                            category_id=self.ob_config.golf_config.category_id)
        self.site.golf.tabs_menu.click_button(self.expected_sport_tab)
        self.assertEqual(self.site.golf.tabs_menu.current, self.expected_sport_tabs.outrights,
                         msg=f'"{self.expected_sport_tabs.outrights}" tab is not active')
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in Outright tab')
        sections_names = [section.upper() for section in sections.keys()]
        self.assertTrue(self.event_section_name in sections_names,
                        msg=f'Required section {self.event_section_name} not found in Outright tab in sections {sections_names}')
        self.event_section_name = next((event_section_name for event_section_name in sections if
                                        event_section_name.upper() == self.event_section_name),
                                       None)
        event_section = sections.get(self.event_section_name)
        event_section.expand()
        events = event_section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found in sections of Outright tab')
        events_names = [event.upper() for event in events.keys()]
        self.assertIn(self.event_name, events_names, msg=f'Required {self.event_name} not found in {events_names}')
        self.event_name = next((events_name for events_name in events if events_name.upper() == self.event_name),
                               None)
        event = events.get(self.event_name)
        event.click()
        self.site.wait_content_state('EVENTDETAILS')
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in edp_market_sections.keys()]
        self.assertIn("LUCKY DIP", edp_market_sections_name,
                      msg=f'Expected Lucky Dip market is not displayed in EDP page')
        market_key = next(
            (section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'), None)
        self.__class__.lucky_dip_section = edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()
        self.assertTrue(self.lucky_dip_section.odds.is_displayed(), msg='odds not available')

    def test_003_click_on_the_odds(self):
        """
        DESCRIPTION: Click on the Odds
        EXPECTED: Lucky Dip Animation is displayed, with Lucky Dip Landing page with Below fields
        EXPECTED: ![](index.php?/attachments/get/9d647578-d1ab-4619-a77e-b2f86e07d231)
        """
        self.lucky_dip_section.scroll_to()
        self.lucky_dip_section.odds.click()
        self.assertTrue(self.lucky_dip_section.lucky_dip_QB_splash_container.has_lucky_dip_animation(),
                        msg='Lucky dip animation not displayed')
        self.__class__.quick_bet = self.site.quick_bet_panel.selection
        wait_for_haul(2)
        self.assertTrue(self.quick_bet.content.amount_form.input.is_displayed(), msg='Stake field is not displayed')
        self.assertFalse(self.site.quick_bet_panel.place_bet.is_enabled(expected_result=False),
                         msg='Place bet button enabled')

    def test_004_enter_the_stake_and_click_on_place_bet_cta(self):
        """
        DESCRIPTION: Enter the stake and click on Place bet CTA
        EXPECTED: Player selection card is displayed to the user, with Golfer/Player Name, Odds and Potential returns as below
        EXPECTED: ![](index.php?/attachments/get/79fe23c9-2682-467c-a13e-dfa5e1b621e1)
        """
        self.quick_bet.content.amount_form.input.value = self.bet_amount
        amount = '{:.2f}'.format(float(self.bet_amount))
        self.assertEqual(self.quick_bet.content.amount_form.input.value, amount,
                         msg=f'Actual amount "{self.quick_bet.content.amount_form.input.value}" does not match '
                             f'expected "{amount}"')
        self.assertTrue(self.site.quick_bet_panel.place_bet.is_enabled(), msg='Place bet button is not enabled')
        self.site.quick_bet_panel.place_bet.click()
        luckey_dip_got_it_panel = wait_for_result(lambda: self.site.lucky_dip_got_it_panel.has_lucky_dip_got_it_panel(timeout=5),
                                             timeout=5)
        self.assertTrue(luckey_dip_got_it_panel, msg='Lucky Dip Animation is not displayed to the user')
        lucky_dip_player = self.site.lucky_dip_got_it_panel.lucky_dip_player_name
        self.assertTrue(lucky_dip_player, msg='Lucky Dip player name is not displayed ')
        self.assertTrue(self.site.lucky_dip_got_it_panel.outcome_value, msg='odds value is not displayed')
        self.assertTrue(self.site.lucky_dip_got_it_panel.lucky_dip_potential_returns, msg='Potential returns is not '
                                                                                          'displayed')
        self.assertTrue(self.site.lucky_dip_got_it_panel.lucky_Dip_got_it_button.is_displayed(),
                        msg='Got it button is not displayed')
