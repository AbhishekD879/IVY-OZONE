import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.helpers import get_inplay_ls_structure


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C2727612_Archived_Verify_Primary_Market_Data_on_In_Play_Watch_Live_page(Common):
    """
    TR_ID: C2727612
    NAME: [Archived] Verify Primary Market Data on 'In-Play Watch Live' page
    DESCRIPTION: This test case verifies Primary Market Data on 'In-Play Watch Live' page.
    PRECONDITIONS: 1. Live now/Upcoming events* with attached Live Stream should be preconfigured in TI.
    PRECONDITIONS: *events should be configured for different Sports and different Types of individual Sport (e.g Football - England Football League Trophy)
    PRECONDITIONS: 2. Load Oxygen application
    PRECONDITIONS: 3. Load application and navigate to In-Play - Watch Live section in Sports Menu Ribbon
    PRECONDITIONS: 4. Navigate to <Sport> event section when 'Live Now' switcher is selected
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True
    outcome_code = ['MR', 'HH', '--']
    enable_bs_performance_log = True

    def test_001_verify_sport_event_with_available_selections(self):
        """
        DESCRIPTION: Verify <Sport> event with available selections
        EXPECTED: Only selections that belong to the Market with the following attributes are shown on In-Play Landing page:
        EXPECTED: *   Market's attribute 'siteChannels' contains 'M'
        EXPECTED: *   Attribute 'isMarketBetInRun="true"' is present
        EXPECTED: *   All selections in such market have 'outcomeMeaningMajorCode="MR"/"HH"'
        EXPECTED: *   All selections in such market have attribute 'siteChannels' contains 'M'
        EXPECTED: If event has several markets that contain the above attributes - selections from the market **with the lowest 'displayOrder'** are shown on In-Play Landing page
        """
        self.navigate_to_page('/in-play/watchlive')
        self.site.wait_content_state_changed()
        inplay_events = get_inplay_ls_structure()
        event_ids = inplay_events['liveStream']['eventsIds']
        for event_id in event_ids:
            event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']
            self.assertIn('M', event_details['siteChannels'], msg="Site channel details  not found")
            self.assertIn('EVFLAG_BL', event_details['drilldownTagNames'], msg="Drill down tag names not found")
            self.assertEqual('true', event_details['isStarted'], msg="Event is not started")
            self.assertEqual('true', event_details['isLiveNowEvent'], msg="Not a live event")
            markets = event_details['children']
            self.assertTrue(markets, msg="Markets not available")
            for market in markets:
                market_details = market['market']
                try:
                    self.assertEqual('true', market_details['isMarketBetInRun'], msg="isMarketBetInRun not found")
                    self.assertNotIn('isResulted', market_details.keys(), msg="Resulted events found")
                    self.assertIn('M', market_details['siteChannels'], msg="Site channel details not found")
                    outcomes = market_details['children']
                    for outcome in outcomes:
                        outcome_details = outcome['outcome']
                        self.assertIn('M', outcome_details['siteChannels'], msg="SiteChannel = M not found")
                        self.assertTrue(outcome_details['outcomeMeaningMajorCode'],
                                        msg="Outcome Meaning Major Code is not present")
                except KeyError:
                    self._logger.info(msg='current market' + market_details['templateMarketName'] + 'odds might suspended')

    def test_002_navigate_to_event_section_whenupcomingswitcher_is_selected(self):
        """
        DESCRIPTION: Navigate to event section when 'Upcoming' switcher is selected
        EXPECTED: The list of pre-match events is displayed on the page
        """
        self.navigate_to_page('/in-play/watchlive')
        self.site.wait_content_state_changed()
        if self.device == 'desktop':
            self.site.inplay.tab_content.grouping_buttons.click_button(vec.inplay.UPCOMING_SWITCHER)

    def test_003_repeat_step_1(self):
        """
        DESCRIPTION: Repeat step #1
        """
        inplay_events = get_inplay_ls_structure()
        event_ids = inplay_events['upcomingLiveStream']['eventsIds']
        self.assertTrue(event_ids, msg='Event IDs are not retrieved.')
        for event_id in event_ids:
            event_details = self.ss_req.ss_event_to_outcome_for_event(event_id=event_id)[0]['event']
            self._logger.info(msg='Event name is' + event_details['name'])
            self.assertIn('M', event_details['siteChannels'], msg="Site channel details  not found")
            self.assertIn('EVFLAG_BL', event_details['drilldownTagNames'], msg="Drill down tag names not found")
            markets = event_details['children']
            self.assertTrue(markets)
            for market in markets:
                market_details = market['market']
                self._logger.info(msg='current market name is' + market_details['templateMarketName'])
                try:
                    self.assertEqual('true', market_details['isMarketBetInRun'], msg="isMarketBetInRun not found")
                    self.assertNotIn('isResulted', market_details.keys(), msg="Resulted events found")
                    self.assertIn('M', market_details['siteChannels'], msg="Site channel details not found")
                    outcomes = market_details['children']
                    for outcome in outcomes:
                        outcome_details = outcome['outcome']
                        self.assertIn('M', outcome_details['siteChannels'], msg="SiteChannel = M not found")
                        self.assertTrue(outcome_details['outcomeMeaningMajorCode'],
                                        msg="Outcome Meaning Major Code is not present")
                except KeyError:
                    self._logger.info(msg='current market' + market_details['templateMarketName'] + 'odds might suspended')
