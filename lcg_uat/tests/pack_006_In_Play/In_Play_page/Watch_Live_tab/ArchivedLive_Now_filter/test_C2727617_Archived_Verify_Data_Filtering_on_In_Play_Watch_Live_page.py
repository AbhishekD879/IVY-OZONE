import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_inplay_ls_structure


# @pytest.mark.tst2 # In-play page is not available
# @pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.high
@pytest.mark.reg156_fix
@pytest.mark.desktop
@pytest.mark.in_play
@vtest
class Test_C2727617_Archived_Verify_Data_Filtering_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727617
    NAME: [Archived] Verify Data Filtering on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies data filtering on 'In-Play Watch Live' page
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 2. Load application and navigate to In-pLay - Watch Live section in Sports Menu Ribbon
    PRECONDITIONS: In order to get a list with Regions (Classes IDs) use a link:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/Class?simpleFilter=class.categoryId:intersects:XX&existsFilter=class:simpleFilter:event.drilldownTagNames:intersects:EVFLAG_BL&existsFilter=class:simpleFilter:event.siteChannels:contains:M&simpleFilter=class.siteChannels:contains:M&existsFilter=class:simpleFilter:event.isLiveNowEvent&simpleFilter=class.hasLiveNowEvent&translationLang=LL
    PRECONDITIONS: *   XX - sports Category ID (for tst2 environmet all sports are: 16,34,51,5,6,24,18,22,31,30,32,23,55,26,28,25,1,9,10,13,48,46,20,3,54,36,8,35,12,42,53,21,19,39,61,104,103,65,82,97,2,52,72,80,29,99,50,59,154,37,110,105,87,108,79,7,149,16,34,51,6,18,9,20,54,36,12,61,104,103,65,82,97,2,52,72,80,29,99,50,59,154,37,110,105,87,108,79,7,149)
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: For each Class retrieve a list of Events:
    PRECONDITIONS: https://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForClass/XXX?simpleFilter=event.siteChannels:contains:M&simpleFilter=market.siteChannels:contains:M&simpleFilter=outcome.siteChannels:contains:M&simpleFilter=market.isMarketBetInRun&limitTo=market.displayOrder:isLowest&simpleFilter=event.isStarted&simpleFilter=event.drilldownTagNames:intersects:EVFLAG_BL&existsFilter=market:simpleFilter:outcome.outcomeMeaningMajorCode:in:HH,MR&simpleFilter=event.isLiveNowEvent&existsFilter=event:simpleFilter:market.isDisplayed&existsFilter=event:simpleFilter:market.isMarketBetInRun&existsFilter=event:simpleFilter:market.isResulted:isFalse&simpleFilter=event.suspendAtTime:greaterThan:YYYY-MM-DDTHH:MM:SSZ&translationLang=LL
    PRECONDITIONS: *   XXX - is a comma separated list of Class ID's;
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *  YYYY-MM-DD HH:MM:SS - date/time when SS request is made (The time needs to be rounded to the nearest minute or 30 seconds to not break the varnish caching)
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    PRECONDITIONS: drilldownTagNames="EVFLAG_BL" - means Bet In Play List
    """
    keep_browser_open = True
    true = 'true'
    is_market_bet_in_run = is_resulted = 0

    def test_001_verify_events_within_page_when_live_now_switcher_is_selected(self):
        """
        DESCRIPTION: Verify events within page, when 'Live Now' switcher is selected
        EXPECTED: All events with attributes:
        EXPECTED: *   Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: *   Attribute 'isStarted="true"' is present
        EXPECTED: *   Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
        EXPECTED: *   Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: *   Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: *   At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: *   At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: *   At least one market is displayed (available in the response)
        EXPECTED: are shown, when 'Live Now' switcher is selected
        """
        self.navigate_to_page('/in-play/watchlive')
        self.site.wait_content_state_changed()
        inplay_events = get_inplay_ls_structure()
        event_ids = inplay_events['liveStream']['eventsIds']
        self.assertTrue(event_ids, msg='Event IDs are not retrieved.')

        for event_id in event_ids:
            event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']
            self._logger.info(msg='Event name is' + event_details['name'])
            self.assertIn('M', event_details['siteChannels'],
                          msg='Event attribute siteChannels does not contain "M".')
            self.assertEqual(self.true, event_details['isStarted'],
                             msg=f'Actual value: "{event_details["isStarted"]}" is not same as '
                                 f'Expected value: "{self.true}"')
            self.assertIn('EVFLAG_BL', event_details['drilldownTagNames'],
                          msg=' Flag "EVFLAG_BL" not found')
            self.assertEqual(self.true, event_details['isLiveNowEvent'],
                             msg=f'Actual value: "{event_details["isStarted"]}" is not same as '
                                 f'Expected value: "{self.true}".')
            markets = event_details['children']
            self.assertTrue(markets, msg='Markets not found')

            for market in markets:
                market_details = market['market']
                self.assertIn('M', market_details['siteChannels'],
                              msg='Market attribute siteChannels does not contain "M"'
                                  'in current market' + market_details["templateMarketName"])
                try:
                    if self.true == market_details['isMarketBetInRun']:
                        self.is_market_bet_in_run += 1
                except KeyError:
                    self._logger.info('current market' + market['market']['templateMarketName'] + ' does not have MarketBetInRun')
                if 'isResulted' not in market_details.keys():
                    self.is_resulted += 1
                try:
                    outcomes = market_details['children']
                except KeyError:
                    self._logger.info('current market' + market_details["templateMarketName"] + ' does not have outcomes')
                    continue
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
