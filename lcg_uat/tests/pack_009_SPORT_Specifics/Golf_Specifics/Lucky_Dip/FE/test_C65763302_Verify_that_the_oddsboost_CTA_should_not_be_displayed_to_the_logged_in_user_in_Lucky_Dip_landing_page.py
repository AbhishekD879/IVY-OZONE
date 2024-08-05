import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from voltron.utils.exceptions.cms_client_exception import CmsClientException


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.mobile_only
@pytest.mark.lucky_dip
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C65763302_Verify_that_the_oddsboost_CTA_should_not_be_displayed_to_the_logged_in_user_in_Lucky_Dip_landing_page(BaseSportTest, BaseGolfTest):
    """
    TR_ID: C65763302
    NAME: Verify that the oddsboost CTA should not be displayed to the logged in user in  Lucky Dip landing page.
    DESCRIPTION: This testcase verifies that the Oddsboost CTA should not be displayed to the logged in user in Lucky Dip Landing page
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Loggedin user should have active Oddsboost token
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        odds_boost = self.cms_config.get_initial_data(cached=True).get('oddsBoost', {})
        if not odds_boost.get('enabled'):
            raise CmsClientException('Odds Boost is disabled in CMS')
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
        username = tests.settings.odds_boost_user
        self.site.login(username=username)

    def test_002_navigate_to_golf_from_a_z_menu(self):
        """
        DESCRIPTION: Navigate to Golf from A-Z menu
        EXPECTED: User is navigated to Golf Landing page
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

    def test_003_click_on_the_event_competition_in_which_lucky_dip_market_is_configured_from_outright_tab(self):
        """
        DESCRIPTION: Click on the event/Competition in which Lucky Dip Market is configured from Outright tab
        EXPECTED: User is Navigated to the respective EDP page and Lucky Dip market with Odds is displayed
        """
        self.site.golf.tabs_menu.click_button(self.expected_sport_tabs.outrights)
        self.assertEqual(self.site.golf.tabs_menu.current, self.expected_sport_tabs.outrights,
                         msg=f'"{self.expected_sport_tabs.outrights}" tab is not active')
        sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(sections, msg='No sections found in Outright tab')
        sections_names=[section.upper() for section in sections.keys()]
        self.assertTrue(self.event_section_name in sections_names,
                        msg=f'Required section {self.event_section_name} not found in Outright tab in sections {sections_names}')
        self.event_section_name = next((event_section_name for event_section_name in sections if event_section_name.upper() == self.event_section_name),
                               None)
        event_section = sections.get(self.event_section_name)
        event_section.expand()
        events = event_section.items_as_ordered_dict
        self.assertTrue(events, msg='No events found in sections of Outright tab')
        events_names = [event.upper() for event in events.keys()]
        self.assertIn(self.event_name, events_names, msg=f'Required {self.event_name} not found in {events_names}')
        self.event_name=next((events_name for events_name in events if events_name.upper() == self.event_name),
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

    def test_004_click_on_the_odds(self):
        """
        DESCRIPTION: Click on the ODDS
        EXPECTED: User is able to select the odds
        EXPECTED: User is displayed with Lucky dip Animation and
        EXPECTED: Lucky dip Landing page is displayed to the user
        """
        self.lucky_dip_section.scroll_to()
        self.lucky_dip_section.odds.click()
        self.assertTrue(self.site.lucky_dip_got_it_panel.lucky_dip_QB_splash_container.has_lucky_dip_animation(),
                        msg='Lucky dip animation not displayed')

    def test_005_verify_the_display_of_odds_boost_cta_above_the_selection_in_lucky_dip_landing_page(self):
        """
        DESCRIPTION: Verify the display of Odds boost CTA above the selection in lucky dip landing page
        EXPECTED: Odds boost cta should not be displayed to the user
        """
        self.assertFalse(self.site.quick_bet_panel.has_odds_boost_button(expected_result=False),
                         msg=f'"{vec.odds_boost.BOOST_BUTTON.disabled}" button is shown after clicking odds')