import pytest
import tests
from tests.base_test import vtest
import voltron.environments.constants as vec
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.racing
@pytest.mark.horseracing
@pytest.mark.event_details
@pytest.mark.watch_free
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.login
@vtest
class Test_C1274039_Verify_Navigation_between_WATCH_FREE_and_LIVE_STREAM_buttons(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C1274039
    NAME: Verify Navigation between 'WATCH FREE' and 'LIVE STREAM' buttons
    DESCRIPTION: This test case verifies Navigation between 'WATCH FREE' and 'LIVE STREAM' (for Coral)/'WATCH' and 'LIVESIM'(for Ladbrokes) buttons on Event details page for **mobile and tablet**
    DESCRIPTION: This test case verifies Navigation between 'WATCH FREE' and 'LIVE STREAM' (for Coral)/'WATCH' and 'LIVESIM'(for Ladbrokes) buttons on Event details page for **desktop**
    DESCRIPTION: Test case is applicable for 'Horse racing' and 'Greyhounds' details events page
    DESCRIPTION: 'LIVESIM' is not available for 'Greyhounds'
    DESCRIPTION: 'Live Commentary' is not available on mobile and tablet, only on desktop
    PRECONDITIONS: *   Application is loaded
    PRECONDITIONS: *   Horseracing Landing page is opened
    PRECONDITIONS: *   Event is started (scheduled race-off time is reached)
    PRECONDITIONS: *   Make sure there is mapped race visualization and streaming to tested event
    PRECONDITIONS: *   User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: *   SiteServer event should be configured to support streaming
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
        event_params = self.ob_config.add_UK_racing_event(is_live=True, at_races_stream=True, time_to_start=1)
        self.__class__.eventID, self.__class__.event_off_time, self.__class__.marketID, self.__class__.selection_ids = \
            event_params.event_id, event_params.event_off_time, event_params.market_id, event_params.selection_ids
        self._logger.info(f'*** Created event with ID {self.eventID}')
        self.__class__.created_event_name = f'{self.event_off_time} {self.horseracing_autotest_uk_name_pattern.upper()}'
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.open_betslip_with_selections(selection_ids=list(self.selection_ids.values())[0])
        bet_amount = 1
        self.place_single_bet(stake_bet_amounts={list(self.selection_ids.keys())[0]: bet_amount})
        self.check_bet_receipt_is_displayed()
        self.__class__.brand_is_ladbrokes = self.brand == 'ladbrokes'
        self.__class__.device_is_mobile = self.device_type == 'mobile'

    def test_001_go_to_the_event_details_page_of_verified_started_event_from_uk__ire_group(self):
        """
        DESCRIPTION: Go to the event details page of verified started event (from 'UK & IRE' group)
        EXPECTED: **For Coral:**
        EXPECTED: * Event details page is opened
        EXPECTED: * Twо buttons 'WATCH FREE' Active and 'LIVE STREAM' inactive are displayed
        EXPECTED: * The area below 'WATCH FREE' button is expanded
        EXPECTED: * Visualization video object is shown
        EXPECTED: * An information link labeled "Find out more about Watch Free here" with '?' mark appears below Race information on the page
        EXPECTED: **For Ladbrokes:**
        EXPECTED: * Event details page is opened
        EXPECTED: * Twо buttons 'WATCH' (inactive) and 'DONE' active are displayed
        EXPECTED: * Area below 'DONE' button is expanded
        EXPECTED: * Visualization video object is shown
        EXPECTED: * 'Live Commentary' link is displayed
        EXPECTED: * Microphone icon is shown next to the 'Live Commentary' link
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        if self.brand_is_ladbrokes and not self.device_is_mobile:
            self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                            msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not displayed')
            self.assertTrue(self.horse_racing_edp.has_live_commentary_link(),
                            msg=f'"Live commentary" link is not displayed')
        else:
            self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                            msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not active')
        stream_button = self.horse_racing_edp.video_stream_button
        self.assertFalse(stream_button.is_selected(expected_result=False),
                         msg=f'"{stream_button.name}" button is active')
        self.horse_racing_edp.watch_free_button.click()
        result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                 name='Waiting for visualisation video',
                                 poll_interval=5,
                                 timeout=60)
        self.assertTrue(result, msg='Visualisation video is not shown')

    def test_002_tap_active_watch_free_for_coral_inactive_done_for_ladbrokes_button(self):
        """
        DESCRIPTION: Tap active 'WATCH FREE' (for Coral)/ active 'DONE' (for Ladbrokes) button
        EXPECTED: **For Coral:**
        EXPECTED: *   The area below 'WATCH FREE' button is collapsed
        EXPECTED: *   'WATCH FREE' button becomes inactive
        EXPECTED: *   The information link is no longer displayed
        EXPECTED: **For Ladbrokes:**
        EXPECTED: *   The area below 'DONE' button is collapsed
        EXPECTED: *   'DONE' button becomes inactive
        EXPECTED: *   'DONE' label on button changes to 'LIVESIM'
        """
        self.horse_racing_edp.watch_free_button.click()
        self.assertFalse(self.horse_racing_edp.watch_free_button.is_selected(expected_result=False),
                         msg=f'"{self.site.racing_event_details.tab_content.watch_free_button.name}" button is active')
        if self.device_is_mobile and not self.brand_is_ladbrokes:
            self.assertFalse(self.horse_racing_edp.has_watch_free_info_link(expected_result=False),
                             msg='Watch Free info link is present')

    def test_003_tap_inactive_watch_free_for_coral_inactive_watch_for_ladbrokes_button(self):
        """
        DESCRIPTION: Tap inactive 'WATCH FREE' (for Coral)/ inactive 'WATCH' (for Ladbrokes) button
        EXPECTED: **For Coral:**
        EXPECTED: * 'WATCH FREE' button becomes active
        EXPECTED: * The area below 'WATCH FREE' button is expanded
        EXPECTED: * Visualization video object is shown
        EXPECTED: * An information link labeled "Find out more about Watch Free here" with '?' mark appears under Media Area on the page
        EXPECTED: **For Ladbrokes:**
        EXPECTED: * The area below 'WATCH' button is expanded
        EXPECTED: * 'WATCH' label on button changes to 'DONE'
        """
        if self.brand_is_ladbrokes:
            self.horse_racing_edp.video_stream_button.click()
            result = wait_for_result(lambda: self.horse_racing_edp.video_stream_button.name == vec.sb.DONE.upper(),
                                     name='"WATCH" button to become "DONE"',
                                     timeout=5)
            self.assertTrue(result, msg=f'Button "{self.horse_racing_edp.video_stream_button.name}"'
                                        f' did not change label to "{vec.sb.DONE.upper()}"')
            if self.device_is_mobile:
                dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_WATCH_LIVE)
                self.assertTrue(dialog, msg='Dialog "Watch Live" is not present on page')
                self.assertEqual(dialog.error_message, vec.sb.STREAM_IS_NOT_AVAILABLE,
                                 msg=f'Stream error "{dialog.error_message}" is not the same as expected "{vec.sb.STREAM_IS_NOT_AVAILABLE}"')
                dialog.ok_button.click()
                dialog.wait_dialog_closed()
        else:
            self.site.racing_event_details.tab_content.watch_free_button.click()
            self.assertTrue(self.horse_racing_edp.watch_free_button.is_selected(),
                            msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not active')
            result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                     name='Waiting for visualisation video',
                                     poll_interval=5,
                                     timeout=10)
            self.assertTrue(result, msg='Visualisation video is not shown')
            if self.device_is_mobile:
                self.assertTrue(self.horse_racing_edp.has_watch_free_info_link(),
                                msg='Watch Free info link is not present')

    def test_004_tap_inactive_live_stream_for_coral_livesim_for_ladbrokes_button(self):
        """
        DESCRIPTION: Tap inactive 'LIVE STREAM' (for Coral)/ 'LIVESIM' (for Ladbrokes) button
        EXPECTED: **For Coral:**
        EXPECTED: *   The area below 'LIVE STREAM' button is expanded
        EXPECTED: *   'LIVE STREAM' button becomes active
        EXPECTED: *   'WATCH FREE' button  becomes inactive
        EXPECTED: *   Stream is launched !!! Note: cannot test the following (because we can't map streams) so instead verifying error message that stream is not available
        EXPECTED: *   'Possible delay: 10 seconds' text message is shown above video object
        EXPECTED: 'The Stream for this event is currently not available.' text message is shown above video object
        EXPECTED: **For Ladbrokes:**
        EXPECTED: *   The area below 'LIVESIM' button is expanded
        EXPECTED: *   'LIVESIM' button becomes active
        EXPECTED: *   'LIVESIM' label on button is changed to 'DONE'
        EXPECTED: *   'WATCH' button  becomes inActive
        EXPECTED: *   Stream is launched !!! Note: cannot test the following (because we can't map streams) so instead verifying error message that stream is not available
        EXPECTED: 'The Stream for this event is currently not available.' text message is shown above video object
        """
        if self.brand_is_ladbrokes:
            self.horse_racing_edp.watch_free_button.click()
            if not self.device_is_mobile:
                self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                                msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not displayed')
            else:
                self.assertTrue(self.horse_racing_edp.watch_free_button.is_selected(),
                                msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not active')
            self.assertEqual(self.horse_racing_edp.watch_free_button.name, vec.sb.DONE.upper(),
                             msg=f'Button "{self.horse_racing_edp.watch_free_button.name}" not '
                                 f'changed label to "{vec.sb.DONE.upper()}"')
            stream_button = self.horse_racing_edp.video_stream_button
            self.assertFalse(stream_button.is_selected(expected_result=False),
                             msg=f'"{stream_button.name}" button is active')
        else:
            self.horse_racing_edp.video_stream_button.click()
            stream_button = self.horse_racing_edp.video_stream_button
            if self.device_type == 'mobile':
                self.assertTrue(stream_button.is_selected(), msg=f'"{stream_button.name}" button is not active')
                self.assertTrue(self.horse_racing_edp.has_video_stream_area,
                                msg='Video Stream area is not shown')
                self.__class__.dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_WATCH_LIVE)
                self.assertTrue(self.dialog, msg='Dialog "Watch Live" is not present on page')
                self.assertEqual(self.dialog.error_message, vec.sb.STREAM_IS_NOT_AVAILABLE,
                                 msg=f'Stream error "{self.dialog.error_message}" is not the same as expected "{vec.sb.STREAM_IS_NOT_AVAILABLE}"')
                self.dialog.ok_button.click()
                self.dialog.wait_dialog_closed()
                self.site.wait_splash_to_hide(2)
            else:
                self.assertTrue(stream_button.is_displayed(), msg=f'"{stream_button.name}" button is not displayed')

    def test_005_tap_active_live_stream_for_coral_done_for_ladbrokes_button(self):
        """
        DESCRIPTION: Tap active 'LIVE STREAM' (for Coral)/'DONE' (for Ladbrokes) button
        EXPECTED: **For Coral:**
        EXPECTED: *   The area below 'LIVE STREAM' button is collapsed
        EXPECTED: *   'LIVE STREAM' button becomes inactive
        EXPECTED: **For Ladbrokes:**
        EXPECTED: *   The area below 'DONE' button is collapsed
        EXPECTED: *   'DONE' button becomes inactive
        EXPECTED: *   'DONE' label on button is changed to 'LIVESIM'
        """
        if self.brand_is_ladbrokes:
            self.horse_racing_edp.watch_free_button.click()
            self.assertFalse(self.horse_racing_edp.watch_free_button.is_selected(expected_result=False),
                             msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is active')
        else:
            if self.device_type == 'mobile':
                self.horse_racing_edp.video_stream_button.click()
                self.assertTrue(self.horse_racing_edp.video_stream_button.is_selected(),
                    msg=f'"{self.site.racing_event_details.tab_content.video_stream_button.name}" button is not active')
                self.dialog.ok_button.click()
                self.dialog.wait_dialog_closed()
                self.site.wait_splash_to_hide(2)
            else:
                self.assertTrue(self.horse_racing_edp.video_stream_button.is_displayed(),
                            msg=f'"{self.site.racing_event_details.tab_content.video_stream_button.name}" button is not displayed')



    def test_006_repeat_steps_4_for_coral(self):
        """
        DESCRIPTION: Repeat steps #4 (for Coral)
        """
        if not self.brand_is_ladbrokes:
            self.test_004_tap_inactive_live_stream_for_coral_livesim_for_ladbrokes_button()

    def test_007_tap_inactive_watch_free_for_coral_watch_for_ladbrokes_button(self):
        """
        DESCRIPTION: Tap inactive 'WATCH FREE' (for Coral)/'WATCH' (for Ladbrokes) button
        EXPECTED: **For Coral:**
        EXPECTED: *   The area below 'WATCH FREE' button is expanded
        EXPECTED: *   'WATCH FREE' button becomes active
        EXPECTED: *   'LIVE STREAM' button becomes inactive
        EXPECTED: *   Visualisation video object is shown
        EXPECTED: *   An information link labeled "Find out more about Watch Free here" with '?' mark appears under Media Area on the page
        EXPECTED: **For Ladbrokes:**
        EXPECTED: *   The area below 'WATCH' button is expanded
        EXPECTED: *   'WATCH' button becomes active
        EXPECTED: *   'WATCH' label on button is changed to 'DONE'
        EXPECTED: *   'LIVESIM' button becomes inactive
        EXPECTED: *   Visualization video object is shown
        """
        if self.brand_is_ladbrokes:
            self.horse_racing_edp.video_stream_button.click()
            self.assertTrue(self.horse_racing_edp.video_stream_button.is_selected(),
                            msg=f'"{self.horse_racing_edp.video_stream_button.name}" button is not active')
            self.assertEqual(self.horse_racing_edp.video_stream_button.name, vec.sb.DONE.upper(),
                             msg=f'Button "{self.horse_racing_edp.video_stream_button.name}" '
                                 f'did not change label to "{vec.sb.DONE.upper()}"')
            if self.device_is_mobile:
                dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_WATCH_LIVE)
                self.assertTrue(dialog, msg='Dialog "Watch Live" is not present on page')
                self.assertEqual(dialog.error_message, vec.sb.STREAM_IS_NOT_AVAILABLE,
                                 msg=f'Stream error "{dialog.error_message}" is not the same as expected "{vec.sb.STREAM_IS_NOT_AVAILABLE}"')
                dialog.ok_button.click()
                dialog.wait_dialog_closed()

        else:
            self.horse_racing_edp.watch_free_button.click()
            self.assertTrue(self.horse_racing_edp.watch_free_button.is_selected(),
                            msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not active')
            self.assertFalse(self.horse_racing_edp.video_stream_button.is_selected(
                expected_result=False),
                msg=f'"{self.horse_racing_edp.video_stream_button.name}" button is active')
            if self.device_is_mobile:
                self.assertTrue(self.horse_racing_edp.has_watch_free_info_link(),
                                msg='Watch Free info link is not present')
                result = wait_for_result(lambda: self.horse_racing_edp.has_watch_free_area,
                                         name='Waiting for visualisation video',
                                         timeout=5)
                self.assertTrue(result, msg='Visualisation video is not shown')
