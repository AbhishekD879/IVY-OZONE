import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # Event can not be created in prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28564_1st_Half__2nd_Half_Result_section_order_in_markets_list(Common):
    """
    TR_ID: C28564
    NAME: 1st Half / 2nd Half Result section order in markets list
    DESCRIPTION: This test case verifies '1st Half / 2nd Half Result' section order in markets list on Event Details Page.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: Football events with 1st Half / 2nd Half Result markets (name="First-Half Result", name="Second-Half Result")
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="First-Half Result"
    PRECONDITIONS: *   PROD: name="1st Half Result"
    """
    keep_browser_open = True
    EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS = ['1ST HALF', '2ND HALF']

    def test_000_pre_conditions(self):
        """
        PRECONDITIONS: Create a event
        """
        self.__class__.market_name = '1st Half / 2nd Half Result'
        markets_params = [('first_half_result', {'cashout': True}),
                          ('second_half_result', {'cashout': True})]
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_event(markets=markets_params)
        self.__class__.eventID = self.event.event_id
        self.__class__.event_name = '%s v %s' % (self.event.team1, self.event.team2)
        for market in self.event.ss_response['event']['children']:
            if market['market']['templateMarketName'] == 'First-Half Result':
                self.__class__.first_half_market = market['market']
            elif market['market']['templateMarketName'] == 'Second-Half Result':
                self.__class__.second_half_market = market['market']

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')

    def test_002_go_to_event_details_page_of_football_event(self):
        """
        DESCRIPTION: Go to Event Details page of Football event
        EXPECTED: Event Details page is opened successfully representing available markets
        """
        self.navigate_to_edp(self.eventID, timeout=60)
        wait_for_result(lambda: self.site.wait_content_state(state_name='EventDetails'), timeout=120)
        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(self.markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)
        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

    def test_003_go_to_1st_half__2nd_half_result_section(self):
        """
        DESCRIPTION: Go to '1st Half / 2nd Half Result' section
        EXPECTED: Section contains data from two markets:
        EXPECTED: *   First-Half Result
        EXPECTED: *   Second-Half Result
        EXPECTED: If markets are not available - section is not shown
        """
        if self.brand == 'bma' and self.device_type == 'mobile':
            expected_market_name = self.market_name.upper()
        else:
            expected_market_name = self.market_name
        self.assertIn(expected_market_name, self.markets_list,
                      msg=f'"{expected_market_name}" section is not present')
        self.__class__.first_half_second_half = self.markets_list.get(expected_market_name)
        self.assertTrue(self.first_half_second_half,
                        msg=f'"{expected_market_name}" section is not found in "{self.markets_list.keys()}"')
        first_half_second_half = self.first_half_second_half.grouping_buttons.items_names
        self.assertEqual(first_half_second_half, self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS,
                         msg=f'Actual market headers "{first_half_second_half}" '
                             f'are not same as expected headers: "{self.EXPECTED_FIRST_HALF_SECOND_HALF_SWITCHERS}"')

    def test_004_check_displayorder_attribute_values_of_all_markets_available_in_1st_half__2nd_half_result_section_in_ss_response(self):
        """
        DESCRIPTION: Check '**displayOrder**' attribute values of all markets available in '1st Half / 2nd Half Result' section in SS response
        EXPECTED: **Smallest displayOrder** of First-Half Result, Second-Half Result markets **is set as section's display order**
        """
        first_half_result_display_order = self.first_half_market['displayOrder']
        self.assertTrue(first_half_result_display_order, msg="Display order is not displayed")
        second_half_result_display_order = self.second_half_market['displayOrder']
        self.assertTrue(second_half_result_display_order, msg="Display order is not displayed")
        display_order_list = [int(first_half_result_display_order), int(second_half_result_display_order)]
        self.assertEqual(sorted(display_order_list), display_order_list,
                         msg=f'Actual order of displayOrder: "{sorted(display_order_list)}" is not same as'
                             f'Expected order of displayOrder: "{display_order_list}"')

    def test_005_check_sections_order_in_markets_list(self):
        """
        DESCRIPTION: Check section's order in markets list
        EXPECTED: Section is ordered by:
        EXPECTED: *   by** displayOrder** **in ascending**
        EXPECTED: *   if displayOrder is the same then **alphanumerically**
        """
        # covered in above step
