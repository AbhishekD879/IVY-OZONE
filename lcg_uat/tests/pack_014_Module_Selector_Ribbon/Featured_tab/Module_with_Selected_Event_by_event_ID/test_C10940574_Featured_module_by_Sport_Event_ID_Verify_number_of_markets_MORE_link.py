import pytest
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create events with multiple markets in prod/beta
@pytest.mark.mobile_only
@pytest.mark.medium
@pytest.mark.homepage_featured
@vtest
class Test_C10940574_Featured_module_by_Sport_Event_ID_Verify_number_of_markets_MORE_link(BaseFeaturedTest):
    """
    TR_ID: C10940574
    NAME: Featured module by <Sport> Event ID: Verify '<number of markets> MORE >' link
    DESCRIPTION: This test case verifies '<number of markets> MORE >' link on the Event section.
    PRECONDITIONS: 1.  Active Featured modules by EventID(not Outright Event with primary market) is created in CMS and displayed on Featured tab in app. Make sure you have events with one market and with more than one market in those modules.
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3.  In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: On the Featured tab calculation of markets is implemented in another way as on Landing pages. The following filter is used:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForEvent/XXX,...,XXX?count=event:market&simpleFilter=event.siteChannels:contains:M
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   XXX,...,XXX - list of Event ID's
    PRECONDITIONS: 4. User is on Homepage > Featured tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)Module by <Sport> EventId(not Outright Event with primary market) is created in CMS and is expanded by default.
        """
        self.__class__.markets = [
            ('both_teams_to_score', {'cashout': True}),
            ('match_result_and_both_teams_to_score', {'cashout': True}),
            ('over_under_total_goals', {'cashout': True})]
        params = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets)
        self.__class__.market_id = params.default_market_id
        self.__class__.eventID = params.event_id
        self.__class__.selection_ids = list(params.selection_ids.values())

        self.__class__.module = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=self.eventID,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)
        self.__class__.module_name = self.module['title'].upper()

    def test_001_navigate_to_module_that_has_event_with_multiple_markets(self):
        """
        DESCRIPTION: Navigate to module that has Event with multiple markets
        """
        self.site.wait_content_state('Homepage')
        self.wait_for_featured_module(name=self.module_name)
        self.__class__.module = self.get_section(section_name=self.module_name)
        self.assertTrue(self.module.is_expanded(), msg=f'"{self.module_name}" module is not expanded')

    def test_002_verify_number_of_available_markets_more__link_for_event_with_several_markets(self):
        """
        DESCRIPTION: Verify '<number of available markets> MORE >' link for event with several markets
        EXPECTED: **CORAL:**
        EXPECTED: Link is shown under Price/Odds buttons of event in format:
        EXPECTED: **"<number of available markets> MORE >"**
        EXPECTED: **LADBROKES:**
        EXPECTED: Link is shown over Price/Odds buttons of event in format:
        EXPECTED: **"<number of available markets> MORE >"**
        """
        more_market_link_label = self.module.get_markets_count_string()

        y_location_of_odd_button = self.module.second_player_bet_button.location['y'] + \
            self.module.second_player_bet_button.size['height']
        y_location_of_more_markets_link = self.module.more_markets_link.location['y'] + \
            self.module.more_markets_link.size['height']
        if self.brand == 'ladbrokes':
            self.assertTrue(y_location_of_odd_button >= y_location_of_more_markets_link,
                            msg=f'"{more_market_link_label}" should not be below odds buttons')
        else:
            self.assertTrue(y_location_of_odd_button < y_location_of_more_markets_link,
                            msg=f'"{more_market_link_label}" is not below odds buttons')

    def test_003_verify_number_of_extra_markets_in_brackets(self):
        """
        DESCRIPTION: Verify number of extra markets in brackets
        EXPECTED: For **pre-match** events number of markets correspond to:
        EXPECTED: 'Number of all markets - **1**'
        EXPECTED: For **BIP **events number of markets correspond to:
        EXPECTED: 'Number of markets with **'isMarketBetInRun="true"' **attribute - **1**'
        """
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID)
        markets_count = self.module.get_markets_count()
        expected_count = len(self.markets)
        self.assertEqual(markets_count, expected_count,
                         msg=f'Number of markets present in "MORE" link: "{markets_count}" '
                             f'is not equal to expected: "{expected_count}"')
        for market in event_resp[0]['event']['children']:
            self.assertEquals(market['market']['isMarketBetInRun'], "true",
                              msg="'isMarketBetInRun with attribute is not there for market'")

    def test_004_tap_number_of_markets_more__link(self):
        """
        DESCRIPTION: Tap '<number of markets> MORE >' link
        EXPECTED: '<number of markets> MORE >' link leads to the Event Details page
        """
        self.module.more_markets_link.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_005_navigate_to_module_that_has_event_with_single_market_and_verify_number_of_markets_more__link_for_event_with_only_one_market(self):
        """
        DESCRIPTION: Navigate to module that has Event with single market and Verify '<number of markets> MORE >' link for event with ONLY one market
        EXPECTED: '<number of markets> MORE >' link is not shown on the Event section
        """
        params = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.eventID = params.event_id
        self.__class__.module = self.cms_config.add_featured_tab_module(
            select_event_by='Event', id=self.eventID,
            events_time_from_hours_delta=-10, module_time_from_hours_delta=-10)
        self.__class__.module_name = self.module['title'].upper()
        self.navigate_to_page('Homepage')
        self.site.wait_content_state(state_name='Homepage')
        self.test_001_navigate_to_module_that_has_event_with_multiple_markets()
        self.assertFalse(self.module.has_markets(),
                         msg=f'"{self.module}" does have MORE markets link')
