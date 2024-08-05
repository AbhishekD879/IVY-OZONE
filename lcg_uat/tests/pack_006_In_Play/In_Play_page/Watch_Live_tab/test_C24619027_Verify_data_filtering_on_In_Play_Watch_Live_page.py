import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from crlat_siteserve_client.utils.exceptions import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_inplay_ls_structure
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.in_play
@pytest.mark.desktop
@vtest
class Test_C24619027_Verify_data_filtering_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C24619027
    NAME: Verify data filtering on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies live and upcoming events with mapped stream filtering on 'In-Play Watch Live' page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose 'Watch Live' tab
    PRECONDITIONS: 3. Make sure that Live and Upcoming events with the mapped stream are present in 'Live Now' and 'Upcoming' sections (for mobile/tablet) or when 'Live Now'/'Upcoming' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * 'InPlayWatchLive' should be enabled in CMS > System configuration > Structure > InPlayWatchLive
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * Be aware that 'drilldownTagNames' to determine WHICH stream provider has been mapped to the event
    PRECONDITIONS: **'drilldownTagNames'**** ***Streaming flags are:*
    PRECONDITIONS: * EVFLAG_IVM -  IMG Video Mapped for this event
    PRECONDITIONS: * EVFLAG_PVM - Perform Video Mapped for this event
    PRECONDITIONS: * EVFLAG_GVM' - iGameMedia Video Mapped for this event
    PRECONDITIONS: * To verify attributes received for recognazing if events have mapped stream use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::STREAM_EVENT::XXX" for live now events and "IN_PLAY_SPORT_TYPE::XX::UPCOMING_STREAM_EVENT::XXX" for upcoming events
    PRECONDITIONS: where
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40724)
    """
    keep_browser_open = True
    true = 'true'
    is_market_bet_in_run = is_resulted = 0
    enable_bs_performance_log = True

    def verify_data_filtering(self, event_ids, inplay=True):
        for event_id in event_ids:
            try:
                event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']
            except SiteServeException:
                continue
            self._logger.info(msg='Event name is' + event_details['name'])
            self.assertIn('M', event_details['siteChannels'],
                          msg=f'Event attribute siteChannels does not contain "M" for "{event_details["name"]}"')
            if inplay:
                self.assertEqual(self.true, event_details['isStarted'],
                                 msg=f'Actual value: "{event_details["isStarted"]}" is not same as '
                                 f'Expected value: "{self.true}" for "{event_details["name"]}"')
                self.assertEqual(self.true, event_details['isLiveNowEvent'],
                                 msg=f'Actual value: "{event_details["isStarted"]}" is not same as '
                                     f'Expected value: "{self.true}". for "{event_details["name"]}"')
            else:
                result = wait_for_result(lambda: 'isStarted' not in [event_details.keys()], timeout=0.5)
                self.assertTrue(result, msg=f'attribute "isStarted" is present'
                                            f'for "{event_details["name"]}"')
            self.assertIn('EVFLAG_BL', event_details['drilldownTagNames'],
                          msg=f' Flag "EVFLAG_BL" not found for "{event_details["name"]}"')
            stream_flag = 'EVFLAG_IVM' or 'EVFLAG_PVM' or 'EVFLAG_GVM' in event_details['drilldownTagNames']
            self.assertTrue(stream_flag, msg=f' Flags "EVFLAG_IVM or EVFLAG_PVM or EVFLAG_GVM"not found for "{event_details["name"]}"')
            flag_code = 'IVA' or 'PVA' or 'GVA' in event_details['typeFlagCodes']
            self.assertTrue(flag_code,
                            msg=f' Flags "IVA or PVA or GVA" not found for "{event_details["name"]}"')
            markets = event_details['children']
            self.assertTrue(markets, msg='Markets not found')

            for market in markets:
                market_details = market['market']
                self.assertIn('M', market_details['siteChannels'],
                              msg='Market attribute siteChannels does not contain "M"'
                                  'in current market' + market_details["templateMarketName"])
                if self.true == market_details.get('isMarketBetInRun'):
                    self.is_market_bet_in_run += 1
                if 'isResulted' not in market_details.keys():
                    self.is_resulted += 1
                try:
                    outcomes = market_details['children']
                except KeyError:
                    self._logger.info(
                        'current market' + market_details["templateMarketName"] + ' does not have outcomes')
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
            self.is_market_bet_in_run = self.is_resulted = 0

    def test_000_preconditions(self):
        """
        DESCRIPTION: 1) Several sports should contain live events, upcoming events and events with 'Watch live' label
        """
        if tests.settings.backend_env != 'prod':
            start_time_upcoming = self.get_date_time_formatted_string(hours=10)
            self.ob_config.add_autotest_premier_league_football_event(is_live=True, perform_stream=True)
            self.ob_config.add_autotest_premier_league_football_event(is_upcoming=True, perform_stream=True, start_time=start_time_upcoming)

    def test_001_verify_events_within_live_now_section_when_live_now_switcher_is_selected(self):
        """
        DESCRIPTION: Verify events within 'Live now' section/ when 'Live Now' switcher is selected
        EXPECTED: All events with attributes:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * Event's attribute 'drilldownTagNames' contains
        EXPECTED: {"EVFLAG_BL" AND "EVFLAG_IVM"} OR {"EVFLAG_BL" AND "EVFLAG_PVM"} OR {"EVFLAG_BL" AND "EVFLAG_GVM"}
        EXPECTED: * Type's attribute contains 'typeFlagCodes' contains "IVA" OR "PVA" OR "GVA"
        EXPECTED: * Attribute 'isLiveNowEvent="true"' is present
        EXPECTED: * Time in 'suspendAtTime' attribute of the event is NOT in the past or it is not present
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        """
        self.navigate_to_page('/in-play/watchlive')
        self.site.wait_content_state_changed(timeout=30)
        inplay_events = get_inplay_ls_structure()
        event_ids = inplay_events['liveStream']['eventsIds']
        self.assertTrue(event_ids, msg='Event IDs are not retrieved.')
        self.verify_data_filtering(event_ids=event_ids)

    def test_002_verify_events_within_upcoming_events_section_when_upcoming_switcher_is_selected(self):
        """
        DESCRIPTION: Verify events within 'Upcoming Events' section/ when 'Upcoming' switcher is selected
        EXPECTED: All events with attributes:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Event is NOT started
        EXPECTED: * Event's attribute 'drilldownTagNames' contains
        EXPECTED: {"EVFLAG_BL" AND "EVFLAG_IVM"} OR {"EVFLAG_BL" AND "EVFLAG_PVM"} OR {"EVFLAG_BL" AND "EVFLAG_GVM"}
        EXPECTED: * Type's attribute contains 'typeFlagCodes' contains "IVA" OR "PVA" OR "GVA"
        EXPECTED: * At least one market contains attribute 'isMarketBetInRun="true"'
        EXPECTED: * At least one market is not resulted (there is no attribute 'isResulted="true")
        EXPECTED: * At least one market is displayed (available in the response)
        EXPECTED: are shown
        EXPECTED: Events with 'isStarted="true"' attribute are NOT present within 'Upcoming' section
        """
        if self.device_type == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)
        inplay_events = get_inplay_ls_structure()
        event_ids = inplay_events['upcomingLiveStream']['eventsIds']
        self.assertTrue(event_ids, msg='Event IDs are not retrieved.')
        self.verify_data_filtering(event_ids=event_ids, inplay=False)
