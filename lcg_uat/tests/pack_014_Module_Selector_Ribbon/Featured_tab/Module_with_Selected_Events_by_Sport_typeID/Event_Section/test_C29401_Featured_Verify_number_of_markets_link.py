import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod  # Cannot create events in Prod/Beta
@pytest.mark.medium
@pytest.mark.homepage_featured
@pytest.mark.desktop
@vtest
class Test_C29401_Featured_Verify_number_of_markets_link(Common):
    """
    TR_ID: C29401
    NAME: Featured: Verify '+<number of markets>' link
    DESCRIPTION: This test case verifies '+<number of markets>' link on the Event section.
    DESCRIPTION: **Jira ticket:** BMA-1624
    PRECONDITIONS: 1.  Active Featured module by TypeID is created in CMS and displayed on Featured tab in app. Make sure you have events with one market and with more than one market in this module.
    PRECONDITIONS: 2. CMS, TI: https://confluence.egalacoral.com/display/SPI/Environments+-+to+be+reviewed
    PRECONDITIONS: 3.  In order to check event data use link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: **NOTE**: '+<number of markets>' link is shown only for events that are retrieved by typeID, for boosted selections link is not displayed.
    PRECONDITIONS: On the Featured tab calculation of markets is implemented in another way as on Landing pages. The following filter is used:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForEvent/XXX,...,XXX?count=event:market&simpleFilter=event.siteChannels:contains:M
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   XXX,...,XXX - list of Event ID's
    PRECONDITIONS: 4. User is on Homepage > Featured tab
    """
    keep_browser_open = True
    event_markets = [
        ('sixty_minutes_betting',),
        ('puck_line',),
        ('total_goals_2_way',)
    ]
    number_of_markets = 4

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create test prematch event
        EXPECTED: Prematch event created successfully
        """
        event = self.ob_config.add_ice_hockey_event_to_ice_hockey_usa(markets=self.event_markets)
        self.__class__.eventID = event.event_id
        team1, team2 = event.team1, event.team2
        self.__class__.event_name = f'{team2} v {team1}'
        self._logger.info(f'*** Created Ice Hockey event "{self.event_name}"')
        event_resp = self.ss_req.ss_event_to_outcome_for_event(event_id=self.eventID,
                                                               query_builder=self.ss_query_builder)
        full_section_name = event.ss_response['event']['categoryCode'] + self.get_accordion_name_for_event_from_ss(
            event=event_resp[0])
        self.__class__.section_name = full_section_name.replace('ICE_HOCKEY', '')

        event_one_market = self.ob_config.add_ice_hockey_event_to_ice_hockey_usa()
        self.__class__.eventID_one_market = event_one_market.event_id
        team1, team2 = event_one_market.team1, event_one_market.team2
        self.__class__.event_name_one_market = f'{team2} v {team1}'

    def test_001_go_to_event_section(self):
        """
        DESCRIPTION: Go to Event section
        EXPECTED:
        """
        self.navigate_to_page(name='sport/ice-hockey')
        self.site.wait_content_state(state_name='IceHockey')
        sleep(5)
        self.__class__.sections = self.site.ice_hockey.tab_content.accordions_list.items_as_ordered_dict
        self.assertTrue(self.sections, msg='No sections found on page')
        self.__class__.section = self.sections.get(self.section_name)
        self.assertTrue(self.section,
                        msg=f'"{self.section_name}" module not found in sections "{", ".join(self.sections.keys())}"')
        self.__class__.events = self.section.items_as_ordered_dict
        self.assertTrue(self.events, msg='No events found on Specials page')

    def test_002_verify_plusnumber_of_markets_link_for_event_with_several_markets(self):
        """
        DESCRIPTION: Verify '+<number of markets>' link for event with several markets
        EXPECTED: Link is shown next to the Price/Odds buttons of event in format:
        EXPECTED: **"+<number of available markets>"**
        """
        self.__class__.event_mult_markets = self.events.get(self.event_name)
        self.assertTrue(self.event_mult_markets.has_markets(), msg='"{self.event_name}" does not have markets link')

    def test_003_verify_number_of_extra_markets_in_brackets(self):
        """
        DESCRIPTION: Verify number of extra markets in brackets
        EXPECTED: For **pre-match** events number of markets correspond to:
        EXPECTED: 'Number of all markets - **1**'
        EXPECTED: For **BIP **events number of markets correspond to:
        EXPECTED: 'Number of markets with **'isMarketBetInRun="true"' **attribute - **1**'
        """
        more_market_link_label = self.event_mult_markets.get_markets_count_string()
        market_count = str(self.number_of_markets - 1)
        self.assertTrue(market_count in more_market_link_label, msg='number of extra markets not correct')

    def test_004_tap_plusnumber_of_markets_link(self):
        """
        DESCRIPTION: Tap '+<number of markets>' link
        EXPECTED: '+<number of markets>' link leads to the Event Details page
        """
        self.event_mult_markets.more_markets_link.click()
        self.site.wait_content_state('EventDetails', timeout=20)

    def test_005_verify_plusnumber_of_markets_link_for_event_with_only_one_market(self):
        """
        DESCRIPTION: Verify '+<number of markets>' link for event with ONLY one market
        EXPECTED: '+<number of markets>' link is not shown on the Event section
        """
        self.test_001_go_to_event_section()
        self.__class__.event_single_market = self.events.get(self.event_name_one_market)
        self.assertFalse(self.event_single_market.has_markets(),
                         msg='"{self.event_name_one_market}" does not have markets link')
