import pytest
import tests
import voltron.environments.constants as vec

from tests.base_test import vtest
from tests.pack_010_RACES_General.BaseRacingTest import BaseRacing
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod # We cant create event in prod
@pytest.mark.login
@pytest.mark.event_details
@pytest.mark.medium
@pytest.mark.races
@pytest.mark.desktop
@pytest.mark.horseracing
@pytest.mark.watch_free
@vtest
class Test_C60094977_Verify_WATCH_button(BaseRacing, BaseBetSlipTest):
    """
    TR_ID: C60094977
    NAME: Verify WATCH button
    DESCRIPTION: This test case verifies video stream on Media Area
    DESCRIPTION: Test case is applicable for 'Horse racing' and 'Greyhounds' details events page
    DESCRIPTION: 'PRE-PARADE' is not available for 'Greyhounds'
    DESCRIPTION: 'Live Commentary' is not available on mobile and tablet, only on desktop
    DESCRIPTION: **Jira ticket: **
    DESCRIPTION: BMA-6585 - Racecard Layout Update - Media Area
    DESCRIPTION: BMA-17781 - Live Sim/Watch Free Display Change for Special Open Collapse Button
    DESCRIPTION: BMA-39820 - Desktop HR+ GH Redesign : Race Page - Streaming redesign
    DESCRIPTION: Note: Cannot automate streaming
    PRECONDITIONS: *   Event is started (scheduled race-off time is reached)
    PRECONDITIONS: *   Make sure there is streaming mapped
    PRECONDITIONS: *   User is logged in and placed a minimum sum of £1 on one or many Selections within tested event
    PRECONDITIONS: *   SiteServer event should be configured to support streaming
    PRECONDITIONS: *   Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    PRECONDITIONS: *   URLs for 'Live Commentary' should be set in CMS:
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
        DESCRIPTION: Add racing event with start time more than 5 minutes to the following groups:
        DESCRIPTION: UK & IRE,

        EXPECTED: Racing event added
        """
        event_params = self.ob_config.add_UK_racing_event(is_live=True, at_races_stream=True, time_to_start=6)
        self.__class__.eventID, selection_ids = event_params.event_id, event_params.selection_ids
        self._logger.info(f'*** Created event with ID {self.eventID}')
        self.site.login(username=tests.settings.betplacement_user, async_close_dialogs=False)
        self.open_betslip_with_selections(selection_ids=list(selection_ids.values())[0])
        bet_amount = 1
        self.place_single_bet(stake_bet_amounts={list(selection_ids.keys())[0]: bet_amount})
        self.check_bet_receipt_is_displayed()
        self.site.close_betreceipt()

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        self.site.wait_content_state('Homepage')

    def test_002_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Horse Racing> icon from the Sports Menu Ribbon
        EXPECTED: Horse Racing landing page is opened
        """
        cms_horse_tab_name = self.get_sport_title(category_id=21)
        if self.device_type == 'mobile':
            all_items = self.site.home.menu_carousel.items_as_ordered_dict
            if not self.brand == 'ladbrokes':
                all_items.get(cms_horse_tab_name.upper()).click()
            else:
                all_items.get(cms_horse_tab_name).click()
        else:
            all_items = self.site.header.sport_menu.items_as_ordered_dict
            all_items.get(cms_horse_tab_name.upper()).click()
        wait_for_result(lambda: self.site.wait_content_state('Horseracing'), timeout=20)

    def test_003_go_to_event_details_page_and_navigate_to_media_area(self):
        """
        DESCRIPTION: Go to event details page and navigate to media area
        EXPECTED: *For Coral:*
        EXPECTED: **For mobile&tablet:**
        EXPECTED: *   Twо buttons 'PRE-PARADE' and 'WATCH' are displayed and active
        EXPECTED: **For desktop:**:
        EXPECTED: *  Twо switchers 'PRE-PARADE' and 'WATCH' are displayed and active
        EXPECTED: *For Ladbrokes:*
        EXPECTED: **For mobile&tablet:**
        EXPECTED: *   Twо buttons 'WATCH' and 'PRE-PARADE' are displayed and active
        EXPECTED: **For desktop:**:
        EXPECTED: *  Twо switchers 'WATCH' and 'PRE-PARADE' are displayed and active
        EXPECTED: *  'Live Commentary' link is displayed
        EXPECTED: *   Microphone icon is shown next to the 'Live Commentary' link
        """
        self.navigate_to_edp(event_id=self.eventID, sport_name='horse-racing')
        self.__class__.horse_racing_edp = self.site.racing_event_details.tab_content
        self.assertTrue(self.horse_racing_edp.watch_free_button.is_displayed(),
                        msg=f'"PRE-PARADE" button is not displayed')
        self.assertTrue(self.horse_racing_edp.video_stream_button.is_displayed(),
                        msg=f'"{self.horse_racing_edp.watch_free_button.name}" button is not active')
        if self.brand == 'ladbrokes' and not self.device_type == 'mobile':
            self.assertTrue(self.horse_racing_edp.has_live_commentary_link(),
                            msg=f'"Live commentary" link is not displayed')
            self.assertTrue(self.horse_racing_edp.has_microphone_icon,
                            msg=f'"Microphone icon" is not displayed')

    def test_004_tap_inactive_watchbutton(self):
        """
        DESCRIPTION: Tap active 'WATCH'button
        EXPECTED: Note: different devices will launch stream differently
        EXPECTED: *   The area below 'WATCH' button is expanded
        EXPECTED: *   'WATCH' button becomes inactive
        EXPECTED: *   'WATCH' label on button is changed to 'DONE'
        EXPECTED: *   Stream is shown
        """
        # WATCH button
        self.horse_racing_edp.video_stream_button.click()
        self.assertTrue(self.horse_racing_edp.video_stream_button.is_selected(),
                        msg=f'"{self.horse_racing_edp.video_stream_button.name}" button is not active')
        if self.device_type == 'mobile':
            dialog = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_WATCH_LIVE)
            self.assertTrue(dialog, msg='Dialog "Watch Live" is not present on page')
            self.assertEqual(dialog.error_message, vec.sb.STREAM_IS_NOT_AVAILABLE,
                             msg=f'Stream error "{dialog.error_message}" '
                                 f'is not the same as expected "{vec.sb.STREAM_IS_NOT_AVAILABLE}"')
            dialog.ok_button.click()
            dialog.wait_dialog_closed()
        else:
            result = wait_for_result(lambda: self.horse_racing_edp.has_video_stream_area,
                                     name='Waiting for visualisation video',
                                     poll_interval=5,
                                     timeout=60)
            self.assertTrue(result, msg='Visualisation video is not shown')
            self.assertEqual(self.horse_racing_edp.video_stream_button.name, vec.sb.DONE.upper(),
                             msg=f'Button "{self.horse_racing_edp.video_stream_button.name}" '
                                 f'did not change label to "{vec.sb.DONE.upper()}"')
        if self.brand == 'ladbrokes' and not self.device_type == 'mobile':
            self.assertFalse(self.horse_racing_edp.has_watch_free_info_link(expected_result=False),
                             msg='Watch Free info link is present')

    def test_005_rotate_device_from_portrait_to_landscape_mode_and_vice_versa(self):
        """
        DESCRIPTION: Rotate device from Portrait to Landscape mode and vice versa
        EXPECTED: Video streaming is rotated accordingly
        """
        # Can Not Automate this step
        pass
