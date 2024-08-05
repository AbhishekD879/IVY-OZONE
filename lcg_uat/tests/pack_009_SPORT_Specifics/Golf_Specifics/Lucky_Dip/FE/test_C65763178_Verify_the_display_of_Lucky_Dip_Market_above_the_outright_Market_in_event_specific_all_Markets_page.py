import pytest
import voltron.environments.constants as vec
from tests.pack_009_SPORT_Specifics.Golf_Specifics.BaseGolfTest import BaseGolfTest
from tests.base_test import vtest
from voltron.utils.exceptions.cms_client_exception import CmsClientException

@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
@pytest.mark.high
@pytest.mark.sports
@pytest.mark.lucky_dip
@pytest.mark.mobile_only
@vtest
class Test_C65763178_Verify_the_display_of_Lucky_Dip_Market_above_the_outright_Market_in_event_specific_all_Markets_page(BaseGolfTest):
    """
    TR_ID: C65763178
    NAME: Verify the display of Lucky Dip Market, above the outright Market in event specific all Markets page
    DESCRIPTION: This testcase verifies the display of Lucky Dip Market, above the Outright Market in even specific all Markets page
    PRECONDITIONS: Lucky Dip should be configured as new market in OB in market template win Only
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
        self.__class__.eventID = event['id']

    def test_001_launch_ladbrokes_application(self):
        """
        DESCRIPTION: Launch Ladbrokes application
        EXPECTED: User is in Home page of the application
        """
        self.site.login()

    def test_002_navigate_to_golf_from_a_z_landing_page(self):
        """
        DESCRIPTION: Navigate to Golf from A-Z Landing page
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

    def test_003_click_on_the_eventcompetition_in_which_lucky_dip_market_is_configured(self):
        """
        DESCRIPTION: Click on the event/Competition in which Lucky Dip Market is configured
        EXPECTED: User is navigated to the Event detail page of the specific event/Competition.
        EXPECTED: ALL Markets are displayed to the user under ALL Markets tab
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

    def test_004_verify_the_lucky_dip_market_above_the_outright_market_in_all_markets(self):
        """
        DESCRIPTION: Verify the Lucky Dip Market above the Outright Market in All Markets
        EXPECTED: Lucky Dip market should be displayed above the Outright Market.
        EXPECTED: ![](index.php?/attachments/get/fce75614-dcd2-4104-85d9-c34c0e0bed2a)
        """
        edp_market_sections = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        edp_market_sections_name = [market.upper() for market in edp_market_sections.keys()]
        self.assertIn("LUCKY DIP", edp_market_sections_name, msg=f'Expected Lucky Dip market is not displayed in EDP page')
        self.assertIn("OUTRIGHT", edp_market_sections_name, msg=f'outright market is not available in EDP page')
        luckydip_index_position = edp_market_sections_name.index("LUCKY DIP")
        outright_index_position = edp_market_sections_name.index("OUTRIGHT")
        self.assertEqual(luckydip_index_position, outright_index_position-1, msg=f'Lucky Dip Market is not present above the Outright Market in All Markets')