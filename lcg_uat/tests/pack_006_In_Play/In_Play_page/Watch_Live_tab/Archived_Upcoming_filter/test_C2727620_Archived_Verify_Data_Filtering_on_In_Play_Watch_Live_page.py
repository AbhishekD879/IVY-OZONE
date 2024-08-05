import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import get_inplay_ls_structure
from voltron.utils.exceptions.voltron_exception import VoltronException


@pytest.mark.stg2
@pytest.mark.tst2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C2727620_Archived_Verify_Data_Filtering_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727620
    NAME: [Archived] Verify Data Filtering on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies data filtering on 'In-Play Watch Live' page.
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 2. Load application and navigate to In-pLay - Watch Live section in Sports Menu Ribbon
    PRECONDITIONS: 3. Select 'Upcoming' switcher
    PRECONDITIONS: In order to get a list with Regions (Classes IDs) and Leagues (Types IDs) use a link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/ClassToSubType?simpleFilter=class.categoryId:equals:XX&simpleFilter=class.isActive:isTrue&simpleFilter=class.siteChannels:contains:M&translationLang=LL
    PRECONDITIONS: *   XX - sports Category ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: For each Class retrieve a list of Event IDs:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToMarketForClass/XXX?simpleFilter=event.siteChannels:contains:M&simpleFilter=market.siteChannels:contains:M&simpleFilter=market.isMarketBetInRun&simpleFilter=event.drilldownTagNames:intersects:EVFLAG_BL&simpleFilter=event.isNext24HourEvent&simpleFilter=event.isStarted:isFalse&existsFilter=event:simpleFilter:market.isDisplayed&existsFilter=event:simpleFilter:market.isMarketBetInRun&existsFilter=event:simpleFilter:market.isResulted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:YYYY-MM-DDTHH:MM:SSZ&translationLang=en
    PRECONDITIONS: *   XXX -  is a comma separated list of Class ID's;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   YYYY-MM-DD HH:MM:SS - date/time when SS request is made (The time needs to be rounded to the nearest minute or 30 seconds to not break the varnish caching)
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: To retrieve details about a particular event:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX -  is Event ID;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    """
    keep_browser_open = True
    outcome_code = ['MR', 'HH']
    true = 'true'
    is_market_bet_in_run = is_resulted = 0
    enable_bs_performance_log = True

    def test_001_verify_events_within_page_when_upcomingswitcher_is_selected(self):
        """
        DESCRIPTION: Verify events within page, when 'Upcoming' switcher is selected
        EXPECTED: All events with attributes:
        EXPECTED: *   Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: *   Event is NOT started
        EXPECTED: *   Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: *   Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: *   Attribute 'isNext24HourEvent="true"' is present
        EXPECTED: *   At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: *   At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: *   At least one market is displayed (available in the response)
        EXPECTED: are shown, when 'Upcoming' sorting type is selected
        EXPECTED: Events with 'isStarted="true"' attribute are NOT present within 'Upcoming' section
        """
        self.navigate_to_page('/in-play/watchlive')
        self.site.wait_content_state_changed()
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
        inplay_events = get_inplay_ls_structure()
        event_ids = inplay_events['upcomingLiveStream']['eventsIds']
        for event_id in event_ids:
            event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']
            self._logger.info(msg='Event name is' + event_details['name'])
            self.assertIn('M', event_details['siteChannels'],
                          msg='Event attribute siteChannels does not contain "M".')
            self.assertEqual(self.true, event_details['isNext24HourEvent'],
                             msg=f'Actual value: "{event_details["isNext24HourEvent"]}" is not same as '
                                 f'Expected value: "{self.true}"')
            self.assertIn('EVFLAG_BL', event_details['drilldownTagNames'],
                          msg=' Flag "EVFLAG_BL" not found')
            markets = event_details['children']
            self.assertTrue(markets, msg='Markets not found')
            market_details, outcomes = None, None
            for market in markets:
                try:
                    market_details = market['market']
                    self.assertIn('M', market_details['siteChannels'],
                                  msg='Market attribute siteChannels does not contain "M"'
                                      'in current market' + market_details["templateMarketName"])
                    if self.true == market_details['isMarketBetInRun']:
                        self.is_market_bet_in_run += 1
                    if 'isResulted' not in market_details.keys():
                        self.is_resulted += 1
                    outcomes = market_details['children']
                except KeyError:
                    self._logger.info('current market' + market_details["templateMarketName"] + ' does not have outcomes')
                if outcomes:
                    for outcome in outcomes:
                        outcome_details = outcome['outcome']
                        self.assertIn('M', outcome_details['siteChannels'],
                                      msg='Outcome attribute siteChannels does not contain "M".')

            if self.is_market_bet_in_run < 1:
                raise VoltronException('Event name' + event_details['name'] +
                                       'doesnt have atleast one market with "is_market_bet_in_run" as true.')
            if self.is_resulted < 1:
                raise VoltronException('Event name' + event_details['name'] +
                                       'doesnt have atleast one market with "is resulted".')
