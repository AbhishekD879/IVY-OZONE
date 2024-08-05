from collections import OrderedDict
import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest

@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.basketball_specific
@pytest.mark.sports_specific
@pytest.mark.adhoc_suite
@vtest
class Test_C66007942_Verify_the_display_of_data_in_the_Basketball_Outrights_tab(BaseBetSlipTest):
    """
    TR_ID: C66007942
    NAME: Verify the display of data in the Basketball Outrights tab
    DESCRIPTION: This test case validates the data in Basketball Outright's tab.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2.Outrights tab can be configured from CMS-&gt;
    PRECONDITIONS: Sports menu-&gt; Sports category-&gt; Basketball-&gt; Outright's tab-&gt; Enable/Disable.
    PRECONDITIONS: Note: In mobile when no events are available Basketball sport is not displayed in A-Z sports menu and on clicking Basketball from Sports ribbon user is navigated back to the sports homepage.
    """
    home_breadcrumb = 'Home'
    sport_name = 'Basketball'
    keep_browser_open = True

    def get_outrights_selections(self):
        # Create a request class for sports selections
        ss_req_class = self.ss_req.ss_class(
            query_builder=self.ss_query_builder
            .add_filter(
                simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, self.basketball_category_id))
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.IS_ACTIVE))
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, "M"))
            .add_filter(simple_filter(LEVELS.CLASS, ATTRIBUTES.HAS_OPEN_EVENT))
        )

        # Get class IDs based on the applied filters
        class_ids = [class_['class']['id'] for class_ in ss_req_class if
                     class_.get('class') and class_['class'].get('id')]

        # Set additional query parameters for events
        queryParams = (self.ss_query_builder
                       .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.SITE_CHANNELS, OPERATORS.CONTAINS, "M"))
                       .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.EVENT_SORT_CODE, OPERATORS.INTERSECTS,
                                                 'TNMT,TR01,TR02,TR03,TR04,TR05,TR06,TR07,TR08,TR09,TR10,TR11,TR12,TR13,TR14,TR15,TR16,TR17,TR18,TR19,TR20'))
                       .add_filter(
            simple_filter(LEVELS.EVENT, ATTRIBUTES.SUSPEND_AT_TIME, OPERATORS.GREATER_THAN, self.start_date_minus))
                       )

        # Get sports selections for the specified class IDs and query parameters
        events = self.ss_req.ss_event_to_outcome_for_class(class_id=class_ids, query_builder=queryParams)

        # Identify outright selections within the events
        outright_selection = set()
        for event in events:
            for market in event['event']['children']:
                market_info = market['market']
                # Check if the market is an 'Outright' templateMarketName and allows multiple accumulators
                if market_info.get('templateMarketName') == 'Outright' \
                        and \
                        int(market_info.get('maxAccumulators')) > 1:
                    outright_selection.add(market_info['children'][0]['outcome']['id'])

        # Return a list of outright selections
        return list(outright_selection)

    def test_001_launch_the_ladbrokes_and_coral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes and Coral application
        EXPECTED: Home page should loaded successfully
        """
        self.__class__.basketball_category_id = self.ob_config.basketball_config.category_id
        self.site.login()
        self.site.wait_content_state('Homepage')

    def test_002_click_on_basketball_sport(self):
        """
        DESCRIPTION: Click on Basketball sport.
        EXPECTED: User should be able to navigate to the Basketball landing page.
        """
        self.navigate_to_page(name='sport/basketball')
        self.site.wait_content_state(state_name='basketball')

    def test_003_verify_basketball_landing_page(self):
        """
        DESCRIPTION: Verify Basketball landing page.
        EXPECTED: Desktop
        EXPECTED: All the different tabs should be displayed with Matches tab selected by default.
        EXPECTED: In play widget will display if any events are live when it was enabled in System Configuration.
        EXPECTED: Mobile
        EXPECTED: Matches tab loaded as default
        EXPECTED: If in-play module is enabled in CMS it should display in matches tab above to the time and league filters
        """
        # Get the name of the currently selected tab from the basketball section's tabs menu
        current_tab_name = self.site.basketball.tabs_menu.current

        # Perform an assertion to check if the current tab name matches the expected tab name ('MATCHES' in this case)
        # The comparison is case-insensitive to ensure flexibility
        self.assertEqual(current_tab_name.upper(), vec.sb.MATCHES.upper(),
                         msg=f'Default tab is not "{current_tab_name.upper()}", it is "{vec.sb.MATCHES.upper()}"')

    def test_004_verify_outrights_tab(self):
        """
        DESCRIPTION: Verify Outright's tab
        EXPECTED: Accordions should be in collapsed mode by default if data present.
        EXPECTED: Outright tab should not be visble to the user if no data present in it.
        """
        # Get the internal name of the outrights tab based on the sport tabs' internal names and the basketball category ID
        outrights_tab = self.get_sport_tab_name(self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights,
                                                self.basketball_category_id)

        # Check if the current tab is not already set to the "outright" tab; if not, click on the outrights tab
        if self.site.basketball.tabs_menu.current != "outright":
            self.site.basketball.tabs_menu.click_button(button_name=outrights_tab)

        # Get the name of the currently selected tab after the potential click
        current_tab = self.site.basketball.tabs_menu.current

        # Perform an assertion to check if the current tab matches the expected outrights_tab
        self.assertEqual(current_tab, outrights_tab,
                         msg=f'Default tab: "{current_tab}" opened is not as expected: "{outrights_tab}"')

        # Get a dictionary of sections within the basketball tab content, ordered by appearance
        sections = self.site.basketball.tab_content.accordions_list.items_as_ordered_dict

        # Ensure that there are sections present in the basketball tab content
        self.assertTrue(sections, msg='No sections found')

        # Iterate through each section, scroll to it, and check if it is expanded (should not be expanded)
        for section_name, section in list(sections.items()):
            # Scroll to the section to make it visible
            section.scroll_to()

            # Perform an assertion to check if the section is not expanded within a given timeout
            self.assertFalse(section.is_expanded(expected_result=False, timeout=3),
                             msg=f'Section "{section_name}" is expanded')

    def test_005_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordions are collapsable and expandable
        EXPECTED: Accordion's should be collapsable and expandable
        """
        # Get a list of accordions within the basketball tab content as an ordered dictionary
        accordions = list(self.site.basketball.tab_content.accordions_list.items_as_ordered_dict.items())

        # Ensure that there are accordions present on the page
        self.assertTrue(accordions, msg='No accordions found on page')

        # Iterate through each accordion in the list
        for accordion_name, accordion in accordions:
            # Check if the accordion is not already expanded
            if not accordion.is_expanded():
                # Expand the accordion
                accordion.expand()

                # Perform an assertion to check if the accordion is expanded after the expansion operation
                self.assertTrue(accordion.is_expanded(),
                                msg=f'Accordion {accordion_name} is not expanded after expansion')

    def test_006_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should be navigated on the respective page on click
        """

        accordion = list(self.site.basketball.tab_content.accordions_list.items_as_ordered_dict.values())[0]
        event_name,event = list(accordion.items_as_ordered_dict.items())[0]
        event.click()
        self.site.wait_content_state(state_name="EVENTDETAILS")
        if self.device_type == 'desktop':
            page = self.site.sports_page
            breadcrumbs = OrderedDict((key.strip(), page.breadcrumbs.items_as_ordered_dict[key])
                                      for key in page.breadcrumbs.items_as_ordered_dict)

            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

            self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                             msg='Home page is not shown the first by default')
            self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index(self.sport_name), 1,
                             msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
            self.assertTrue(breadcrumbs[self.sport_name].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index(event_name), 2,
                             msg=f'"{event_name} " item name is not shown after "{self.sport_name}"')
            self.assertTrue(
                int(breadcrumbs[event_name].link.css_property_value('font-weight')) == 700,
                msg=f'" matches " hyperlink from breadcrumbs is not highlighted according to the selected page')

    def test_007_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be naviagted to homepage
        EXPECTED: Mobile
        EXPECTED: User should be naviagted to sport navigation page
        """
        self.site.back_button.click()

    def test_008_verify_by_expanding_the_accordion_and_click_on_events(self):
        """
        DESCRIPTION: Verify by expanding the accordion and click on events.
        EXPECTED: User should be navigated to respective page.
        """
        # Covered in above steps


    def test_009_verify_bet_placements_for_single_multiple_complex(self):
        """
        DESCRIPTION: Verify bet placements for Single, Multiple, Complex
        EXPECTED: Bet placements needs to be successful
        """
        outright_selections = self.get_outrights_selections()
        if len(outright_selections) >= 1:
            # Single Bet
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=outright_selections[0])
            self.place_single_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()

        if len(outright_selections) > 1:
            # Multiple bet
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=outright_selections[0:2])
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()

        if len(outright_selections) > 2:
            # Complex bet
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=outright_selections[0:3])
            self.place_multiple_bet(number_of_stakes=3)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()