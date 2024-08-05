from collections import OrderedDict
import pytest
from crlat_cms_client.utils.exceptions import CMSException
import tests
from tests.base_test import vtest
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.quick_bet
@pytest.mark.desktop
# @pytest.mark.desktop_only
@pytest.mark.lucky_dip
@vtest
class Test_C65842686_Verify_that_lucky_dip_market_should_not_be_displayed_in_desktop_when_user_navigates_from_matches_tabSee_all_link(BaseGolfTest):
    """
    TR_ID: C65842686
    NAME: Verify that lucky dip market should not be displayed  in desktop when user navigates from matches tab>See all link
    DESCRIPTION: This test case verifies that lucky dip market should not be displayed  in desktop when user navigates from matches tab&gt;See all link
    PRECONDITIONS: 
    """
    keep_browser_open = True
    device_name = tests.desktop_default

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Lucky Dip should be configured in CMS or not
        """
        # Retrieve active lucky dip events
        event_sport_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                    self.ob_config.golf_config.category_id)
        is_tab_enabled = self.cms_config.get_sport_tab_status(
                    tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                    sport_id=self.ob_config.golf_config.category_id)
        if(not is_tab_enabled):
            raise CMSException(f' "{event_sport_tab}" tab is not enabled in CMS')
        all_lucky_dip_events = self.get_active_lucky_dip_events(all_available_events=True)
        event = all_lucky_dip_events[0]
        self.__class__.eventName = event['event']['name'].upper()
        self.__class__.ob_event_section_name = (event['event']['className'] + ' - ' + event['event']['typeName']).upper()

    def test_001_launch_ladbrokes_application_in_desktop(self):
        """
        DESCRIPTION: Launch Ladbrokes application in desktop
        EXPECTED: User should be able to launch application in desktop
        """
        self.site.wait_content_state('Homepage')

    def test_002_navigate_to_golf_pageampgtevents_tab(self):
        """
        DESCRIPTION: Navigate to Golf page&amp;gt;Events Tab
        EXPECTED: User should be navigated to event tab
        """
        self.navigate_to_page(name='sport/golf')
        event_sport_tab = \
            self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches,
                                    self.ob_config.golf_config.category_id)
        current_sport_tab = self.site.golf.tabs_menu.current
        golf_slp_tabs = self.site.golf.tabs_menu.items_as_ordered_dict
        self.assertIn(event_sport_tab, golf_slp_tabs, f'expected tab: "{event_sport_tab}" is not found in "{golf_slp_tabs}"')
        if event_sport_tab != current_sport_tab:
            golf_slp_tabs(event_sport_tab).click()
        sub_tabs = self.site.golf.date_tab.items_as_ordered_dict
        for tab in sub_tabs:
            sub_tabs[tab].click()
            if self.site.sports_page.tab_content.has_no_events_label(expected_result=True):
                continue
            self.__class__.event_sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            sections = OrderedDict()
            for section_name, section in self.__class__.event_sections.items():
                sections.update({section_name.replace("\nSEE ALL", ""): section})
            self.__class__.event_sections = sections
            self.__class__.event_section_name = next((event_section_name for event_section_name in self.event_sections if self.ob_event_section_name == event_section_name.upper()), None)
            if self.event_section_name != None:
                break
        self.assertIsNotNone(self.event_section_name, f'expected section "{self.ob_event_section_name}" is not available in all sub tabs')

    def test_003_navigate_to_the_type_for_which_lucky_dip_market_is_configured_and_click_on_see_all_link(self):
        """
        DESCRIPTION: Navigate to the type for which lucky dip market is configured and click on see all link
        EXPECTED: User should be navigated to the type for which lucky dip market is configured
        """
        self.event_sections[self.event_section_name].group_header.see_all_link.click()
        league_tabs = self.site.competition_league.tabs_menu.items_as_ordered_dict
        expected_league_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,self.ob_config.golf_config.category_id)
        outright_tab = next((league_tabs[tab] for tab in league_tabs if tab.upper() == expected_league_tab.upper()), None)
        self.assertIsNotNone(outright_tab, f'expected tab : "{expected_league_tab}" not in "{list(league_tabs.keys())}"')
        outright_tab.click()
        self.assertEqual(self.site.competition_league.tabs_menu.current.upper(), expected_league_tab.upper(), f'Outright tab is not active')
        self.__class__.has_event_title = self.site.competition_league.tab_content.has_co_header_title
        if self.has_event_title:
            self.__class__.markets_names = self.site.competition_league.tab_content.accordions_list.items_as_ordered_dict
        else:
            outrights_events = self.site.competition_league.tab_content.accordions_list_for_competitions.items_as_ordered_dict
            event_names = [event_name.upper() for event_name in outrights_events]
            self.assertIn(self.eventName, event_names, f'event name "{self.eventName}" 'f'is not found in outrights tab events : {event_names}')
            self.eventName = next((event_name for event_name in outrights_events if self.eventName == event_name.upper()), None)
            self.__class__.event = outrights_events.get(self.eventName)

    def test_004_navigate_to_the_edp_of_event_for_which_lucky_dip_market_is_configured_and_check_if_the_lucky_dip_market_is_displayed(self):
        """
        DESCRIPTION: Navigate to the EDP of event for which lucky dip market is configured and check if the lucky dip market is displayed
        EXPECTED: Lucky dip market should not be displayed in EDP page of Golf in desktop
        """
        if self.has_event_title:
            market_names = self.markets_names
        else:
            self.event.expand()
            market_names = self.event.competitions_market_headers_text
        market_names = list(market_name.upper() for market_name in market_names)
        self.assertNotIn("LUCKY DIP", market_names, msg=f'LUCKY DIP is available in desktop')
