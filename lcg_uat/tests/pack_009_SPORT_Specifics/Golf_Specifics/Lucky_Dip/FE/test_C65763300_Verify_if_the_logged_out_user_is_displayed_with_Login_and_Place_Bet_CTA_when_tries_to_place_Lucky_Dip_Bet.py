import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.quick_bet
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@vtest
class Test_C65763300_Verify_if_the_logged_out_user_is_displayed_with_Login_and_Place_Bet_CTA_when_tries_to_place_Lucky_Dip_Bet(BaseGolfTest):
    """
    TR_ID: C65763300
    NAME: Verify if the logged out user is displayed with Login and Place Bet CTA when tries to place Lucky Dip Bet
    DESCRIPTION: This testcase verifies the display of 'Login and Place Bet' CTA when user tries to place Lucky Dip Bet
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
        """
        # Check if Lucky Dip is enabled in CMS
        cms_config_lucky_dip = self.cms_config.get_system_configuration_item('LuckyDip')
        if len(cms_config_lucky_dip) == 0 or not cms_config_lucky_dip.get('enabled'):
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')

        # Check if Lucky Dip is enabled in OB
        lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        event = lucky_dip_events[0]['event']
        self.__class__.sport_name = event['categoryCode'].upper()
        self.__class__.lucky_dip_eventID = event['id']
        self.__class__.event_name = event['name'].upper()
        self.__class__.event_section_name = event['className'].upper() + " - " + event['typeName'].upper()
        self.assertTrue(self.lucky_dip_eventID, msg="Lucky Dip Event Not Available")

    def test_001_launch_ladbrokes_application_and_navigate_to_golf_from_a_z_sports(self):
        """
        DESCRIPTION: Launch Ladbrokes application and Navigate to Golf from A-Z sports
        EXPECTED: User is navigated to Golf Landing Page
        """
        # Navigate to Golf from A-Z Sport page
        if self.device_type == 'mobile':
            # Mobile specific
            self.site.open_sport(name=vec.SB.ALL_SPORTS)
            self.site.all_sports.click_item(item_name=self.sport_name)
        else:
            # Desktop specific
            self.site.sport_menu.sport_menu_items_group("AZ").click_item(item_name=self.sport_name)
            self.site.wait_content_state(state_name=self.sport_name)

    def test_002_click_on_the_eventcompetition_in_which_lucky_dip_market_is_configured_and_click_on_the_odds_displayed_against_lucky_dip_market(self):
        """
        DESCRIPTION: Click on the event/Competition in which Lucky Dip Market is configured and click on the Odds displayed against Lucky Dip market
        EXPECTED: User is able to select the odds
        EXPECTED: User is displayed with Lucky dip Animation and
        EXPECTED: Luckydip Landing page is displayed to the user
        """
        # Navigate to the event/Competition in which Lucky Dip Market is configured

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

        # Check If Lucky Dip Market is available
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in edp_market_sections.keys()]
        self.assertIn("LUCKY DIP", edp_market_sections_name,
                      msg=f'Expected Lucky Dip market is not displayed in EDP page')

        # Navigating To Lucky Dip Selection
        market_key = next((section_name for section_name in edp_market_sections if section_name.upper() == 'LUCKY DIP'),
                          None)
        self.__class__.lucky_dip_section = edp_market_sections.get(market_key)
        self.lucky_dip_section.scroll_to()

        # Verify Odds are displayed For Lucky Dip Market
        self.assertTrue(self.lucky_dip_section.odds, f"Odds are not displayed beside the Market")
        self.lucky_dip_section.odds.click()

        # Verify Lucky Dip Animation is displayed
        self.assertTrue(self.lucky_dip_section.lucky_dip_QB_splash_container.has_lucky_dip_animation(), f"Lucky Dip animation is not displayed")

    def test_003_verify_the_display_of_login_and_place_bet_cta_in_lucky_dip_landing_page(self):
        """
        DESCRIPTION: Verify the display of 'Login and Place bet' CTA in Lucky Dip Landing page
        EXPECTED: Login and Place bet CTA should be displayed to the user
        """
        # Verify the display of 'Login and Place bet Button'
        quick_bet = self.site.quick_bet_panel
        self.site.wait_content_state_changed()
        self.assertEqual(quick_bet.place_bet.name, vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET,
                         msg=f'Found "{quick_bet.place_bet.name}" button name, expected "{vec.betslip.LOGIN_AND_PLACE_BET_QUICK_BET}"')
