import pytest
from selenium.common.exceptions import StaleElementReferenceException
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from tests.base_test import vtest
from tests.pack_014_Module_Selector_Ribbon.BaseFeaturedTest import BaseFeaturedTest
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # cannot create eventhub in prod/beta
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.mobile_only
@vtest
class Test_C11088160_Featured_module_by_Sport_Event_ID_Verify_number_of_markets_MORE_link(BaseFeaturedTest):
    """
    TR_ID: C11088160
    NAME: Featured module by <Sport> Event ID: Verify '<number of markets> MORE >' link
    DESCRIPTION: This test case verifies '<number of markets> MORE >' link on the Event section.
    PRECONDITIONS: 1. Event Hub is created in CMS > Sport Pages > Event Hub.
    PRECONDITIONS: 2. Module by <Sport> EventId(not Outright Event with the primary market) is created in EventHub. Make sure you have events with one market and with more than one market in those modules.
    PRECONDITIONS: 3. A user is on Homepage > EventHub tab
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: In order to check event data use the link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: XXX - event ID
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: On the Featured tab calculation of markets is implemented in another way as on Landing pages. The following filter is used:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForEvent/XXX,...,XXX?count=event:market&simpleFilter=event.siteChannels:contains:M
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: XXX,...,XXX - list of Event ID's
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
            PRECONDITIONS: Event Hub is created in CMS > Sport Pages > Event Hub.
        """
        self.__class__.extra_markets_event1 = [('both_teams_to_score', {'cashout': True})]
        event_with_two_markets = self.ob_config.add_autotest_premier_league_football_event(
            markets=self.extra_markets_event1)
        eventID_two_markets = event_with_two_markets.event_id
        self.__class__.event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=eventID_two_markets,
                                                                              query_builder=self.ss_query_builder)

        event_with_one_market = self.ob_config.add_autotest_premier_league_football_event()
        eventID_one_market = event_with_one_market.event_id
        existing_event_hubs = self.cms_config.get_event_hubs()
        existed_index_number = [index['indexNumber'] for index in existing_event_hubs]
        index_number = next(index for index in range(1, 20) if index not in existed_index_number)
        self.cms_config.create_event_hub(index_number=index_number)
        self.cms_config.add_sport_module_to_event_hub(page_id=index_number, module_type='FEATURED')
        module_data = self.cms_config.add_featured_tab_module(select_event_by='Event', id=eventID_two_markets,
                                                              page_type='eventhub',
                                                              page_id=index_number,
                                                              events_time_from_hours_delta=-10,
                                                              module_time_from_hours_delta=-10)
        self.__class__.module_name = module_data['title'].upper()

        self.__class__.module_data_single = self.cms_config.add_featured_tab_module(select_event_by='Event',
                                                                                    id=eventID_one_market,
                                                                                    page_type='eventhub',
                                                                                    page_id=index_number,
                                                                                    events_time_from_hours_delta=-10,
                                                                                    module_time_from_hours_delta=-10)

        internal_id = f'tab-eventhub-{index_number}'
        event_hub_tab_data = self.cms_config.module_ribbon_tabs.create_tab(directive_name='EventHub',
                                                                           internal_id=internal_id,
                                                                           hub_index=index_number,
                                                                           display_date=True)

        self.__class__.event_hub_tab_name = event_hub_tab_data.get('title').upper()
        self.site.wait_content_state(state_name='Homepage')

    @retry(stop=stop_after_attempt(10), wait=wait_fixed(wait=40),
           retry=retry_if_exception_type((StaleElementReferenceException, VoltronException)), reraise=True)
    def test_001_navigate_to_the_module_that_has_event_with_multiple_markets(self):
        """
        DESCRIPTION: Navigate to the module that has Event with multiple markets
        EXPECTED:
        """
        self.device.refresh_page()
        event_hub_content = self.site.home.get_module_content(self.event_hub_tab_name)
        self.assertTrue(event_hub_content, msg=f'Event hub module "{self.event_hub_tab_name}" was not found')
        event_hub_modules = event_hub_content.accordions_list.items_as_ordered_dict
        self.assertTrue(event_hub_modules, msg=f'No modules found on "{self.event_hub_tab_name}" tab')
        self.__class__.event_hub_module = event_hub_modules.get(self.module_name)
        self.assertTrue(self.event_hub_module,
                        msg=f'Module "{self.module_name}" is not found on {self.event_hub_tab_name} tab')
        self.assertTrue(self.event_hub_module.is_expanded(timeout=2),
                        msg=f'Module: "{self.module_name}" not expanded')

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
        more_market_link_label = self.event_hub_module.get_markets_count_string()

        y_location_of_odd_button = self.event_hub_module.second_player_bet_button.location['y'] + self.event_hub_module.second_player_bet_button.size['height']
        y_location_of_more_markets_link = self.event_hub_module.more_markets_link.location['y'] + self.event_hub_module.more_markets_link.size['height']
        if self.brand == 'ladbrokes':
            self.assertTrue(y_location_of_odd_button >= y_location_of_more_markets_link,
                            msg=f'"{more_market_link_label}" should not be below odds buttons')
        else:
            self.assertTrue(y_location_of_odd_button < y_location_of_more_markets_link,
                            msg=f'"{more_market_link_label}" is not below odds buttons')

    def test_003_verify_the_number_of_extra_markets_in_brackets(self):
        """
        DESCRIPTION: Verify the number of extra markets in brackets
        EXPECTED: For **pre-match** events number of markets correspond to:
        EXPECTED: 'Number of all markets - **1**'
        EXPECTED: For **BIP** events number of markets correspond to:
        EXPECTED: 'Number of markets with **'isMarketBetInRun="true"' **attribute - 1**'
        """
        markets_count = self.event_hub_module.get_markets_count()
        expected_count = len(self.extra_markets_event1)
        self.assertEqual(markets_count, expected_count,
                         msg=f'Number of markets present in "MORE" link: "{markets_count}" '
                             f'is not equal to expected: "{expected_count}"')
        for market in self.event_resp[0]['event']['children']:
            self.assertEquals(market['market']['isMarketBetInRun'], "true",
                              msg="'isMarketBetInRun with attribute is not there for market'")

    def test_004_tap_number_of_markets_more__link(self):
        """
        DESCRIPTION: Tap '<number of markets> MORE >' link
        EXPECTED: '<number of markets> MORE >' link leads to the Event Details page
        """
        self.event_hub_module.more_markets_link.click()
        self.site.wait_content_state(state_name='EventDetails')

    def test_005_navigate_to_the_module_that_has_event_with_a_single_market_and_verify_number_of_markets_more__link_for_event_with_only_one_market(
            self):
        """
        DESCRIPTION: Navigate to the module that has Event with a single market and Verify '<number of markets> MORE >' link for event with ONLY one market
        EXPECTED: '<number of markets> MORE >' link is not shown on the Event section
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state(state_name='Homepage')
        self.module_name = self.module_data_single['title'].upper()
        self.test_001_navigate_to_the_module_that_has_event_with_multiple_markets()
        self.assertFalse(self.event_hub_module.has_markets(),
                         msg='"{self.event_hub_module}" does not have markets link')
