from collections import OrderedDict
import pytest
from tests.base_test import vtest
import voltron.environments.constants as vec
from crlat_siteserve_client.siteserve_client import simple_filter
from crlat_siteserve_client.constants import LEVELS
from crlat_siteserve_client.constants import OPERATORS
from crlat_siteserve_client.constants import ATTRIBUTES
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_response_url, do_request
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.sports_specific
@pytest.mark.snooker_specific
@pytest.mark.adhoc_suite
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.timeout(900)
@vtest
class Test_C66007986_Validate_the_data_displayed_in_the_Snooker_Outrights_tab(BaseBetSlipTest):
    """
    TR_ID: C66007986
    NAME: Validate the data displayed in the Snooker Outright's tab.
    DESCRIPTION: This test case needs to verify Outrights tab display for the Snooker sport.
    PRECONDITIONS: 1.User should have access to oxygen CMS
    PRECONDITIONS: URL: https://cms-api-ui-hlv0.coralsports.nonprod.cloud.ladbrokescoral.com/
    PRECONDITIONS: 2.Outrights tab can be configured from CMS-&gt;
    PRECONDITIONS: Sports menu -&gt; Sports category -&gt; Snooker -&gt; Outrights tab -&gt; Enable/Disable.
    PRECONDITIONS: Note: In mobile when no events are available Snooker sport is not displayed in A-Z sports menu and on clicking Snooker  from Sports ribbon user is navigated back to the sports homepage.
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    default_date_tab = vec.sb.SPORT_DAY_TABS.today
    home_breadcrumb = vec.sb.HOME_FOOTER_ITEM.upper()
    highlight_tab = vec.sb.TABS_NAME_OUTRIGHTS.upper()

    def get_sport_tab_name(self, name: str, category_id: int):
        tabs_data = self.cms_config.get_sport_config(category_id=category_id).get('tabs')
        sport_tab = next((tab for tab in tabs_data if tab.get('name') == name), '')
        sport_tab_name = sport_tab.get('label').upper()
        return sport_tab_name

    def get_outrights_selections(self):
        category_id = self.ob_config.backend.ti.snooker.category_id
        # Create a request class for sports selections
        ss_req_class = self.ss_req.ss_class(
            query_builder=self.ss_query_builder
            .add_filter(
                simple_filter(LEVELS.CLASS, ATTRIBUTES.CATEGORY_ID, OPERATORS.EQUALS, category_id))
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
                if market_info.get('templateMarketName') == 'Outright' and int(market_info.get('maxAccumulators')) > 1:
                    outright_selection.add(market_info['children'][0]['outcome']['id'])

        # Return a list of outright selections
        return list(outright_selection)

    def test_000_preconditions(self):
        """
        PRECONDITIONS: Load the app
        PRECONDITIONS: Go to the Snooker Landing Page -> 'Click on Matches Tab'
        """
        category_id = self.ob_config.backend.ti.snooker.category_id
        self.__class__.sport_name = self.get_sport_title(category_id)
        self.__class__.status = self.cms_config.get_sport_tab_status(
            tab_name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, sport_id=category_id)
        self.__class__.expected_tab_name = self.get_sport_tab_name(
            name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.outrights, category_id=category_id)
        self.__class__.matches_tab_name = self.get_sport_tab_name(
            name=self.cms_config.constants.SPORT_TABS_INTERNAL_NAMES.matches, category_id=category_id)

    def test_001_launch_the_ladbrokescoral_application(self):
        """
        DESCRIPTION: Launch the Ladbrokes/Coral application
        EXPECTED: Home page should loaded successfully
        """
        self.site.login()

    def test_002_click_on_the_snooker_sport(self):
        """
        DESCRIPTION: Click on the Snooker sport.
        EXPECTED: User should be able to navigate to the Snooker landing page.
        """
        self.site.open_sport(self.sport_name, content_state='Snooker')

    def test_003_verify_snooker_landing_page(self):
        """
        DESCRIPTION: Verify Snooker landing page.
        EXPECTED: Desktop
        EXPECTED: Tabs should be displayed with defualt selected matches tab with  today events.
        EXPECTED: In play widget will display if any events are in live when it was enabled in sys config.
        EXPECTED: Mobile
        EXPECTED: Matches module loaded as default with inplay events in it
        """
        current_tab_on_sport_slp = self.site.sports_page.tabs_menu.current
        if self.device_type == 'mobile' and not self.status and current_tab_on_sport_slp != self.matches_tab_name.upper():
            self.assertEqual(current_tab_on_sport_slp.upper(), self.matches_tab_name.upper(),
                             msg=f"Current Active tab is {current_tab_on_sport_slp},"
                                 f"Expected tab is Matches")

    def test_004_verify_outrights_tab(self):
        """
        DESCRIPTION: Verify Outright's tab
        EXPECTED: Accordions should be in collapsed mode by default if data present.
        EXPECTED: Outright tab should not be visble to the user if no data present in it .
        """
        tabs = self.site.contents.tabs_menu.items_as_ordered_dict
        if not self.status and self.expected_tab_name not in tabs:
            raise SiteServeException("events  are not present in outright tab of Snooker")
        tabs.get(self.expected_tab_name).click()
        self.site.wait_content_state_changed()
        current_tab_name = self.site.contents.tabs_menu.current
        self.assertEqual(current_tab_name.upper(), self.expected_tab_name.upper(),
                         msg=f'Actual tab is "{current_tab_name}", instead of "{self.expected_tab_name.upper()}"')
        self.__class__.actual_url = get_response_url(self, url='/EventToOutcomeForClass')
        # If the URL is not available, refresh the page and try again
        if not self.actual_url:
            self.device.refresh_page()
            self.__class__.actual_url = get_response_url(self, url='/EventToOutcomeForClass')
        response = do_request(method='GET', url=self.actual_url)
        self.__class__.event_type_name = {}
        self.__class__.event_time = {}
        for event in response['SSResponse']['children']:
            if not event.get('event'):
                break
            type_name = f"{event['event']['categoryName']} - {event['event']['typeName'].encode('utf-8').decode('unicode-escape')}".strip().upper()
            event_name = event['event']['name'].strip().upper()
            self.__class__.event_type_name[event_name] = type_name

    def test_005_verify_accordions_are_collapsable_and_expandable(self):
        """
        DESCRIPTION: Verify accordions are collapsable and expandable
        EXPECTED: Accordions should be collapsable and expandable
        """
        if len(self.event_type_name):
            sections = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            for section_name, section in sections.items():
                expanded = section.is_expanded()
                if expanded:
                    section.collapse()
                    self.assertFalse(section.is_expanded(expected_result=False),
                                     msg=f"accordion with section name {section_name} is still expanded even after clicking")
                else:
                    section.expand()
                    self.assertTrue(section.is_expanded(),
                                    msg=f"accordion with section name {section_name} is not expanded even after clicking")
                    section.collapse()
                self.assertTrue(section_name.split('\n')[0].upper() in self.event_type_name.values(),
                                msg=f"according with {section_name} is not present in {self.event_type_name.values()}")
        else:
            self.assertTrue(self.site.sports_page.tab_content.has_no_events_label(),
                            msg="No events message is not displayed even when there are no events available")

    def test_006_verify_breadcrumbs(self):
        """
        DESCRIPTION: Verify Breadcrumbs
        EXPECTED: Desktop
        EXPECTED: User should navigate to the respective page on click
        """
        if self.device_type != 'mobile':
            page = self.site.sports_page
            breadcrumbs = OrderedDict((key.strip().upper(), page.breadcrumbs.items_as_ordered_dict[key])
                                      for key in page.breadcrumbs.items_as_ordered_dict)

            self.assertTrue(breadcrumbs, msg='No breadcrumbs found')

            self.assertEqual(list(breadcrumbs.keys()).index(self.home_breadcrumb), 0,
                             msg='Home page is not shown the first by default')
            self.assertTrue(breadcrumbs[self.home_breadcrumb].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.home_breadcrumb}" breadcrumb')

            self.assertEqual(list(breadcrumbs.keys()).index('SNOOKER'), 1,
                             msg=f'"{self.sport_name}" sport title is not shown after "{self.home_breadcrumb}"')
            self.assertTrue(breadcrumbs['SNOOKER'].angle_bracket,
                            msg=f'Angle bracket is not shown after "{self.sport_name}" breadcrumb')
            self.assertEqual(list(breadcrumbs.keys()).index(self.highlight_tab), 2,
                             msg=f'" matches " item name is not shown after "{self.sport_name}"')
            self.assertTrue(
                int(breadcrumbs[self.highlight_tab].link.css_property_value('font-weight')) == 700,
                msg=f'" outright " hyperlink from breadcrumbs is not highlighted according to the selected page')
        accordions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(accordions, msg="Events are not shown in outright tab")
        accordion = list(accordions.values())[0]
        accordion.expand()
        events = accordion.items_as_ordered_dict
        # Assert that at least one event is found
        self.assertTrue(events, msg='No events found in the section')
        event = list(events.values())[0]
        self.__class__.event_id = event.event_id
        event.click()
        self.site.wait_content_state("EVENTDETAILS")
        if self.device_type != 'mobile':
            sport_breadcrumb = self.site.sport_event_details.breadcrumbs.items_as_ordered_dict.get("Snooker")
            sport_breadcrumb.click()
            self.site.wait_content_state(state_name='Snooker')

    def test_007_verify_by_clicking_on_backward_chevron_beside_sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside sport header
        EXPECTED: Desktop
        EXPECTED: User should be naviagted to homepage
        """
        if self.device_type != 'mobile':
            self.site.back_button.click()
            self.site.wait_content_state("EVENTDETAILS")
            sport_breadcrumb = self.site.sport_event_details.breadcrumbs.items_as_ordered_dict.get("Home")
            sport_breadcrumb.click()
            self.site.wait_content_state("homepage")
            self.site.open_sport(self.sport_name, content_state='Snooker')
            self.site.contents.tabs_menu.items_as_ordered_dict.get(self.expected_tab_name).click()

    def test_008_verify_by_clicking_on_backward_chevron_on_above__sport_header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron on above  sport header
        EXPECTED: Mobile
        EXPECTED: User should be navigated to sport navigation page
        """
        if self.device_type == 'mobile':
            self.site.back_button.click()
            self.site.wait_content_state(state_name='Snooker')
            current_tab_on_sport_slp = self.site.sports_page.tabs_menu.current
            self.assertTrue(current_tab_on_sport_slp.upper() == self.expected_tab_name.upper(),
                            msg="After clicking on back button from event detail page outright tab is not selected by defualt ")

    def test_009_verify_by_expanding_the_accordion_and_click_on_events(self):
        """
        DESCRIPTION: Verify by expanding the accordion and click on events
        EXPECTED: User should navigate to the respective page .
        """
        if self.device_type != 'mobile':
            accordions = self.site.sports_page.tab_content.accordions_list.items_as_ordered_dict
            self.assertTrue(accordions, msg="Events are not shown in outright tab")
            accordion = list(accordions.values())[0]
            accordion.expand()
            events = accordion.items_as_ordered_dict
            # Assert that at least one event is found
            self.assertTrue(events, msg='No events found in the section')
            event = list(events.values())[0]
            self.__class__.event_id = event.event_id
            event.click()
            self.site.wait_content_state("EVENTDETAILS")

    def test_010_verify_by_clicking_on_backward_chevron_beside_outright__header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron beside outright  header
        EXPECTED: Desktop
        EXPECTED: User should navigate  to Outright's page
        """
        if self.device_type != 'mobile':
            wait_for_result(lambda: self.site.back_button, name='Back button to be available', timeout=10,
                            bypass_exceptions=VoltronException)
            self.site.back_button.click()
            self.site.wait_content_state(state_name='Snooker')
            current_tab_on_sport_slp = self.site.sports_page.tabs_menu.current
            self.assertTrue(current_tab_on_sport_slp.upper() == self.expected_tab_name.upper(),
                            msg="After clicking on back button from event detail page outright tab is not selected by defualt ")

    def test_011_verify_by_clicking_on_backward_chevron_on_above__outright__header(self):
        """
        DESCRIPTION: Verify by clicking on backward chevron on above  Outright  header
        EXPECTED: Mobile
        EXPECTED: User should be navigate to Outright's page
        """
        # covered in above steps

    def test_012_verify_bet_placements_for_single_multiple_complex(self):
        """
        DESCRIPTION: Verify bet placements for single, multiple, complex
        EXPECTED: Bet placements should be successful
        """
        # **************** place single bet ********************************
        outright_selections = self.get_outrights_selections()

        if len(outright_selections) >= 1:
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=outright_selections[0])
            self.place_single_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        # ********************   place multiple bet ************************
        if len(outright_selections) > 1:
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=outright_selections[0:2])
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
        # ***************  validate complex bets ********************************
        if len(outright_selections) > 2:
            self.__class__.expected_betslip_counter_value = 0
            self.open_betslip_with_selections(selection_ids=outright_selections[0:3])
            self.place_multiple_bet(number_of_stakes=1)
            self.check_bet_receipt_is_displayed()
            self.site.close_betreceipt()
