import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from crlat_siteserve_client.constants import ATTRIBUTES, LEVELS, OPERATORS
from crlat_siteserve_client.siteserve_client import SiteServeRequests, simple_filter, exists_filter
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.watch_free
@vtest
class Test_C60094973_Verify_Navigation_between_PRE_PARADE_and_WATCH_buttons(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C60094973
    NAME: Verify Navigation between 'PRE-PARADE' and 'WATCH' buttons
    DESCRIPTION: This test case verifies Navigation between 'PRE-PARADE' and 'LIVE STREAM'
    DESCRIPTION: Test case is applicable for 'Horse racing' and 'Greyhounds' details events page
    DESCRIPTION: 'PRE-PARADE' is not available for 'Greyhounds'
    DESCRIPTION: 'Live Commentary' is not available on mobile and tablet, only on desktop
    DESCRIPTION: **Jira tickets: **
    DESCRIPTION: *   [BMA-6588 (Quantum Leap - Horse racing visualisation)] [1]
    DESCRIPTION: *   [BMA-6585 (Racecard Layout Update - Media Area)] [2]
    DESCRIPTION: *   [BMA-17781 - Live Sim/Watch Free Display Change for Special Open Collapse Button.] [3]
    DESCRIPTION: *   [BMA-17782 (Live Sim/Watch Free Display Change for the Information Link Exception)] [4]
    DESCRIPTION: *   [BMA-39820 - Desktop HR+ GH Redesign : Race Page - Streaming redesign] [5]
    DESCRIPTION: [1]: https://jira.egalacoral.com/browse/BMA-6558
    DESCRIPTION: [2]: https://jira.egalacoral.com/browse/BMA-6585
    DESCRIPTION: [3]: https://jira.egalacoral.com/browse/BMA-17781
    DESCRIPTION: [4]: https://jira.egalacoral.com/browse/BMA-17782
    DESCRIPTION: [5]: https://jira.egalacoral.com/browse/BMA-39820
    DESCRIPTION: AUTOTEST [C528051]
    PRECONDITIONS: *   Application is loaded
    PRECONDITIONS: *   Horseracing Landing page is opened
    PRECONDITIONS: *   Event is started (scheduled race-off time is reached)
    PRECONDITIONS: *   Make sure there is mapped race visualization and streaming to tested event
    PRECONDITIONS: *   User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: *   SiteServer event should be configured to support streaming
    PRECONDITIONS: *   Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    PRECONDITIONS: URL to **Test/Demo** visualization:  https://www.racemodlr.com/coral-demo/visualiser/{event id} (implemented on DEV, TST2, STG2 environments)
    PRECONDITIONS: URL to **Real **visualization: https://www.racemodlr.com/coral/visualiser/{event id} (implemented on PROD environment)
    PRECONDITIONS: **NOTE**: It event attribute **'typeFlagCodes' **contains 'UK' or 'IE' parameter, this event is included in the group 'UK & IRE'.
    PRECONDITIONS: * URLs for 'Live Commentary' should be set in CMS:
    PRECONDITIONS: GH= https://sport.mediaondemand.net/player/ladbrokes?sport=greyhounds&showmenu=false
    PRECONDITIONS: HR= https://sport.mediaondemand.net/player/ladbrokes?sport=horses&showmenu=false
    PRECONDITIONS: To set links do the following steps:
    PRECONDITIONS: 1) Go to CMS -> System Configuration -> Structure
    PRECONDITIONS: 2) Type in Search field 'LiveCommentary'
    PRECONDITIONS: 3) Paste links in 'Field Value' per each 'Field Name'
    PRECONDITIONS: 4) Click on 'Save changes'
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Create event and Login
        DESCRIPTION: Place a bet a minimum sum of £1 on one or many Selections within tested event
        """
        if tests.settings.backend_env == 'prod':
            self.__class__.ss_req_hr = SiteServeRequests(env=tests.settings.backend_env,
                                                         class_id=self.horse_racing_live_class_ids,
                                                         category_id=self.ob_config.backend.ti.horse_racing.category_id,
                                                         brand=self.brand)
            query_params = self.basic_active_events_filter() \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.CATEGORY_ID, OPERATORS.INTERSECTS,
                                          self.ob_config.backend.ti.horse_racing.category_id)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_STARTED, OPERATORS.IS_TRUE)) \
                .add_filter(simple_filter(LEVELS.EVENT, ATTRIBUTES.IS_RESULTED, OPERATORS.IS_FALSE)) \
                .add_filter(simple_filter(LEVELS.MARKET, ATTRIBUTES.TEMPLATE_MARKET_NAME, OPERATORS.EQUALS,
                                          self.ob_config.horseracing_config.default_market_name)) \
                .add_filter(exists_filter(LEVELS.EVENT,
                                          simple_filter(LEVELS.MARKET, ATTRIBUTES.DRILLDOWN_TAG_NAMES,
                                                        OPERATORS.INTERSECTS, 'MKTFLAG_EPR,EVFLAG_AVA')))
            events = self.ss_req_hr.ss_event_to_outcome_for_class(query_builder=query_params)
            event = next((event for event in events if
                          event.get('event') and event['event'] and event['event'].get('children') and
                          ('EVFLAG_AVA' in event['event'].get('drilldownTagNames', ''))), None)
            if event is None:
                raise SiteServeException('No events are available(which are started and not resulted)')
            self.__class__.eventID = event.get('event').get('id')
            self._logger.info(f'*** Found Horse racing event with id "{self.eventID}"')
            outcomes = next(((market['market'].get('children')) for market in event['event'].get('children')), None)
            if outcomes is None:
                raise SiteServeException('No outcomes available')
            selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self._logger.info(
                f'*** Found Horse racing event with id "{self.eventID}" with selection ids: "{selection_ids}"')
        else:
            event_params = self.ob_config.add_UK_racing_event(is_live=True, at_races_stream=True, time_to_start=1)
            self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
            self._logger.info(f'*** Created event with ID {self.eventID}')
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0])
        bet_amount = 1
        self.place_single_bet(stake_bet_amounts={list(selection_ids.keys())[0]: bet_amount})
        self.check_bet_receipt_is_displayed()

    def test_001_go_to_the_event_details_page_of_verified_started_event_from_uk__ire_group(self):
        """
        DESCRIPTION: Go to the event details page of verified started event (from 'UK & IRE' group)
        EXPECTED: * Event details page is opened
        EXPECTED: * Twо buttons 'PRE-PARADE' and 'LIVE STREAM'/'WATCH' are displayed
        EXPECTED: * The area below 'PRE-PARADE' button is not expanded
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        # PRE-PARADE
        self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                        msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not active')
        # LIVE STREAM/WATCH
        stream_button = self.horse_racing_edp.video_stream_button
        self.assertTrue(stream_button.is_displayed(),
                        msg=f'"{stream_button.name}" button is not displayed')
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=30)
        self.assertFalse(result, msg='Visualisation video is shown')

    def test_002_tap_on_the_pre_parade_button(self):
        """
        DESCRIPTION: Tap on the 'PRE-PARADE' button
        EXPECTED: * 'PRE-PARADE' button becomes active
        EXPECTED: * The area below 'PRE-PARADE' button is expanded
        EXPECTED: * Visualization video object is shown
        EXPECTED: 'PRE-PARADE' label on button changes to 'DONE'
        """
        self.horse_racing_edp.watch_free_button.click()
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertTrue(result, msg='Visualisation video is not shown')
        result = wait_for_result(lambda: self.horse_racing_edp.watch_free_button.name == vec.sb.DONE.upper(),
                                 name='"PRE-PARADE" button to become "DONE"',
                                 timeout=5)
        self.assertTrue(result, msg=f'Button "{self.horse_racing_edp.watch_free_button.name}"'
                                    f' did not change label to "{vec.sb.DONE.upper()}"')

    def test_003_tap_on_the_done_button(self):
        """
        DESCRIPTION: Tap on the 'Done' button
        EXPECTED: *   The area below 'DONE' button is collapsed
        EXPECTED: *   'DONE' label on button changes to 'PRE-PARADE'
        """
        self.horse_racing_edp.watch_free_button.click()
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=30)
        self.assertFalse(result, msg='Visualisation video is shown')
        self.assertFalse(self.horse_racing_edp.watch_free_button.is_selected(expected_result=False),
                         msg=f'"{self.site.racing_event_details.tab_content.watch_free_button.name}" button is active')
        result = wait_for_result(lambda: self.horse_racing_edp.watch_free_button.name == vec.sb.PRE_PARADE.upper(),
                                 name='"DONE" button to become "PRE-PARADE"',
                                 timeout=5)
        self.assertTrue(result, msg=f'Button "{self.horse_racing_edp.watch_free_button.name}"'
                                    f' did not change label to "{vec.sb.PRE_PARADE.upper()}"')

    def test_004_tap_on_the_watchbutton(self):
        """
        DESCRIPTION: Tap on the 'WATCH'button
        EXPECTED: *   The area below 'WATCH' button is expanded
        EXPECTED: *   'WATCH' label on button is changed to 'DONE'
        EXPECTED: *    Stream is launched
        """
        # Streaming cannot be automated - Streaming feed not available for QA2
        # WATCH button
        self.horse_racing_edp.video_stream_button.click()
        self.assertTrue(self.horse_racing_edp.video_stream_button.is_selected(),
                        msg=f'"{self.horse_racing_edp.video_stream_button.name}" button is not active')
        if self.device_type == 'desktop' or tests.settings.backend_env == 'prod':
            result = wait_for_result(lambda: self.horse_racing_edp.has_video_stream_area,
                                     name='Waiting for visualisation video',
                                     poll_interval=5,
                                     timeout=60)
            self.assertTrue(result, msg='Visualisation video is not shown')
            self.assertEqual(self.horse_racing_edp.video_stream_button.name, vec.sb.DONE.upper(),
                             msg=f'Button "{self.horse_racing_edp.video_stream_button.name}" '
                                 f'did not change label to "{vec.sb.DONE.upper()}"')
        else:
            dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_WATCH_LIVE)
            self.assertTrue(dialog, msg='Dialog "Watch Live" is not present on page')
            self.assertEqual(dialog.error_message, vec.sb.STREAM_IS_NOT_AVAILABLE,
                             msg=f'Stream error "{dialog.error_message}" is not the same as expected "{vec.sb.STREAM_IS_NOT_AVAILABLE}"')
            dialog.ok_button.click()
            dialog.wait_dialog_closed()

    def test_005_tap_on_the_done_button(self):
        """
        DESCRIPTION: Tap on the 'DONE' button
        EXPECTED: *   The area below 'DONE' button is collapsed
        EXPECTED: *   'DONE' label on button is changed to 'WATCH'
        """
        if not self.device_type == 'mobile':
            self.horse_racing_edp.video_stream_button.click()
            self.assertFalse(self.horse_racing_edp.video_stream_button.is_selected(expected_result=False),
                             msg=f'"{self.site.racing_event_details.tab_content.watch_free_button.name}" button is active')
        self.assertEqual(self.horse_racing_edp.video_stream_button.name, vec.sb.WATCH.upper(),
                         msg=f'Button "{self.horse_racing_edp.video_stream_button.name}" '
                             f'did not change label to "{vec.sb.WATCH.upper()}"')

    def test_006_tap_on_the_pre_parade_button(self):
        """
        DESCRIPTION: Tap on the 'PRE-PARADE' button
        EXPECTED: *   The area below 'PRE-PARADE' button is expanded
        EXPECTED: *   'PRE-PARADE' label on button is changed to 'DONE'
        EXPECTED: *   Visualization video object is shown
        """
        self.test_002_tap_on_the_pre_parade_button()
