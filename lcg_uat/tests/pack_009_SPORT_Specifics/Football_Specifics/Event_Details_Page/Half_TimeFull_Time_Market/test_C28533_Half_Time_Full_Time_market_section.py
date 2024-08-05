import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_008_SPORT_General.BaseSportTest import BaseSportTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@pytest.mark.desktop
@vtest
class Test_C28533_Half_Time_Full_Time_market_section(BaseSportTest):
    """
    TR_ID: C28533
    NAME: Half Time/Full Time market section
    DESCRIPTION: This test case verifies 'Half Time/Full Time market section' market section on Event Details Page
    DESCRIPTION: Test case needs to be run on Mobile/Tablet/Desktop.
    PRECONDITIONS: To get information for an event use the following URL:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - the event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **Note: **Name differences could be present for different events and environments. E.g.:
    PRECONDITIONS: *   TST2: name="Half Time / Full Time"
    PRECONDITIONS: *   PROD: name="|Half-Time/Full-Time|"
    """
    keep_browser_open = True

    def test_000_pre_conditions(self):
        """
            PRECONDITIONS: Create a event
        """
        self.__class__.market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.half_time_full_time

        if tests.settings.backend_env == 'prod':
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id)

            for event in events:
                for market in event['event']['children']:
                    if market.get('market').get('templateMarketName') == self.market_name:
                        self.__class__.eventID = market.get('market').get('eventId')
                        break
            if self.eventID is None:
                raise SiteServeException('There are no available market with Half-time/Full-time market')
        else:
            markets_params = [('half_time_full_time', {'cashout': True})]
            event = self.ob_config.add_autotest_premier_league_football_event(markets=markets_params)
            self.__class__.eventID = event.event_id

            for market in event.ss_response['event']['children']:
                if market['market']['templateMarketName'] == self.market_name:
                    self.__class__.marketid = market['market']['id']

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
        self.site.wait_content_state(state_name='EventDetails', timeout=60)

        self.__class__.markets_tabs_list = self.site.sport_event_details.markets_tabs_list
        self.assertTrue(self.markets_tabs_list,
                        msg='No market tab found on event: "%s" details page' % self.event_name)

        self.__class__.markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.markets_list, msg='Markets list is not present')

    def test_003_go_to_half_timefull_time_market_section(self):
        """
        DESCRIPTION: Go to 'Half Time/Full Time' market section
        EXPECTED: *   Section is present on Event Details Page and titled 'Half Time/Full Time market section'
        EXPECTED: *   It is possible to collapse/expand section
        """
        if self.brand == 'ladbrokes':
            self.__class__.expected_market_name = 'Half Time / Full Time' if tests.settings.backend_env == 'prod' else 'Half time/ Full Time Result Market'
        else:
            self.__class__.expected_market_name = 'HALF TIME/ FULL TIME RESULT MARKET' if self.device_type == 'mobile' else 'Half Time/ Full Time Result Market'

        self.assertIn(self.expected_market_name, self.markets_list, msg=f'"{self.expected_market_name}" section is not present')

        self.__class__.half_time_full_time = self.markets_list.get(self.expected_market_name)
        self.assertTrue(self.half_time_full_time,
                        msg=f'"{self.expected_market_name}" section is not found in "{self.markets_list.keys()}"')

        self.half_time_full_time.collapse()
        self.assertFalse(self.half_time_full_time.is_expanded(expected_result=False),
                         msg=f'"{self.half_time_full_time}" section is not collapsed')

        self.half_time_full_time.expand()
        self.assertTrue(self.half_time_full_time.is_expanded(),
                        msg=f'"{self.expected_market_name}" section is not expanded')

    def test_004_verify_market_name(self):
        """
        DESCRIPTION: Verify market name
        EXPECTED: Selection name corresponds to part of '**name**' attribute on the market level
        EXPECTED: **NOTE** "Result" or "Result Market" can be added in the end of some market names  - this expected and hardcoded
        EXPECTED: e.g. ***Half Time / Full Time Result Market***
        """
        # Covered in step-3

    def test_005_verify_cash_out_label_next_to_market_section_name(self):
        """
        DESCRIPTION: Verify Cash out label next to Market section name
        EXPECTED: If 'Half Time/Full Time' market section has **cashoutAvail="Y"** then label Cash out should be displayed next to market section name
        """
        self.assertTrue(self.half_time_full_time.market_section_header.has_cash_out_mark(),
                        msg=f'Market "{self.half_time_full_time}" has no cashout label')

    def test_006_expandhalf_timefull_time_market_section(self):
        """
        DESCRIPTION: Expand 'Half Time/Full Time' market section
        EXPECTED: The list of available selections received from SS response are displayed within market section
        """
        outcomes = self.markets_list[self.expected_market_name].outcomes.items_as_ordered_dict
        self.assertTrue(outcomes, msg='No items found on market outcomes')

    def test_007_verify_half_timefull_time_section_in_case_of_data_absence(self):
        """
        DESCRIPTION: Verify 'Half Time/Full Time' section in case of data absence
        EXPECTED: 'Half Time/Full Time' section is not shown if:
        EXPECTED: *   market is absent
        EXPECTED: *   there are no outcomes within the market
        """
        if tests.settings.backend_env != 'prod':
            self.ob_config.change_market_state(self.eventID, self.marketid, displayed=False)
            self.device.refresh_page()
            self.site.wait_splash_to_hide()
            self.site.wait_content_state(state_name='EventDetails', timeout=60)
            markets_list = self.site.sport_event_details.tab_content.accordions_list.items_as_ordered_dict
            self.assertNotIn(self.expected_market_name, markets_list,
                             msg=f'"{self.expected_market_name}" section is not present')
