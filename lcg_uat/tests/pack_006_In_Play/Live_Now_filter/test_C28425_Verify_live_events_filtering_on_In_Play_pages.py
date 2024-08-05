import pytest
from tests.base_test import vtest
from tests.Common import Common
from crlat_siteserve_client.utils.exceptions import SiteServeException
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.helpers import get_inplay_ls_structure, get_inplay_structure


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.in_play
@vtest
class Test_C28425_Verify_live_events_filtering_on_In_Play_pages(Common):
    """
    TR_ID: C28425
    NAME: Verify live events filtering on 'In-Play' pages
    DESCRIPTION: This test case verifies live events filtering on 'In-Play' page
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose some Sport
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * For event configuration use Open Bet TI system, see details following the link below:
    PRECONDITIONS: https://confluence.egalacoral.com/display/SPI/Open+Bet+Systems
    PRECONDITIONS: * To get SiteServer info about event use the following url:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/Z.ZZ/EventToOutcomeForEvent/XXXXXXX?translationLang=LL
    PRECONDITIONS: where:
    PRECONDITIONS: Z.ZZ - current supported version of OpenBet SiteServer
    PRECONDITIONS: LL - language (e.g. en, ukr)
    PRECONDITIONS: XXXXXXX - event id
    PRECONDITIONS: * To verify received data use Dev Tools -> Network -> Web Sockets -> ?EIO=3&transport=websocket-> response with type: "IN_PLAY_SPORT_TYPE::XX::LIVE_EVENT::XXX"
    PRECONDITIONS: where
    PRECONDITIONS: XX - Sport/Category Id
    PRECONDITIONS: XXX - Type Id
    PRECONDITIONS: ![](index.php?/attachments/get/40725)
    """
    enable_bs_performance_log = True
    keep_browser_open = True
    true = 'true'
    is_market_bet_in_run = is_resulted = 0

    def test_001_verify_live_events_within_the_page(self):
        """
        DESCRIPTION: Verify live events within the page
        EXPECTED: All events with attributes:
        EXPECTED: * Event's/market's/outcome's attribute 'siteChannels' contains 'M'
        EXPECTED: * Attribute 'isStarted="true"' is present
        EXPECTED: * Event's attribute 'drilldownTagNames' contains "EVFLAG_BL"
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

        for event_id in event_ids:
            try:
                event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']
            except SiteServeException:
                continue
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

    def test_002_repeat_step_1_on_home_page__in_play_tab_mobiletablet_sports_landing_page__in_play_tab_sports_landing_page__in_play_widget_desktop(
            self):
        """
        DESCRIPTION: Repeat step 1 on:
        DESCRIPTION: * Home page > 'In-Play' tab **Mobile/Tablet**
        DESCRIPTION: * Sports Landing Page > 'In-Play' tab
        DESCRIPTION: * Sports Landing page > 'In-play' widget **Desktop**
        EXPECTED:
        """
        if self.device_type == 'mobile':
            self.navigate_to_page('/home/in-play')
            self.site.wait_content_state_changed(timeout=30)
            inplay_events = get_inplay_structure()
            event_ids = inplay_events['livenow']['eventsIds']
        else:
            self.navigate_to_page('/live-stream')
            self.site.wait_content_state_changed(timeout=30)
            inplay_events = get_inplay_ls_structure()
            event_ids = inplay_events['liveStream']['eventsIds']
        self.assertTrue(event_ids, msg='Event IDs are not retrieved.')

        for event_id in event_ids:
            try:
                event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']
            except SiteServeException:
                continue
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
                if market_details['siteChannels']:
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
