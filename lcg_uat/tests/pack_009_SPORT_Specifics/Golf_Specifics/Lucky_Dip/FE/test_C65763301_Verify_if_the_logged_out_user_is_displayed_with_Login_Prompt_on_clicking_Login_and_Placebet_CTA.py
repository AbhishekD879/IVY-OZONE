import pytest
from tests.base_test import vtest
import voltron.environments.constants as vec
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.waiters import wait_for_haul


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@vtest
class Test_C65763301_Verify_if_the_logged_out_user_is_displayed_with_Login_Prompt_on_clicking_Login_and_Placebet_CTA(BaseGolfTest):
    """
    TR_ID: C65763301
    NAME: Verify if the logged out user is displayed with Login Prompt on clicking 'Login and Placebet' CTA
    DESCRIPTION: This testcase verifies the display of Login Prompt on clicking 'Login and Placebet' CTA for a logged out user.
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Lucky Dip should be configured in CMS
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        cms_config_lucky_dip = self.cms_config.get_system_configuration_structure()['LuckyDip']['enabled']
        if not cms_config_lucky_dip:
            raise CmsClientException(f'Lucky Dip is not Enabled in CMS')
        event = self.get_active_lucky_dip_events(number_of_events=1, all_available_events=True)[0]['event']
        self.__class__.sport_name = event['categoryCode'].upper()
        self.__class__.event_name = event['name'].upper()
        self.__class__.event_section_name = event['className'].upper() + " - " + event['typeName'].upper()

    def test_001_launch_ladbrokes_application_and_navigate_to_golf_from_a_z_sports(self):
        """
        DESCRIPTION: Launch Ladbrokes application and Navigate to Golf from A-Z sports
        EXPECTED: User is navigated to Golf Landing Page
        """
        self.site.wait_content_state('Home')
        self.site.open_sport(name=vec.SB.ALL_SPORTS)
        self.site.all_sports.a_z_sports_section.click_item(item_name=self.sport_name)

    def test_002_click_on_the_eventcompetition_in_which_lucky_dip_market_is_configured_and_click_on_the_odds_displayed_against_lucky_dip_market(self):
        """
        DESCRIPTION: Click on the event/Competition in which Lucky Dip Market is configured and click on the Odds displayed against Lucky Dip market
        EXPECTED: User is able to select the odds
        EXPECTED: User is displayed with Lucky dip Animation and
        EXPECTED: Luckydip Landing page  is displayed to the user
        """
        # Navigation To Outright/Golf
        expected_sport_tab = self.get_sport_tab_name(name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,
                                                     category_id=self.ob_config.golf_config.category_id)
        self.site.golf.tabs_menu.click_button(expected_sport_tab)
        self.assertEqual(self.site.golf.tabs_menu.current, expected_sport_tab,
                         msg=f'"{expected_sport_tab}" tab is not active')

        # Clicking on Type(example:The Honda Classic)
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
        # Opening Event
        events = event_section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found in sections of Outright tab')
        events_names = [event.upper() for event in events.keys()]
        self.assertIn(self.event_name, events_names, msg=f'Required {self.event_name} not found in {events_names}')
        self.event_name = next((events_name for events_name in events if events_name.upper() == self.event_name),
                               None)
        event = events.get(self.event_name)
        event.click()
        self.site.wait_content_state('EVENTDETAILS')
        # reading and verifying the markets present in EDP
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in edp_market_sections.keys()]
        self.assertIn("LUCKY DIP", edp_market_sections_name,
                      msg=f'Expected Lucky Dip market is not displayed in EDP page')
        market_key = next(
            (section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'), None)
        self.__class__.lucky_dip_section = edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()
        self.assertTrue(self.lucky_dip_section.odds.is_displayed(), msg='odds not available')
        self.lucky_dip_section.odds.click()

    def test_003_enter_the_required_amount_as_stake_and_click_on_login_and_placebet_cta(self):
        """
        DESCRIPTION: Enter the required amount as stake and click on Login and Placebet CTA
        EXPECTED: User should be displayed with the Login Prompt
        """
        # adding stake in betslip and verifying the added stake
        quick_bet = self.site.quick_bet_panel.selection
        wait_for_haul(5)
        quick_bet.content.amount_form.input.value = self.bet_amount
        bet_amount_string='{:.2f}'.format(float(self.bet_amount))
        betslip_stake = '{:.2f}'.format(float(quick_bet.content.amount_form.input.value))
        self.assertEqual(betslip_stake, bet_amount_string,
                         msg=f'Actual amount "{betslip_stake}" does not match '
                             f'expected "{bet_amount_string}"')
        # verifying if Login button is enabled after adding stake and login Prompt is coming after clicking Login and Placebet CTA
        bet_button_names = vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET
        betnow_btn = self.site.quick_bet_panel.place_bet
        self.assertTrue(betnow_btn.is_enabled(timeout=2), msg='Bet Now button is not enabled')
        if isinstance(bet_button_names, (list, tuple)):
            self.assertTrue(any(True for bet_button_name in bet_button_names if betnow_btn.name == bet_button_name),
                            msg=f'Button text "{betnow_btn.name}" does not match any of expected "{bet_button_names}"')
        else:
            self.assertEqual(betnow_btn.name, bet_button_names,
                             msg=f'Button text "{betnow_btn.name}" does not match expected "{bet_button_names}"')
        betnow_btn.click()
        self.__class__.dialog = self.site.wait_for_dialog(vec.dialogs.DIALOG_MANAGER_LOG_IN)
        self.assertTrue(self.dialog, msg=f'"{vec.dialogs.DIALOG_MANAGER_LOG_IN}" dialog is not displayed')
