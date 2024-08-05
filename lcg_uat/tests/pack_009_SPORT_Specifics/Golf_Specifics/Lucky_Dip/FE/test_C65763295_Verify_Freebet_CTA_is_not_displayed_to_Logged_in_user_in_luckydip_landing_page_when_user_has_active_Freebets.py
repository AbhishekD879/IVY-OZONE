import pytest
import tests
import voltron.environments.constants.base.sportsbook as vec
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
class Test_C65763295_Verify_Freebet_CTA_is_not_displayed_to_Logged_in_user_in_luckydip_landing_page_when_user_has_active_Freebets(BaseGolfTest):
    """
    TR_ID: C65763295
    NAME: Verify  Freebet  CTA is not displayed to Logged in user in luckydip landing page, when user has active Freebets
    DESCRIPTION: This testcase verifies the display od Add Freebet CTA for a logged in user in Lucky Dip Landing page, When user has active Freebets
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
    PRECONDITIONS: Logged in user should have Active freebets applicable for Golf
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only for Golf sport
        PRECONDITIONS: Logged in user should have Active freebets applicable for Golf
        """
        # Check if Lucky Dip is enabled in CMS
        cms_config_lucky_dip = self.cms_config.get_system_configuration_item('LuckyDip')
        if len(cms_config_lucky_dip) == 0 or not cms_config_lucky_dip.get('enabled'):
            raise CmsClientException(f'::::: Lucky Dip is Not Enabled in CMS ::::')

        # Check if Lucky Dip is enabled in OB
        lucky_dip_events = self.get_active_lucky_dip_events()
        event = lucky_dip_events[0]['event']
        self.__class__.lucky_dip_eventID = event['id']
        self.__class__.event_name = event['name'].upper()
        self.__class__.event_section_name = event['className'].upper() + " - " + event['typeName'].upper()
        self.assertTrue(self.lucky_dip_eventID, msg="Lucky Dip Event Not Avaiable")

        # Picking FreeBet User
        if tests.settings.backend_env != "prod":
            # only Applicable for non prod environments
            self.__class__.username = tests.settings.freebet_user
            self.ob_config.grant_freebet(username=self.username)
        else:
            self.__class__.username = tests.settings.freebet_user

    def test_001_login_to_ladbrokes_application(self):
        """
        DESCRIPTION: Login to Ladbrokes application
        EXPECTED: User logs in successfully
        """
        # Login to Ladbrokes application
        self.site.login(username=self.username)
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')
        self.site.wait_content_state(state_name="Homepage")

        # Verifying Freebet is Available for Logged In users
        self.navigate_to_page("freebets")
        self.assertNotEquals(first=self.site.freebets.balance.total_balance, second=0, msg='Logged in user does not have Freebet')

        # Navigate Back to Home page
        self.navigate_to_page("homepage")
        self.site.wait_content_state(state_name="Homepage")

    def test_002_navigate_to_golf_from_a_z_landing_page(self):
        """
        DESCRIPTION: Navigate to Golf from A-Z Landing page
        EXPECTED: User is navigated to Golf Landing Page
        """
        # Navigate to Golf from A-Z Sport page
        if self.device_type == 'mobile':
            # Mobile specific
            self.site.open_sport(name=vec.SB.ALL_SPORTS)
            self.site.all_sports.click_item(item_name=vec.SB.GOLF)
        else:
            # Desktop specific
            self.site.sport_menu.sport_menu_items_group("AZ").click_item(item_name=vec.SB.GOLF)
            self.site.wait_content_state(state_name=vec.SB.GOLF)

    def test_003_click_on_the_eventcompetition_in_which_lucky_dip_market_is_configured(self):
        """
        DESCRIPTION: Click on the event/Competition in which Lucky Dip Market is configured
        EXPECTED: User is Navigated to the respective EDP page and Lucky Dip market with Odds is displayed
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

    def test_004_click_on_the_odds(self):
        """
        DESCRIPTION: Click on the ODDS
        EXPECTED: User is able to select the odds
        EXPECTED: User is displayed with Lucky dip Animation and Luckydip Landing page is displayed to the user as below
        EXPECTED: ![](index.php?/attachments/get/5e0c9404-00bf-4e6f-9517-672584f6d477)
        """
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

    def test_005_verify_the_display_od_add_freebet_cta_below_the_stake_field_in_the_lucky_dip_landing_page(self):
        """
        DESCRIPTION: Verify the display od Add Freebet CTA below the stake field in the lucky dip landing page
        EXPECTED: Add Freebet CTA shouldn't be displayed to the user in Lucky Dip Landing page
        """
        # Verify Add Freebet CTA is not displayed
        has_freebet = self.site.quick_bet_panel.selection.quick_stakes.has_use_free_bet_link(expected_result=False)
        self.assertFalse(has_freebet,
                         msg=f'Add Freebet CTA is displayed to the user in Lucky Dip Landing page')
